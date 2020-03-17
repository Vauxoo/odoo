# -*- coding: utf-8 -*-

import time
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
from datetime import datetime
from dateutil.relativedelta import relativedelta


try:
    from line_profiler import LineProfiler

    def do_profile(follow=[]):
        def inner(func):
            def profiled_func(*args, **kwargs):
                try:
                    profiler = LineProfiler()
                    profiler.add_function(func)
                    for f in follow:
                        profiler.add_function(f)
                    profiler.enable_by_count()
                    return func(*args, **kwargs)
                finally:
                    profiler.print_stats()
            return profiled_func
        return inner

except ImportError:
    def do_profile(follow=[]):
        "Helpful if you accidentally leave in production!"
        def inner(func):
            def nothing(*args, **kwargs):
                return func(*args, **kwargs)
            return nothing
        return inner


class ReportAgedPartnerBalance(models.AbstractModel):

    _name = 'report.account.report_agedpartnerbalance'
    _description = 'Aged Partner Balance Report'

    # @do_profile(follow=[])
    def _get_partner_move_lines(self, account_type, date_from, target_move, period_length):
        # This method can receive the context key 'include_nullified_amount' {Boolean}
        # Do an invoice and a payment and unreconcile. The amount will be nullified
        # By default, the partner wouldn't appear in this report.
        # The context key allow it to appear
        # In case of a period_length of 30 days as of 2019-02-08, we want the following periods:
        # Name       Stop         Start
        # 1 - 30   : 2019-02-07 - 2019-01-09
        # 31 - 60  : 2019-01-08 - 2018-12-10
        # 61 - 90  : 2018-12-09 - 2018-11-10
        # 91 - 120 : 2018-11-09 - 2018-10-11
        # +120     : 2018-10-10
        ctx = self._context
        periods = {}
        date_from = fields.Date.from_string(date_from)
        start = date_from
        for i in range(5)[::-1]:
            stop = start - relativedelta(days=period_length)
            period_name = str((5-(i+1)) * period_length + 1) + '-' + str((5-i) * period_length)
            period_stop = (start - relativedelta(days=1)).strftime('%Y-%m-%d')
            if i == 0:
                period_name = '+' + str(4 * period_length)
            periods[str(i)] = {
                'name': period_name,
                'stop': period_stop,
                'start': (i!=0 and stop.strftime('%Y-%m-%d') or False),
            }
            start = stop

        res = []
        total = []
        partner_clause = ''
        cr = self.env.cr
        user_company = self.env.user.company_id
        user_currency = user_company.currency_id
        company_ids = self._context.get('company_ids') or [user_company.id]
        move_state = ['draft', 'posted']
        if target_move == 'posted':
            move_state = ['posted']
        arg_list = (tuple(move_state), tuple(account_type), date_from, date_from,)
        kwargs = {
            'states': tuple(move_state),
            'date_from': date_from,
            'company_ids': tuple(company_ids),
            'types': tuple(account_type),
        }
        if ctx.get('partner_ids'):
            partner_clause = 'AND (l.partner_id IN %(partner_ids)s)'
            kwargs['partner_ids'] = tuple(ctx['partner_ids'].ids)
        if ctx.get('partner_categories'):
            partner_clause = 'AND (l.partner_id IN %(partner_ids)s)'
            partner_ids = self.env['res.partner'].search([('category_id', 'in', ctx['partner_categories'].ids)]).ids
            kwargs['partner_ids'] = tuple(partner_ids or [0])
        kwargs['partner_clause'] = partner_clause

        query = '''
            SELECT DISTINCT l.partner_id
            FROM account_move_line AS l
            INNER JOIN account_account AS aa ON aa.id = l.account_id
            INNER JOIN account_move AS am ON am.id = l.move_id
            WHERE
                (am.state IN %%(states)s)
                AND (aa.internal_type IN %%(types)s)
                AND l.reconciled IS FALSE
                AND (l.date <= %%(date_from)s)
                AND l.company_id IN %%(company_ids)s
                %(partner_clause)s
            UNION
            SELECT DISTINCT l.partner_id
            FROM account_move_line AS l
            INNER JOIN account_partial_reconcile AS apr ON (
                apr.credit_move_id = l.id OR apr.debit_move_id = l.id)
            INNER JOIN account_account AS aa ON aa.id = l.account_id
            INNER JOIN account_move AS am ON am.id = l.move_id
            WHERE
                (am.state IN %%(states)s)
                AND (aa.internal_type IN %%(types)s)
                AND apr.max_date > %%(date_from)s
                AND (l.date <= %%(date_from)s)
                AND l.company_id IN %%(company_ids)s
                %(partner_clause)s
                '''
        cr.execute(query % kwargs, kwargs)
        partners = cr.fetchall()
        some_var = False
        if False in partners:
            some_var = True

        query = '''
            SELECT id AS partner_id, UPPER(name)
            FROM res_partner
            WHERE id IN %s
            ORDER BY UPPER(name)
        '''
        cr.execute(query, (tuple(partners or [0]),))
        partners = cr.dictfetchall()

        if some_var:
            partners += [{'partner_id': 0, 'UPPER': ''}]
        # partners = [x for x in partners if x['partner_id'] == 1874]
        # put a total of 0
        for i in range(7):
            total.append(0)

        # Build a string like (1,2,3) for easy use in SQL query
        partner_ids = [partner['partner_id'] for partner in partners if partner['partner_id']]
        lines = dict((partner['partner_id'] or False, []) for partner in partners)
        # partner_ids = [partner['partner_id'] for partner in partners if partner['partner_id'] and partner['partner_id'] == 1874]
        # lines = dict((partner['partner_id'] or False, []) for partner in partners if partner['partner_id'] == 1874)
        if not partner_ids:
            return [], [], {}

        # Use one query per period and store results in history (a list variable)
        # Each history will contain: history[1] = {'<partner_id>': <partner_debit-credit>}
        history = []
        for i in range(5):
            args_list = (tuple(move_state), tuple(account_type), tuple(partner_ids),)
            dates_query = '(COALESCE(l.date_maturity,l.date)'

            if periods[str(i)]['start'] and periods[str(i)]['stop']:
                dates_query += ' BETWEEN %s AND %s)'
                args_list += (periods[str(i)]['start'], periods[str(i)]['stop'])
            elif periods[str(i)]['start']:
                dates_query += ' >= %s)'
                args_list += (periods[str(i)]['start'],)
            else:
                dates_query += ' <= %s)'
                args_list += (periods[str(i)]['stop'],)
            args_list += (date_from, tuple(company_ids))

            query = '''SELECT l.id
                    FROM account_move_line AS l, account_account, account_move am
                    WHERE (l.account_id = account_account.id) AND (l.move_id = am.id)
                        AND (am.state IN %s)
                        AND (account_account.internal_type IN %s)
                        AND ((l.partner_id IN %s) OR (l.partner_id IS NULL))
                        AND ''' + dates_query + '''
                    AND (l.date <= %s)
                    AND l.company_id IN %s
                    ORDER BY COALESCE(l.date_maturity, l.date)'''
            cr.execute(query, args_list)
            partners_amount = {}
            aml_ids = cr.fetchall()
            # include_ids = [3829474, 3829472, 3829461, 3314156, 3314151, 3314114, 3314008, 3313909, 3313880, 3313826, 3313692, 3313671, 3313639, 3313544, 3313465, 3313450, 3313382, 3313359, 3307357, 3307191, 2577669, 2542495, 2542459, 2542455, 2534489]
            # aml_ids = aml_ids and [x[0] for x in aml_ids if x[0] in include_ids] or []
            aml_ids = aml_ids and [x[0] for x in aml_ids] or []
            for line in self.env['account.move.line'].browse(aml_ids).with_context(prefetch_fields=False):
                partner_id = line.partner_id.id or False
                if partner_id not in partners_amount:
                    partners_amount[partner_id] = 0.0
                line_amount = line.company_id.currency_id._convert(line.balance, user_currency, user_company, date_from)
                if user_currency.is_zero(line_amount):
                    continue
                if not line.currency_id:
                    for partial_line in line.matched_debit_ids.filtered(lambda x: x.max_date <= date_from):
                        line_amount += partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from)
                    for partial_line in line.matched_credit_ids.filtered(lambda x: x.max_date <= date_from):
                        line_amount -= partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from)
                else:
                    line_amount_currency = line.amount_currency
                    for partial_line in line.matched_debit_ids.filtered(lambda x: x.max_date <= date_from):
                        line_amount += partial_line.currency_id._convert(partial_line.amount_currency, user_currency, user_company, date_from)
                        if partial_line.currency_id and partial_line.currency_id == line.currency_id:
                            line_amount_currency += partial_line.amount_currency
                        elif partial_line.currency_id and partial_line.currency_id != line.currency_id:
                            line_amount_currency += partial_line.currency_id._convert(partial_line.amount_currency, line.currency_id, line.company_id, partial_line.max_date)
                        else:
                            line_amount_currency += partial_line.company_id.currency_id._convert(partial_line.amount, line.currency_id, line.company_id, partial_line.max_date)
                    for partial_line in line.matched_credit_ids.filtered(lambda x: x.max_date <= date_from):
                        line_amount -= partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from)
                        if partial_line.currency_id and partial_line.currency_id == line.currency_id:
                            line_amount_currency -= line.amount_currency
                        elif partial_line.currency_id and partial_line.currency_id != line.currency_id:
                            line_amount_currency -= partial_line.currency_id._convert(partial_line.amount_currency, line.currency_id, line.company_id, partial_line.max_date)
                        else:
                            line_amount_currency -= partial_line.company_id.currency_id._convert(partial_line.amount, line.currency_id, line.company_id, partial_line.max_date)
                    if self.env.user.company_id.currency_id.is_zero(line_amount_currency):
                        line_amount = 0
                    # line_amount = line.currency_id._convert(line_amount_currency, user_currency, user_company, date_from)

                if not self.env.user.company_id.currency_id.is_zero(line_amount):
                    partners_amount[partner_id] += line_amount
                    lines.setdefault(partner_id, [])
                    lines[partner_id].append({
                        'line': line,
                        'amount': line_amount,
                        'period': i + 1,
                        })
            history.append(partners_amount)

        # This dictionary will store the not due amount of all partners
        undue_amounts = {}
        query = '''SELECT l.id
                FROM account_move_line AS l, account_account, account_move am
                WHERE (l.account_id = account_account.id) AND (l.move_id = am.id)
                    AND (am.state IN %s)
                    AND (account_account.internal_type IN %s)
                    AND (COALESCE(l.date_maturity,l.date) >= %s)\
                    AND ((l.partner_id IN %s) OR (l.partner_id IS NULL))
                AND (l.date <= %s)
                AND l.company_id IN %s
                ORDER BY COALESCE(l.date_maturity, l.date)'''
        cr.execute(query, (tuple(move_state), tuple(account_type), date_from, tuple(partner_ids), date_from, tuple(company_ids)))
        aml_ids = cr.fetchall()
        # include_ids = [3829474, 3829472, 3829461, 3314156, 3314151, 3314114, 3314008, 3313909, 3313880, 3313826, 3313692, 3313671, 3313639, 3313544, 3313465, 3313450, 3313382, 3313359, 3307357, 3307191, 2577669, 2542495, 2542459, 2542455, 2534489]
        aml_ids = aml_ids and [x[0] for x in aml_ids] or []
        # aml_ids = aml_ids and [x[0] for x in aml_ids if x[0] in include_ids] or []
        for line in self.env['account.move.line'].browse(aml_ids):
            partner_id = line.partner_id.id or False
            if partner_id not in undue_amounts:
                undue_amounts[partner_id] = 0.0
            line_amount = line.company_id.currency_id._convert(line.balance, user_currency, user_company, date_from)
            if user_currency.is_zero(line_amount):
                continue
            if not line.currency_id:
                for partial_line in line.matched_debit_ids.filtered(lambda x: x.max_date <= date_from):
                    line_amount += partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from)
                for partial_line in line.matched_credit_ids.filtered(lambda x: x.max_date <= date_from):
                    line_amount -= partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from)
            else:
                line_amount_currency = line.amount_currency
                for partial_line in line.matched_debit_ids.filtered(lambda x: x.max_date <= date_from):
                    line_amount += partial_line.currency_id._convert(partial_line.amount_currency, user_currency, user_company, date_from)
                    if partial_line.currency_id and partial_line.currency_id == line.currency_id:
                        line_amount_currency += partial_line.amount_currency
                    elif partial_line.currency_id and partial_line.currency_id != line.currency_id:
                        line_amount_currency += partial_line.currency_id._convert(partial_line.amount_currency, line.currency_id, line.company_id, partial_line.max_date)
                    else:
                        line_amount_currency += partial_line.company_id.currency_id._convert(partial_line.amount, line.currency_id, line.company_id, partial_line.max_date)
                for partial_line in line.matched_credit_ids.filtered(lambda x: x.max_date <= date_from):
                    line_amount -= partial_line.company_id.currency_id._convert(partial_line.amount, user_currency, user_company, date_from)
                    if partial_line.currency_id and partial_line.currency_id == line.currency_id:
                        line_amount_currency -= line.amount_currency
                    elif partial_line.currency_id and partial_line.currency_id != line.currency_id:
                        line_amount_currency -= partial_line.currency_id._convert(partial_line.amount_currency, line.currency_id, line.company_id, partial_line.max_date)
                    else:
                        line_amount_currency -= partial_line.company_id.currency_id._convert(partial_line.amount, line.currency_id, line.company_id, partial_line.max_date)
                if self.env.user.company_id.currency_id.is_zero(line_amount_currency):
                    line_amount = 0
                # line_amount = line.currency_id._convert(line_amount_currency, user_currency, user_company, date_from)

            if not self.env.user.company_id.currency_id.is_zero(line_amount):
                undue_amounts[partner_id] += line_amount
                lines.setdefault(partner_id, [])
                lines[partner_id].append({
                    'line': line,
                    'amount': line_amount,
                    'period': 6,
                })

        for partner in partners:
            if partner['partner_id'] is None:
                partner['partner_id'] = False
            at_least_one_amount = False
            values = {}
            undue_amt = 0.0
            if partner['partner_id'] in undue_amounts:  # Making sure this partner actually was found by the query
                undue_amt = undue_amounts[partner['partner_id']]

            total[6] = total[6] + undue_amt
            values['direction'] = undue_amt
            if not float_is_zero(values['direction'], precision_rounding=self.env.user.company_id.currency_id.rounding):
                at_least_one_amount = True

            for i in range(5):
                during = False
                if partner['partner_id'] in history[i]:
                    during = [history[i][partner['partner_id']]]
                # Adding counter
                total[(i)] = total[(i)] + (during and during[0] or 0)
                values[str(i)] = during and during[0] or 0.0
                if not float_is_zero(values[str(i)], precision_rounding=self.env.user.company_id.currency_id.rounding):
                    at_least_one_amount = True
            values['total'] = sum([values['direction']] + [values[str(i)] for i in range(5)])
            ## Add for total
            total[(i + 1)] += values['total']
            values['partner_id'] = partner['partner_id']
            if partner['partner_id']:
                #browse the partner name and trust field in sudo, as we may not have full access to the record (but we still have to see it in the report)
                browsed_partner = self.env['res.partner'].sudo().browse(partner['partner_id'])
                values['name'] = browsed_partner.name and len(browsed_partner.name) >= 45 and browsed_partner.name[0:40] + '...' or browsed_partner.name
                values['trust'] = browsed_partner.trust
            else:
                values['name'] = _('Unknown Partner')
                values['trust'] = False

            if at_least_one_amount or (self._context.get('include_nullified_amount') and lines[partner['partner_id']]):
                res.append(values)

        return res, total, lines

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        total = []
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))

        target_move = data['form'].get('target_move', 'all')
        date_from = fields.Date.from_string(data['form'].get('date_from')) or fields.Date.today()

        if data['form']['result_selection'] == 'customer':
            account_type = ['receivable']
        elif data['form']['result_selection'] == 'supplier':
            account_type = ['payable']
        else:
            account_type = ['payable', 'receivable']

        movelines, total, dummy = self._get_partner_move_lines(account_type, date_from, target_move, data['form']['period_length'])
        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_partner_lines': movelines,
            'get_direction': total,
            'company_id': self.env['res.company'].browse(
                data['form']['company_id'][0]),
        }

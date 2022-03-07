odoo.define('pos_restaurant.TipScreen', function (require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const PosComponent = require('point_of_sale.PosComponent');
    const { parse } = require('web.field_utils');
    const { useContext } = owl.hooks;

    class TipScreen extends PosComponent {
        constructor() {
            super(...arguments);
            this.state = useContext(this.currentOrder.uiState.TipScreen);
            this._totalAmount = this.currentOrder.get_total_with_tax();
        }
        mounted () {
            this.printTipReceipt();
        }
        get overallAmountStr() {
            const tipAmount = parse.float(this.state.inputTipAmount || '0');
            const original = this.env.pos.format_currency(this.totalAmount);
            const tip = this.env.pos.format_currency(tipAmount);
            const overall = this.env.pos.format_currency(this.totalAmount + tipAmount);
            return `${original} + ${tip} tip = ${overall}`;
        }
        get totalAmount() {
            return this._totalAmount;
        }
        get currentOrder() {
            return this.env.pos.get_order();
        }
        get percentageTips() {
            return [
                { percentage: '15%', amount: 0.15 * this.totalAmount },
                { percentage: '20%', amount: 0.2 * this.totalAmount },
                { percentage: '25%', amount: 0.25 * this.totalAmount },
            ];
        }
        async validateTip() {
            const amount = parse.float(this.state.inputTipAmount) || 0;
            const order = this.env.pos.get_order();
            const serverId = this.env.pos.validated_orders_name_server_id_map[order.name];

            if (!serverId) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Unsynced order'),
                    body: this.env._t('This order is not yet synced to server. Make sure it is synced then try again.'),
                });
                return;
            }

            if (!amount) {
                await this.rpc({
                    method: 'set_no_tip',
                    model: 'pos.order',
                    args: [serverId],
                });
                this.goNextScreen();
                return;
            }

            if (amount > 0.25 * this.totalAmount) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: 'Are you sure?',
                    body: `${this.env.pos.format_currency(
                        amount
                    )} is more than 25% of the order's total amount. Are you sure of this tip amount?`,
                });
                if (!confirmed) return;
            }
            /**
             * Callback to be notified, when all the rewards are finish being updated.
             * kept here to have access to the variables used within `validateTip`.
             */
             const _callbackAfterTip = async () => {
                /**
                 * We only want this to be notified once so we insta-clear this callback.
                 * Also in this point we can safely set the order back to `finalzed = true`,
                 * since all the rewards has been applied.
                 */
                order.off('rewards-updated', _callbackAfterTip);
                order.finalized = true;
                /**
                 * All the rest of the code within `_callbackAfterTip`, has been kept intact.
                 */
                const paymentline = this.env.pos.get_order().get_paymentlines()[0];
                if (paymentline.payment_method.payment_terminal) {
                    paymentline.amount += amount;
                    await paymentline.payment_method.payment_terminal.send_payment_adjust(paymentline.cid);
                }
                // set_tip calls add_product which sets the new line as the selected_orderline
                const tip_line = order.selected_orderline;
                await this.rpc({
                    method: 'set_tip',
                    model: 'pos.order',
                    args: [serverId, tip_line.export_as_JSON()],
                });
                this.goNextScreen();
            };
            // set the tip by temporarily allowing order modification
            order.finalized = false;
            /**
             * The trigger `rewards-updated`, is only ran, if there is programs to be set. so we need
             * this evaluation to use sync or async workflow.
             */
            if (this.env.pos.config.promo_programs_ids?.length) {
                /**
                 * Since `set_tip` has asyncronous actions, we need to wait for them to be done
                 * after we block our order again, so we declare the callback.
                 */
                order.on('rewards-updated', _callbackAfterTip);
                order.set_tip(amount);
            } else {
                order.set_tip(amount);
                _callbackAfterTip();
            }
        }
        goNextScreen() {
            this.env.pos.get_order().finalize();
            const { name, props } = this.nextScreen;
            this.showScreen(name, props);
        }
        get nextScreen() {
            if (this.env.pos.config.module_pos_restaurant && this.env.pos.config.iface_floorplan) {
                const table = this.env.pos.table;
                return { name: 'FloorScreen', props: { floor: table ? table.floor : null } };
            } else {
                return { name: 'ProductScreen' };
            }
        }
        async printTipReceipt() {
            const receipts = [
                this.currentOrder.selected_paymentline.ticket,
                this.currentOrder.selected_paymentline.cashier_receipt
            ];

            for (let i = 0; i < receipts.length; i++) {
                const data = receipts[i];
                var receipt = this.env.qweb.renderToString('TipReceipt', {
                    receipt: this.currentOrder.getOrderReceiptEnv().receipt,
                    data: data,
                    total: this.env.pos.format_currency(this.totalAmount),
                });

                if (this.env.pos.proxy.printer) {
                    await this._printIoT(receipt);
                } else {
                    await this._printWeb(receipt);
                }
            }
        }

        async _printIoT(receipt) {
            const printResult = await this.env.pos.proxy.printer.print_receipt(receipt);
            if (!printResult.successful) {
                await this.showPopup('ErrorPopup', {
                    title: printResult.message.title,
                    body: printResult.message.body,
                });
            }
        }

        async _printWeb(receipt) {
            try {
                $(this.el).find('.pos-receipt-container').html(receipt);
                window.print();
            } catch (err) {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Printing is not supported on some browsers'),
                    body: this.env._t(
                        'Printing is not supported on some browsers due to no default printing protocol ' +
                            'is available. It is possible to print your tickets by making use of an IoT Box.'
                    ),
                });
            }
        }
    }
    TipScreen.template = 'pos_restaurant.TipScreen';

    Registries.Component.add(TipScreen);

    return TipScreen;
});

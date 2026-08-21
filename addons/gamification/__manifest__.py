# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Gamification',
    'sequence': 160,
    'category': 'Human Resources',
    'depends': ['mail'],
    'data': [
        'wizard/update_goal.xml',
        'wizard/grant_badge.xml',
        'views/res_users_views.xml',
        'views/gamification_karma_rank_views.xml',
        'views/gamification_karma_tracking_views.xml',
        'views/gamification_badge_views.xml',
        'views/gamification_badge_user_views.xml',
        'views/gamification_goal_views.xml',
        'views/gamification_goal_definition_views.xml',
        'views/gamification_challenge_views.xml',
        'views/gamification_challenge_line_views.xml',
        'views/gamification_menus.xml',
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',  # keep before to populate challenge reports
        'data/gamification_badge_data.xml',
        'data/gamification_challenge_data.xml',
        'data/gamification_karma_rank_data.xml',

        'security/ir.access.csv',
    ],
    'demo': [
        'data/gamification_karma_rank_demo.xml',
        'data/gamification_karma_tracking_demo.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}

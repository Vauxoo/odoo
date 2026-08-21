{
    'name': 'Survey CRM',
    'category': 'Marketing/Surveys',
    'summary': 'Generate leads from surveys',
    'depends': ['survey', 'crm'],
    'data': [
        'views/survey_question_views.xml',
        'views/survey_survey_views.xml',
        'views/survey_user_views.xml',
    ],
    'demo': [
        'demo/lead_qualification_survey_demo.xml',
        'demo/lead_qualification_answer_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'survey_crm/static/src/components/lead_generation_dropdown/crm_lead_gen_element.js',
        ],
    },
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}

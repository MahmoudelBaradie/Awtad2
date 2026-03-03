{
    'name': 'Real Estate Core',
    'version': '19.0.1.0.0',
    'summary': 'Shared entities for real estate ERP',
    'depends': ['base', 'mail', 'analytic', 'account'],
    'data': [
        'security/real_estate_core_security.xml',
        'data/group_alias_data.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/real_estate_menu.xml',
        'views/real_estate_config_views.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}

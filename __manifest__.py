{
    "name": "Lunch Menu Mangement kanban",
    "version": "1.0.0",
    "summary": "A module for Lunch menu management ",
    "description": """
    This module is for seamlessly manage 
    a office lunch system
    """,
    "author": "Sami",
    "category": "Practice",
    # "website": ""
    "license": "LGPL-3",
    "depends": ["base", "web", "sale", "mail"],
    "data": [
        'security/ir.model.access.csv',
        'data/lunch_menu_management.menu.csv',
        'views/menu_view.xml',
        'views/lunch_view.xml',
        'views/employee_views.xml',
        'views/sale_order_line_inherited.xml',
        'views/res_config_settings_views.xml',
        'views/ir_sequence.xml',
        'views/lunch_menu_management_menu.xml',
        'report/basic_report_template.xml',
        'report/inherited_menu_report_template.xml',
        'wizard/menu_data_update_wizard.xml',
        'wizard/menu_report_excel_wizard.xml'
    ],
    # "auto_install": True,
    "application": True,
}

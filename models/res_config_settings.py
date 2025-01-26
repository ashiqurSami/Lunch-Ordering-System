from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    number_of_menu_per_lunch=fields.Integer(string="Number of menus per lunch", config_parameter='lunch_menu_management.number_of_menu_per_lunch',default=10)
    number_of_order_per_user=fields.Integer(string="Number of orders per user", config_parameter='lunch_menu_management.number_of_order_per_user')
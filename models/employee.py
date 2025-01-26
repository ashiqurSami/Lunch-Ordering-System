from odoo import models, fields, api

class Employee(models.Model):
    _name = 'lunch_menu_management.employee'
    _description = 'Employee Info'

    name = fields.Char(string='Name', required=True)
    designation = fields.Char(string='Designation', required=True)

    lunch_ids=fields.One2many('lunch_menu_management.lunch','employee_id')
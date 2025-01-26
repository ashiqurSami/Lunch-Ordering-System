from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class Lunch(models.Model):
    _name = 'lunch_menu_management.lunch'
    _description = 'Lunch Order'

    name = fields.Char(string="User Name", required=True)
    date = fields.Date(string='Date', default=fields.Date.today, required=True)

    state=fields.Selection(
        [
            ('draft','Draft'),
            ('confirm','Confirmed'),
            ('cancelled', 'Cancelled'),
            ('approved','Approved')
        ],
        required=True,
        default='draft',
        tracking=True
    )

    menu_item_ids = fields.Many2many(
        'lunch_menu_management.menu',
        'lunch_menu_rels',
        'lunch_id',
        'menu_id'
    )

    employee_id = fields.Many2one('lunch_menu_management.employee', string="Employee")

    day = fields.Char(string="Day", compute="_compute_day", store=True)

    @api.depends('date')
    def _compute_day(self):
        for record in self:
            if record.date:
                record.day = record.date.strftime('%A')



    total_price = fields.Float(string="Total Bill", compute="_computed_total_price")

    @api.depends('menu_item_ids')
    def _computed_total_price(self):
        for record in self:
            total= sum(menu.price for menu in record.menu_item_ids)
            record.total_price=total


    @api.ondelete(at_uninstall=False)
    def _on_delete_cleanup(self):
        for record in self:
            if record.date and record.date < fields.Date.today():
                raise UserError(_("You cannot delete past lunch menu records."))


    def write(self, vals):
        for record in self:
            if 'date' in vals and vals['date'] < fields.Date.today().isoformat():
                raise UserError(_("You cannot modify records for past dates."))
        return super().write(vals)


    def remove_order(self):
        for record in self:
            if record.date and record.date < fields.Date.today() or record.state=="approved":
                raise UserError(_("You cannot modify records for past dates."))
            record.menu_item_ids.unlink()

    def action_confirm(self):
        self.ensure_one()
        return self.write({'state':'confirm'})

    def action_draft(self):
        self.ensure_one()
        if "approved" in self.mapped('state'):
            raise UserError(_("You cannot draft already approved orders."))
        self.remove_order()
        return self.write({'state':'draft'})

    def action_cancel(self):
        if "approved" in self.mapped('state'):
            raise UserError(_("You cannot draft already approved orders."))
        self.remove_order()
        return self.write({'state': 'cancelled'})

    def action_approve(self):
        if not self.env.user.has_group('lunch_menu_management.group_admin'):
            raise UserError(_("You do not have permission to perform this action."))
        return self.write({'state': 'approved'})


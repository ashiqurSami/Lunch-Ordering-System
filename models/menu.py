from random import randint

from odoo import fields,api,models,_
from odoo.exceptions import ValidationError, UserError


class Menu(models.Model):
    _name="lunch_menu_management.menu"
    _description = "Menu"
    _rec_name = 'menu_id_sequence'
    _inherit =['mail.thread','mail.activity.mixin']

    menu_item = fields.Char(string="Menu Item", required=True)

    active=fields.Boolean(default=True)

    price=fields.Monetary(
        string="Price",
        required=True,
        currency_field="default_currency",
        help="Price of the menu item",
    )
    image=fields.Image(required=True)

    default_currency=fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id
    )

    color = fields.Integer("Color index",
                           default=lambda self: randint(0,11),
                           readonly=True)

    category=fields.Char()

    partner=fields.Many2one('res.partner',string="Partner")

    menu_id_sequence=fields.Char(string="Menu ID",
                            required=True,
                            copy=False,
                            readonly=True,
                            index='trigram',
                            default=lambda self:_('New'))

    @api.model
    def create(self,vals):
        if vals.get('menu_id_sequence',_('New'))==_('New'):
            vals['menu_id_sequence']=self.env['ir.sequence'].next_by_code(
                'menu.id.sequence') or _('New')
        return super(Menu,self).create(vals)

    @api.model
    def name_create(self,menu_item):
        record=self.create({
            'menu_item':menu_item,
            'color':randint(0,11)
        })
        return record.id,record.display_name

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError(_("Price must be a non-negative value."))


    # display_name=fields.Char(
    #     compute="_compute_display_name"
    # )
    #
    # @api.depends('menu_item','price','default_currency')
    # def _compute_display_name(self):
    #     for record in self:
    #         currency_symbol = record.default_currency.symbol or 'tk'
    #         record.display_name=f"{record.menu_item} - {record.price}{currency_symbol}"

    def action_on_click(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Menu',
            'res_model':'lunch_menu_management.menu',
            'view_mode':'form',
            'res_id':self.id,
            'target':'new',
        }

    def url_action(self):
        return{
            'type':'ir.actions.act_url',
            'url':'https://order.peyala.com/',
            'target':'new'
        }

    # def url_action(self):
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': 'my/school/',
    #         'target': 'new'
    #     }

    def print_state(self):
        print(self.menu_item)

    def cron_alert(self):
        for record in self.search([]):
            record.message_post(body="hello i am corn job")

    def write(self, vals):
        if self.image:
            file_size = self.with_context(bin_size=True).image
            if file_size:
                file_size = file_size.decode('utf-8')
                file_size = file_size.split(' ')
                if (file_size[1] == 'Kb' and float(file_size[0]) > 1024) or (
                        file_size[1] == 'Mb' and float(file_size[0]) > 1):
                    raise UserError('Image size cannot exceed 1 MB')

        return super(Menu, self).write(vals)

    def custom_log(self):
        self.message_post(body='Custom log message')
        print(self.env.context)
        print(self._context)

    def action_update_data(self):
        action = self.env.ref('lunch_menu_management.menu_data_update_wizard_action').read()[0]
        print(type(action))
        print(action)
        return self.env.ref('lunch_menu_management.menu_data_update_wizard_action').read()[0]
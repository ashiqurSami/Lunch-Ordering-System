from odoo import models, fields, api

class InheritedSalesOrderLine(models.Model):
    _inherit ='sale.order.line'

    product_image=fields.Binary(related='product_template_id.image_1920',
                                string='Product Image',
                                readonly=True,
                                store=False)
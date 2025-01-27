from odoo import api, fields, models


class MenuDataUpdate(models.TransientModel):
    _name = 'menu.data.update.wizard'
    _description = 'Menu Data Update'

    price = fields.Float()

    def update_data(self):
        active_ids = self.env.context.get('active_ids')
        active_model = self.env.context.get('active_model')

        if active_ids and active_model:
            records = self.env[active_model].browse(active_ids)
            for record in records:
                record.write({
                    'price': self.price
                })

from odoo import models, fields, api

class MenuReportExcelWizard(models.TransientModel):
    _name="menu.report.excel.wizard"
    _description="Menu Report Excel Wizard"

    menu_id=fields.Many2one('lunch_menu_management.menu',string="Menu")
    preview=fields.Html(string="Preview",readonly=True)

    def menu_report(self):
        pass

    def menu_report_pdf(self):
        pass

    def menu_report_excel(self):
        pass

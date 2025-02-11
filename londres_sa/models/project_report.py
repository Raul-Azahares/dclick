from odoo import models, fields, api
import io
import xlsxwriter
import base64

class ProjectReportWizard(models.TransientModel):
    _name = 'project.report.wizard'
    _description = 'Project Report Wizard'

    project_ids = fields.Many2many('project.project', string='Projects')

    def generate_excel(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Projects')

        # Escribir los encabezados
        worksheet.write(0, 0, 'Project Name')

        # Escribir los nombres de los proyectos
        for i, project in enumerate(self.project_ids, start=1):
            worksheet.write(i, 0, project.name)

        workbook.close()
        output.seek(0)
        excel_file = base64.b64encode(output.read())
        output.close()

        # Crear un registro de archivo adjunto
        attachment = self.env['ir.attachment'].create({
            'name': 'Projects_Report.xlsx',
            'type': 'binary',
            'datas': excel_file,
            'res_model': 'project.project',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }
from odoo import models, fields
import io
import xlsxwriter
import base64

class Project(models.Model):
    _inherit = 'project.project'
    _description = 'Project'

    name = fields.Char(string='Project Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    project_manager_id = fields.Many2one('hr.employee', string='Project Manager')
    employee_ids = fields.Many2many('hr.employee', string='Employees')
    client_id = fields.Many2one('res.partner', string='Client')
    task_ids = fields.One2many('project.task', 'project_id', string='Task')

    def get_projects_in_date_range(self, start_date, end_date):
        return self.search([
            ('end_date', '>=', start_date),
            ('end_date', '<=', end_date)
        ])


    def test_button_action(self):
        """Método de prueba para el botón en el listado"""
        return True
    def action_generate_excel(self):
        if not self:
            return {
                'warning': {
                    'title': 'Advertencia',
                    'message': 'No hay proyectos seleccionados.',
                }
            }

        # Generar el informe para todos los proyectos seleccionados
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet("Proyectos")

        # Agregar encabezados
        headers = ['Project Name', 'Start Date', 'End Date', 'Project Manager']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        # Agregar datos
        row = 1
        for project in self:
            sheet.write(row, 0, project.name)
            sheet.write(row, 1, str(project.start_date) if project.start_date else "")
            sheet.write(row, 2, str(project.end_date) if project.end_date else "")
            sheet.write(row, 3, project.project_manager_id.name if project.project_manager_id else "")
            row += 1

        workbook.close()
        output.seek(0)

        # Crear un archivo adjunto para descargar
        attachment = self.env['ir.attachment'].create({
            'name': 'Reporte_Proyectos.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.getvalue()),
            'mimetype': 'application/vnd.ms-excel',
            'res_model': 'project.project',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
    def generate_excel_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet("Proyectos")

        # Agregar encabezados
        headers = ['Project Name', 'Start Date', 'End Date', 'Project Manager']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        # Agregar datos
        row = 1
        for project in self:
            sheet.write(row, 0, project.name)
            sheet.write(row, 1, str(project.start_date) if project.start_date else "")
            sheet.write(row, 2, str(project.end_date) if project.end_date else "")
            sheet.write(row, 3, project.project_manager_id.name if project.project_manager_id else "")
            row += 1

        workbook.close()
        output.seek(0)

        # Guardar archivo en campo binario
        self.write({
            'report_file': base64.b64encode(output.getvalue()),
            'report_file_name': 'Reporte_Proyectos.xlsx'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content/{self.id}?model=project.project&field=report_file&download=true&filename={self.report_file_name}",
            'target': 'self',
        }

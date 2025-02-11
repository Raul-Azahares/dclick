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
    report_file = fields.Binary(string='Archivo de Reporte')
    report_file_name = fields.Char(string='Nombre del Archivo')


    def action_generate_excel(self):
        # Crear un objeto en memoria para escribir el archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Obtener los proyectos seleccionados
        projects = self.env['project.project'].browse(self.env.context.get('active_ids', []))

        # Iterar sobre cada proyecto y crear una hoja por proyecto
        for project in projects:
            # Crear una hoja para el proyecto (el nombre de la hoja es el nombre del proyecto)
            worksheet = workbook.add_worksheet(project.name[:31])  # Limitar a 31 caracteres (límite de Excel)

            # Definir encabezados para la hoja del proyecto
            headers = ['Employee Name', 'Role']
            row = 0
            col = 0

            # Escribir encabezados en la hoja
            for header in headers:
                worksheet.write(row, col, header)
                col += 1

            # Escribir datos de los empleados asignados al proyecto
            row = 1
            for employee in project.employee_ids:
                worksheet.write(row, 0, employee.name or '')
                worksheet.write(row, 1, employee.role or '')  # Mostrar el rol del empleado
                row += 1

        # Cerrar el libro y guardar los datos en el búfer
        workbook.close()

        # Preparar el archivo para descargar
        output.seek(0)
        attachment = self.env['ir.attachment'].create({
            'name': 'projects_employees_report.xlsx',
            'datas': base64.b64encode(output.read()),
            'mimetype': 'application/vnd.ms-excel'
        })

        # Generar el enlace para descargar el archivo
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

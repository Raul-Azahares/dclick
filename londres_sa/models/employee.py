from odoo import models, fields,_
import base64
import io
import csv


class Employee(models.Model):
    _inherit = 'hr.employee'

    role = fields.Selection([
        ('manager', 'Project Manager'),
        ('developer', 'Developer'),
    ], string='Role')
    project_manager_id = fields.Many2one('hr.employee', string='Project Manager')
    project_id = fields.Many2one('project.project', string='Assigned Project')

    def write(self, vals):
        res = super().write(vals)
        for emp in self:
            if emp.role == 'developer' and len(emp.project_ids) > 1:
                raise ValueError("A developer can only be assigned to one project.")
        return res

    def import_employees(self):
        if not self.excel_file:
            raise ValueError(_("Please upload a CSV file before importing."))

        try:
            # Decodificar el archivo CSV cargado
            content = base64.decodebytes(self.excel_file).decode('utf-8')
            input_stream = io.StringIO(content)

            # Leer el archivo CSV
            reader = csv.DictReader(input_stream)

            # Verificar que el archivo contenga las columnas requeridas
            required_columns = {'Name', 'Role', 'Project'}
            if not required_columns.issubset(reader.fieldnames):
                raise ValueError(_("The CSV file must contain the following columns: Name, Role, Project."))

            # Procesar cada fila del archivo
            for row in reader:
                name = row.get('Name', '').strip()
                role = row.get('Role', '').strip()
                project_name = row.get('Project', '').strip()

                # Buscar o crear el proyecto correspondiente
                project = self.env['project.project'].search([('name', '=', project_name)], limit=1)
                if not project:
                    project = self.env['project.project'].create({'name': project_name})

                # Crear o actualizar el empleado
                employee = self.env['hr.employee'].search([('name', '=', name)], limit=1)
                if employee:
                    employee.write({
                        'role': role,
                        'project_id': project.id
                    })
                else:
                    self.env['hr.employee'].create({
                        'name': name,
                        'role': role,
                        'project_id': project.id
                    })

            # Limpiar el campo del archivo después de la importación
            self.write({'excel_file': False, 'excel_file_name': False})

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Import Successful'),
                    'message': _('Employees have been successfully imported.'),
                    'type': 'success',
                    'sticky': False,
                }
            }

        except Exception as e:
            raise ValueError(_("Error during import: %s") % str(e))
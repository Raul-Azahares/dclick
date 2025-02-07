from odoo import http
from odoo.http import request
import pandas as pd

class EmployeeImportController(http.Controller):

    @http.route('/import/employees', type='http', auth='user', methods=['POST'], csrf=False)
    def import_employees(self, file=None):
        if not file:
            return "No se ha proporcionado ningún archivo."

        try:
            df = pd.read_excel(file)
            for index, row in df.iterrows():
                employee_data = {
                    'name': row['Name'],
                    'role': row['Role'],
                    'project_manager_id': row['Project Manager'] if 'Project Manager' in row else None,
                }
                request.env['hr.employee'].create(employee_data)

            return "Employees successfully imported."
        except Exception as e:
            return f"Error importing employees: {str(e)}"
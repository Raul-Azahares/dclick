from odoo import models, fields

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

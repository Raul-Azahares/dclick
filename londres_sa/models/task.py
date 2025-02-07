from odoo import models, fields

class Task(models.Model):
    _inherit = 'project.task'
    _description = 'Task'

    name = fields.Char(string='Task Name', required=True)
    description = fields.Text(string='Description')
    project_id = fields.Many2one('project.project', string='Project')
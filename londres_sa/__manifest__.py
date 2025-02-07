{
    'name': 'Project Management London S.A.',
    'version': '1.0',
    'summary': 'Module to manage projects, employees and clients',
    'description': 'Customized module for project, employee and client management in London S.A.',
    'author': 'by Raul Azahares',
    'depends': ['project','hr', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/project_views.xml',
        'views/client_views.xml',
        'views/task_views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
}
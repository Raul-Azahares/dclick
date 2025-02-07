class ProjectDateRangeController(http.Controller):

    @http.route('/projects/in_date_range', type='json', auth='user', methods=['POST'], csrf=False)
    def get_projects_in_date_range(self, start_date, end_date):
        projects = request.env['project.project'].get_projects_in_date_range(start_date, end_date)
        return projects.read(['name', 'start_date', 'end_date'])
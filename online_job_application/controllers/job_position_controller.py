from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class JobPositionController(http.Controller):
    """
    Controller for displaying published job positions on the website.
    """

    @http.route('/job_positions', type='http', auth='public', website=True)
    def job_positions(self, **kwargs):
        """
        Renders a page displaying all published job positions.

        :param kwargs: Additional parameters passed in the request.
        :return: Rendered HTML page with job positions.
        """
        try:
            _logger.info("Fetching published job positions for display.")

            # Fetch all published job positions
            job_positions = request.env['job.posi1tion'].sudo().search([('is_published', '=', True)])

            if not job_positions:
                _logger.warning("No published job positions found.")
            else:
                _logger.debug(f"Found {len(job_positions)} published job positions.")

            # Render the page with job positions
            return request.render('online_job_application.job_positions_page', {
                'job_positions': job_positions
            })

        except Exception as e:
            _logger.exception(f"An error occurred while fetching job positions: {e}")
            return request.render('website.404', {
                'error_message': "An unexpected error occurred while loading job positions."
            })

from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class DashboardController(http.Controller):

    @http.route('/dashboard_data', type='json', auth='user')
    def get_dashboard_data(self, **kwargs):
        """
            JSON route to fetch dashboard data.

            This route aggregates data about job positions and applications to be displayed
            on a dashboard. It computes statistics like the total number of candidates,
            total jobs, published/unpublished jobs, and application counts by state.

            :param kwargs: Additional parameters passed via the request.
            :return: JSON object containing aggregated dashboard data.
        """
        try:
            _logger.info("Fetching dashboard data...")
            total_candidates = request.env["job.application"].search_count([])
            total_jobs = request.env["job.position"].search_count([])
            published_jobs = request.env["job.position"].search_count([("is_published", "=", True)])
            unpublished_jobs = request.env["job.position"].search_count([("is_published", "=", False)])

            job_position_table = []
            for job_position in request.env["job.position"].search([]):
                total_applications = request.env["job.application"].search_count(
                    [("job_position_id", "=", job_position.id)])
                received_applications = request.env["job.application"].search_count(
                    [("job_position_id", "=", job_position.id), ("state", "=", "received")])
                in_review_applications = request.env["job.application"].search_count(
                    [("job_position_id", "=", job_position.id), ("state", "=", "in_review")])
                interview_applications = request.env["job.application"].search_count(
                    [("job_position_id", "=", job_position.id), ("state", "=", "interview")])
                accepted_applications = request.env["job.application"].search_count(
                    [("job_position_id", "=", job_position.id), ("state", "=", "accepted")])
                rejected_applications = request.env["job.application"].search_count(
                    [("job_position_id", "=", job_position.id), ("state", "=", "rejected")])
                job_position_table.append({
                    "position_id": job_position.id,
                    "position_name": job_position.name,
                    "total_applications": total_applications,
                    "received_applications": received_applications,
                    "in_review_applications": in_review_applications,
                    "interview_applications": interview_applications,
                    "accepted_applications": accepted_applications,
                    "rejected_applications": rejected_applications,
                })

            _logger.debug(f"Job position data: {job_position_table}")
            return {
                "total_candidates": total_candidates,
                "total_jobs": total_jobs,
                "published_jobs": published_jobs,
                "unpublished_jobs": unpublished_jobs,
                "job_position_table": job_position_table,
            }

        except Exception as e:
            _logger.error(f"An error occurred while fetching dashboard data: {e}")
            return {"error": str(e)}

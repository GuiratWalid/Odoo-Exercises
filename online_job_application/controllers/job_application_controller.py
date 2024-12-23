import base64
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class JobApplicationController(http.Controller):
    """
    Controller for handling job applications via the website.
    Provides routes for displaying the application form and submitting applications.
    """

    @http.route('/apply/<int:job_position_id>', type='http', auth='public', website=True, csrf=True)
    def application_form(self, job_position_id, **kw):
        """
        Renders the application form for a specific job position.

        :param job_position_id: ID of the job position.
        :param kw: Additional parameters passed in the request.
        :return: Rendered application form or a 404 page if the job position does not exist.
        """
        _logger.info(f"Fetching job application form for position ID: {job_position_id}")

        # Fetch the job position
        job_position = request.env['job.position'].sudo().browse(job_position_id)
        if not job_position.exists():
            _logger.warning(f"Job position with ID {job_position_id} does not exist.")
            return request.render('website.404')

        _logger.debug(f"Job position found: {job_position.name}")
        return request.render('online_job_application.job_application_form', {
            'job_position': job_position,
        })

    @http.route('/submit_application', type='http', auth='public', website=True, csrf=True)
    def submit_application(self, **kwargs):
        """
        Handles the submission of a job application form.

        :param kwargs: Form data submitted by the user.
        :return: Success page if application is created successfully, or 404 page if an error occurs.
        """
        try:
            _logger.info("Processing job application submission.")

            # Check if the user has already applied for this job position
            application_exists = request.env['job.application'].sudo().search([('email', '=', kwargs.get('email'))])
            if application_exists:
                _logger.error(f"This candidate has already applied for this position.")
                return request.render('website.404', {'error': "You have already applied for this position."})

            # Get the resume file from the form
            resume_file = kwargs.get('resume')
            if not resume_file:
                _logger.error("Resume file is missing in the application submission.")
                return request.render('website.404', {'error': "Resume file is required."})

            # Read and encode the resume file
            resume_data = resume_file.read()
            encoded_resume = base64.b64encode(resume_data).decode('utf-8')
            resume_filename = resume_file.filename

            # Fetch the job position
            job_position_id = kwargs.get('job_position_id')
            job_position = request.env['job.position'].sudo().browse(int(job_position_id))

            if not job_position.exists():
                _logger.error(f"Job position with ID {job_position_id} does not exist.")
                return request.render('website.404')

            _logger.debug(f"Job position found: {job_position.name}. Creating application...")

            # Create the job application
            application = request.env['job.application'].sudo().create({
                'name': kwargs.get('name'),
                'job_position_id': job_position.id,
                'email': kwargs.get('email'),
                'phone': kwargs.get('phone'),
                'resume': encoded_resume,
                'resume_filename': resume_filename,
                'cover_letter': kwargs.get('cover_letter'),
            })

            # Check if the application was created successfully
            if application and application.reference:
                _logger.info(f"Application successfully created with reference: {application.reference}")
                return request.render('online_job_application.job_application_success', {
                    'reference': application.reference
                })
            else:
                _logger.error("Failed to create the application.")
                return request.render('website.404', {'error': "Failed to submit the application."})

        except Exception as e:
            _logger.exception(f"An error occurred while submitting the application: {e}")
            return request.render('website.404', {'error': "An unexpected error occurred."})

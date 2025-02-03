{
    'name': 'Weather',
    'version': '18.0.1.0.0',
    'author': 'Walid Guirat',
    'category': 'Services/Weather',
    'summary': 'Provides real-time weather data and forecasts within Odoo.',
    'description': ' ',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/ir_sequence_data.xml',

        'wizard/res_config_settings_views.xml',
        'wizard/generate_daily_forecast_wizard.xml',

        'views/weather_daily_forecast_views.xml',
        'views/weather_location_views.xml',
        'views/weather_alert_views.xml',

        'report/weather_alert_report_template.xml',
        'report/weather_alert_report.xml',

        'data/mail_template_data.xml',
        'data/ir_cron_data.xml',

        'views/weather_menus.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

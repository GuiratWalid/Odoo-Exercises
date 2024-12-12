{
    'name': 'Weather',
    'version': '18.0.1.0.0',
    'author': 'Walid Guirat',
    'category': 'Services/Weather',
    'summary': 'Provides real-time weather data and forecasts within Odoo.',
    'description': ' ',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'wizard/res_config_settings_views.xml',
        'wizard/get_weather_forecast.xml',

        'views/weather_daily_forecast_views.xml',
        'views/weather_location_views.xml',
        'views/weather_menus.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

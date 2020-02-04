"""

"""

import logging

from logging.config import dictConfig

LOGGING_CONFIG = dict(
    version = 1,
    formatters = {
        'verbose': {'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'},
        'simple': {'format': '%(levelname)s %(message)s'}
    },

    handlers = {
        'console': {'class': 'logging.StreamHandler',
                    'level': logging.INFO,
                    'formatter': 'simple',},
        'file': {'class':'logging.FileHandler',
                 'level': logging.DEBUG,
                 'formatter': 'verbose',
                 'filename': 'Parser.log'}
    },

    root = {
        'handlers': ['console', 'file'],
        'level': logging.DEBUG,
    },
)


def setup_logs(verbose=False):
    """ Setup logs for all modules

    verbose (boolean): If True debug message will be displayed on the console
    """

    if verbose:
        LOGGING_CONFIG['handlers']['console']['level'] = logging.DEBUG

    dictConfig(LOGGING_CONFIG)

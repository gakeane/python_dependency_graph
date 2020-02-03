"""

"""

import logging

log = logging.getLogger(__name__)


def setup_logs(verbose=False):
    """ Setup logs for all modules """

    if verbose:
        log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_path + 'Parser.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    return log

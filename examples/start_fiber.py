import logging
from time import sleep

from pynta.model.experiment.dispertech.fiber_tracking import FiberTracking
from pynta.util.log import get_logger, log_to_screen


logger = get_logger(level=logging.DEBUG)
ch = log_to_screen(level=logging.DEBUG)
logger.addHandler(ch)


if __name__ == '__main__':
    with FiberTracking('config/dispertech.yml') as exp:
        while exp.initializing:
            logger.debug('Still initializing')
            sleep(0.1)
        exp.finalize()

import importlib

from pynta.util import get_logger

logger = get_logger(name=__name__)


def load_camera_module(name):
    try:
        logger.info('Importing camera model {}'.format(name))
        logger.debug('pynta.model.cameras.' + name)
        camera_model_to_import = 'pynta.model.cameras.' + name
        cam_module = importlib.import_module(camera_model_to_import)
    except ModuleNotFoundError:
        logger.error('The model {} for the camera was not found'.format(name))
        raise
    return cam_module
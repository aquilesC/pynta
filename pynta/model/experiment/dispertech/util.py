# -*- coding: utf-8 -*-
"""
    Utility functions for fiber tracking
    ====================================
    Collection of functions that can be reused in other parts of the code. They focus mostly on the work with different
    modules, importing and instantiating them.

    :copyright:  Aquiles Carattino <aquiles@uetke.com>
    :license: GPLv3, see LICENSE for more details
"""

import importlib

from pynta.util import get_logger

logger = get_logger(name=__name__)


def load_camera_module(name: str):
    """Helper function to load the module of the camera based solely on the name.

    .. TODO:: This function is able to import only models from within Pynta. A more flexible approach is desirable.

    :param name: Name of the class to import. Should be a Python file within pynta.model.cameras
    :return: Module to be used
    """
    try:
        logger.info(f'Importing camera model {name}')
        logger.debug('pynta.model.cameras.' + name)
        camera_model_to_import = 'pynta.model.cameras.' + name
        cam_module = importlib.import_module(camera_model_to_import)
    except ModuleNotFoundError:
        logger.error(f'The model {name} for the camera was not found')
        raise
    return cam_module


def instantiate_camera(config: dict):
    """ Imports the camera model specified in config['model'] and instantiates it with the arguments specified in
    config['init'] and (optionally) config['extra_args'].

    :param dict config: configuration dictionary. Most likely imported directly from a yaml file.
    :return: instantiated camera model
    """
    cam_module = load_camera_module(config['model'])
    cam_init_arguments = config['init']
    if 'extra_args' in config:
        logger.info('Initializing camera with extra arguments')
        logger.debug('cam_module.Camera({}, {})'.format(cam_init_arguments, config['extra_args']))
        camera = cam_module.Camera(cam_init_arguments, **config['extra_args'])
    else:
        logger.info('Initializing camera without extra arguments')
        logger.debug('cam_module.camera({})'.format(cam_init_arguments))
        camera = cam_module.Camera(cam_init_arguments)

    return camera


def load_motor_module(name):
    """ Loads the motor model based on the name of the Python file.
    .. TODO:: Make it more flexible to load modules from outside of Pynta

    :return: Motor model module
    """
    try:
        logger.info(f'Importing motor model {name}')
        motor_module_to_import = 'pynta.model.motors.' + name
        motor_module = importlib.import_module(motor_module_to_import)
    except ModuleNotFoundError:
        logger.error(f'The model {name} for the motor was not found')
        raise
    return motor_module


def instantiate_motor(config: dict):
    """ Imports the motor model specified in config['model'] and instantiates it with the arguments specified in
    config['init'] and (optionally) config['extra_args'].

    :param dict config: configuration dictionary. Most likely imported directly from a yaml file.
    :return: instantiated motor model
    """
    motor_module = load_camera_module(config['model'])
    motor_init_arguments = config['init']
    if 'extra_args' in config:
        logger.info('Initializing motor with extra arguments')
        logger.debug(f'motor_module.Motor({motor_init_arguments}, {config["extra_args"]})')
        motor = motor_module.Motor(motor_init_arguments, **config['extra_args'])
    else:
        logger.info('Initializing motor without extra arguments')
        logger.debug(f'motor_module.Motor({motor_init_arguments})')
        motor = motor_module.Motor(motor_init_arguments)
    return motor

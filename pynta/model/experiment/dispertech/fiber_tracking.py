# -*- coding: utf-8 -*-
"""
    Tracking in Hollow Optical Fibers
    =================================

    This experiment is very similar to the nanoparticle tracking experiment, but everything happens inside a hollow
    optical fiber. Some steps are different; for example, the user first has to focus the image of the camera on the
    top part of the setup in order to couple the laser to the optical fiber. Then, the user needs to maximise the
    background signal on the microscope's camera in order to fine-tune the coupling.

    The measurement is essentially a 1-D measurement of diffusion, in which equations need to be adapted for including
    diffusion in a cylinder.

    :copyright:  Aquiles Carattino <aquiles@uetke.com>
    :license: GPLv3, see LICENSE for more details
"""
import importlib

from pynta.model.experiment.base_experiment import BaseExperiment
from pynta.model.experiment.dispertech.util import load_camera_module
from pynta.util import get_logger


logger = get_logger(name=__name__)


class FiberTracking(BaseExperiment):
    """ Experiment class for performing nanoparticle tracking analysis inside a hollow optical fiber.
    """
    SINGLE_SNAP_BKG = 0
    ROLLING_AVERAGE = 1

    BACKGROUND_CORRECTION = (
        ('single_snap', SINGLE_SNAP_BKG),
        ('rolling_avg', ROLLING_AVERAGE)
    )

    def __init__(self, filename=None):
        super().__init__(filename)
        self.cameras = {
            'fiber': None,
            'microscope': None
        }

    def initialize_cameras(self):
        """ The experiment requires two cameras, and they need to be initialized before we can proceed with the
        measurement.
        """

        cam_module = load_camera_module(self.config['camera_fiber']['model'])
        cam_init_arguments = self.config['camera_fiber']['init']

        if 'extra_args' in self.config['camera_fiber']:
            logger.info('Initializing camera with extra arguments')
            logger.debug('cam_module.camera({}, {})'.format(cam_init_arguments, self.config['camera']['extra_args']))
            self.cameras['fiber'] = cam_module.Camera(cam_init_arguments, *self.config['camera_fiber']['extra_args'])
        else:
            logger.info('Initializing camera without extra arguments')
            logger.debug('cam_module.camera({})'.format(cam_init_arguments))
            self.cameras['fiber'] = cam_module.Camera(cam_init_arguments)

        self.camera.initialize()
        self.current_width, self.current_height = self.camera.getSize()
        logger.info('Camera sensor ROI: {}px X {}px'.format(self.current_width, self.current_height))
        self.max_width = self.camera.GetCCDWidth()
        self.max_height = self.camera.GetCCDHeight()
        logger.info('Camera sensor size: {}px X {}px'.format(self.max_width, self.max_height))

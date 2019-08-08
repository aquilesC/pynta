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
import sqlite3
from pathlib import Path
from threading import Thread

from pynta.model.experiment.base_experiment import BaseExperiment
from pynta.model.experiment.dispertech.util import load_camera_module, instantiate_camera
from pynta.util import get_logger


logger = get_logger(name=__name__)


class FiberTracking(BaseExperiment):
    """ Experiment class for performing nanoparticle tracking analysis inside a hollow optical fiber.
    """
    SINGLE_SNAP_BKG = 0
    """Uses only one image to correct the background"""

    ROLLING_AVERAGE = 1
    """Uses a window of averages to correct the background"""

    BACKGROUND_CORRECTION = (
        ('single_snap', SINGLE_SNAP_BKG),
        ('rolling_avg', ROLLING_AVERAGE)
    )

    def __init__(self, filename=None):
        super().__init__(filename)
        self.camera = None

    def initialize_camera(self):
        """ The experiment requires two cameras, and they need to be initialized before we can proceed with the
        measurement. This requires two entries in the config file with names ``camera_fiber``, which refers to the
        camera which monitors the end of the fiber and ``camera_microscope``, which is the one that is used to do the
        real measurement.

        """
        self.camera = instantiate_camera(config=self.config['camera_microscope'])
        logger.info(f'Initializing {self.camera}')
        self.camera.initialize()

    def initialize_electronics(self):
        """ Routine to initialize the rest of the electronics. For example, the LED's can be set to a default on/off
        state. This is also used to measure the temperature.
        """
        logger.info('Initializing electronics')

    def set_up(self):
        """ Initializes all the devices at the same time using threads.
        """
        self.initialize_threads = [
            Thread(target=self.initialize_camera),
            Thread(target=self.initialize_electronics),
        ]
        for thread in self.initialize_threads:
            thread.start()

    def finalize(self):
        logger.info(f'Finalizing The Experiment {self}')

    def __str__(self):
        return "Nanopartilce Tracking Experiment"



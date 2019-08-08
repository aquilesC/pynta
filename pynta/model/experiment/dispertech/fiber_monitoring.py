# -*- coding: utf-8 -*-
"""
    Monitoring the fiber end
    ========================
    This experiment is aimed at monitoring the end of the fiber in order to monitor the laser coupling to it. In
    principle is possible to think about routines which are able to auto-focus on the fiber end through some pattern
    recognition and algorithmic development.

    :copyright:  Aquiles Carattino <aquiles@uetke.com>
    :license: GPLv3, see LICENSE for more details
"""
from threading import Thread

from pynta.model.experiment.base_experiment import BaseExperiment
from pynta.model.experiment.dispertech.util import instantiate_camera, instantiate_motor
from pynta.util import get_logger


logger = get_logger(name=__name__)


class FiberMonitoring(BaseExperiment):
    def __init__(self, filename=None):
        logger.info('Starting Fiber Monitoring Experiment')
        super().__init__(filename)
        self.camera = None
        self.motor = None

    def initialize_camera(self):
        """Initializes the camera that will be used to monitor the end of the fiber."""
        logger.info(f'Initializing camera {self.config["camera_fiber"]["model"]}')
        self.camera = instantiate_camera(config=self.config['camera_fiber'])
        self.camera.initialize()

    def initialize_mirror(self):
        """ Routine to initialize the movable mirror. The steps in this method should be those needed for having the
        mirror in a known position (i.e. the homing procedure).
        """
        logger.info(f'Initializing mirror {self.config["mirror"]["model"]}')
        self.motor = instantiate_motor(config=self.config['motor'])
        self.motor.initialize()

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
            Thread(target=self.initialize_mirror),
        ]
        for thread in self.initialize_threads:
            thread.start()



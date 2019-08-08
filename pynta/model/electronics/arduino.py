"""
    Arduino Model
    =============
    This is an ad-hoc model for controlling an Arduino Due board, which will in turn control a piezo-mirror, a laser,
    and some LED's.
"""
from pynta.controller.devices.arduino.arduino import Arduino
from pynta.util import get_logger

logger = get_logger(__name__)


class ArduinoModel:
    def __init__(self, port):
        self.driver = Arduino(port)


    def move_mirror(self, speed: int, direction: int, axis: int):
        """ Moves the mirror connected to the board

        :param int speed: Speed, from 0 to 2^6.
        :param direction: 0 or 1, depending on which direction to move the mirror
        :param axis: 0 or 1, to select the axis
        """

        binary_speed = '{0:06b}'.format(speed)
        binary_speed = str(direction) + str(1) + binary_speed
        number = int(binary_speed, 2)
        bytestring = number.to_bytes(1, 'big')
        logger.info(f'Moving mirror bits: {binary_speed[::-1]}')
        self.driver.query(bytestring)

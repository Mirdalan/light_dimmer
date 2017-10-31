import sys
import signal
from time import sleep

from RPi import GPIO
import zmq

import configuration
from logger_configuration import configure_logger


# ---------------- INITIATING LOGGER ---------------
logger = configure_logger()
logger.debug("Initializing service...")


def zmq_data_receive():
    """
    Simple method to wait for incoming data.
    :return: Received data. Expecting a dict object.
    """
    context = zmq.Context()
    server = context.socket(zmq.REP)
    server.bind(configuration.transfer_protocol)
    return server.recv_pyobj()


class Dimmer:
    """
    Single dimmer object allowing to control the dimmer features.
    """
    def __init__(self, pin_number, frequency=30, duty_cycle=0, name=''):
        """
        Initializing a single Dimmer object with given or default parameters:
        :param pin_number: Raspberry PI GPIO channel according to GPIO.setmode
        :param duty_cycle: PWM duty cycle
        :param frequency: PWM frequency
        """
        self.name = name
        logger.debug("Initiating dimmer %s." % self.name)
        GPIO.setup(pin_number, GPIO.OUT)
        self.pwm = GPIO.PWM(pin_number, frequency)
        self.pwm.start(duty_cycle)
        self.pin_number = pin_number
        self.duty_cycle = duty_cycle

    def set_duty_cycle(self, duty_cycle):
        """ sets a given duty cycle """
        self.duty_cycle = duty_cycle
        self.pwm.ChangeDutyCycle(duty_cycle)

    def shutdown(self):
        """ Cleans RPi GPIO configuration for this dimmer GPIO channel """
        logger.debug("Shutting down dimmer %s." % self.name)
        GPIO.cleanup(self.pin_number)


class DimmersController:
    """
    Object controlling a group of dimmers.
    """
    def __init__(self):
        """
        Initializes the GPIO by setting its mode.
        Initializes a dict of dimmers.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.dimmers = {}
        for room, args in configuration.dimmers.items():
            self.dimmers[room] = Dimmer(*args, name=room)

    def set(self, requested_levels):
        """ Sets duty cycles according to requested light levels """
        for room, level in requested_levels.items():
            logger.debug("Setting duty cycle for %s dimmer to %f." % (room, level))
            self.dimmers[room].set_duty_cycle(level)

    def any_of_dimmers_not_set(self, requested_levels):
        return any([requested_levels[room] != self.dimmers[room].duty_cycle for room in requested_levels.keys()])

    def soft_set(self, requested_levels):
        """
         Sets duty cycles according to requested light levels in fade mode..
        """
        for room, level in requested_levels.items():
            logger.debug("Setting duty cycle for %s dimmer to %f." % (room, level))
        while self.any_of_dimmers_not_set(requested_levels):
            for room, level in requested_levels.items():
                dimmer = self.dimmers[room]
                if dimmer.duty_cycle < level:
                    dimmer.set_duty_cycle(dimmer.duty_cycle + 1)
                if dimmer.duty_cycle > level:
                    dimmer.set_duty_cycle(dimmer.duty_cycle - 1)
                sleep(configuration.fade_sleep_time)
        for room, level in requested_levels.items():
            logger.debug("Finished setting duty cycle for %s dimmer to %f." % (room, level))

    def systemd_shutdown(self, signum, frame):
        """
        Shuts down whole service. Runs the object 'shutdown()' method to do it.
        Executed by SIGTERM signal which is sent by 'systemctl stop dimmers_control' command.
        :param signum, frame: required by signal but not used.
        """
        logger.debug("Received SIGTERM. Turning out the light...")
        self.soft_set(configuration.dimmers_off)
        self.shutdown()

    def shutdown(self):
        """ Shuts down whole service. """
        logger.debug("Shutting down...")
        for dimmer in self.dimmers.values():
            dimmer.shutdown()
        logger.debug("Bye.")
        sys.exit(0)


if __name__ == '__main__':
    dimmers_control = DimmersController()
    signal.signal(signal.SIGTERM, dimmers_control.systemd_shutdown)

    logger.debug("Initialized. Starting main loop.")
    while True:
        try:
            logger.debug("Waiting for control request.")
            control_data = zmq_data_receive()
            logger.debug("Received a data set. Executing control method.")
            if control_data['method'] == 'soft':
                dimmers_control.soft_set(control_data['requested_levels'])
            else:
                dimmers_control.set(control_data['requested_levels'])
        except KeyboardInterrupt as e:
            logger.error(repr(e))
            dimmers_control.shutdown()
            break
        except Exception as e:
            logger.error(e.__class__.__name__ + " in line " + str(e.__traceback__.tb_lineno) + ": " + str(e))
            sleep(0.1)

import signal
import sys
from time import sleep

import zmq

import configuration
from logger_configuration import configure_logger

import wiringpi

# ---------------- INITIATING LOGGER ---------------
logger = configure_logger()
logger.debug("Initializing service...")


# ---------------- WAIT FOR REQUEST FUNCTION ---------------
def get_control_data():
    zmq_socket = zmq.Context().socket(zmq.REP)
    zmq_socket.bind(configuration.transfer_protocol)
    return zmq_socket.recv_pyobj()


class Dimmer:
    """
    Single dimmer object allowing to control the dimmer features.
    """
    def __init__(self, pin_number, frequency_divisor, duty_cycle=0, name=''):
        """
        Initializing a single Dimmer object with given or default parameters:
        :param pin_number: Raspberry PI GPIO channel according to wiringPiSetup...
        :param duty_cycle: PWM duty cycle
        """
        self.name = name
        logger.debug("Initiating dimmer %s." % self.name)
        wiringpi.pinMode(pin_number, wiringpi.PWM_OUTPUT)
        wiringpi.pwmSetClock(frequency_divisor)
        self.pin_number = pin_number
        self.duty_cycle = duty_cycle

    def set_duty_cycle(self, duty_cycle):
        """ sets a given duty cycle """
        wiringpi.pwmWrite(self.pin_number, duty_cycle)
        self.duty_cycle = duty_cycle

    def increment_or_skip_limit(self, requested_duty_cycle):
        """ increments duty cycle or skips to end if in range of no visible effect values """
        if self.duty_cycle > configuration.duty_high_limit:
            self.set_duty_cycle(requested_duty_cycle)
        else:
            self.set_duty_cycle(self.duty_cycle + 1)

    def decrement_or_hit_limit(self):
        """ decrements duty cycle or skips to end of range of no visible effect values """
        if self.duty_cycle > configuration.duty_high_limit:
            self.set_duty_cycle(configuration.duty_high_limit)
        else:
            self.set_duty_cycle(self.duty_cycle - 1)

    def set_duty_cycle_one_step_towards_level(self, requested_duty_cycle):
        """ decides if duty cycle needs to be incremented or decremented """
        if self.duty_cycle < requested_duty_cycle:
            self.increment_or_skip_limit(requested_duty_cycle)
        if self.duty_cycle > requested_duty_cycle:
            self.decrement_or_hit_limit()

    def shutdown(self):
        """ Cleans GPIO configuration for this dimmer GPIO channel """
        logger.debug("Shutting down dimmer %s." % self.name)
        wiringpi.pinMode(self.pin_number, wiringpi.INPUT)


class DimmersController:
    """
    Object controlling a group of dimmers.
    """
    def __init__(self):
        """
        Initializes the GPIO by setting its mode.
        Initializes a dict of dimmers.
        """
        wiringpi.wiringPiSetupGpio()
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
                dimmer.set_duty_cycle_one_step_towards_level(level)
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
    logger.debug("Initiating dimmer instances.")
    dimmers_control = DimmersController()
    logger.debug("Configuring SIGTERM signal handler.")
    signal.signal(signal.SIGTERM, dimmers_control.systemd_shutdown)

    logger.debug("Initialized. Starting main loop.")
    while True:
        try:
            logger.debug("Waiting for control request.")
            control_data = get_control_data()
            logger.debug("Received a data set. Executing control method.")
            dimmers_control.soft_set(control_data)

        except KeyboardInterrupt as e:
            logger.error(repr(e))
            dimmers_control.shutdown()
            break

        except Exception as e:
            logger.error(e.__class__.__name__ + " in line " + str(e.__traceback__.tb_lineno) + ": " + str(e))
            sleep(0.1)

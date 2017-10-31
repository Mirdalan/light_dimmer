import logging
import sys
import signal
#TODO: configuration in seperate file
#TODO: debug possible client communication problem?
logger = logging.getLogger('Dimmer control daemon')
logger.setLevel(logging.ERROR)
fh = logging.FileHandler('dimmer_control.log')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.debug("Initializing service...")

try:
    from RPi import GPIO
except RuntimeError:
    logging.critical("Could not import RPi.GPIO. Probably didn't have privileges.")
    sys.exit(1)
try:
    import zmq
except RuntimeError:
    logging.critical("Could not import zmq. Probably not installed or using wrong Python interpreter / virtualenv. "
                     "Try installing it: pip3 install zmq")
    sys.exit(1)


def zmq_data_receive():
    """
    Simple method to wait for incoming data.
    :return: Received data. Expecting a dict object.
    """
    context = zmq.Context()
    server = context.socket(zmq.REP)
    server.bind("ipc://pwm_duty_cycles")
    return server.recv_pyobj()


class Dimmer:
    """
    Single dimmer object allowing to control the dimmer features.
    """
    def __init__(self, pin_number=33, duty_cycle=0, frequency=300):
        """
        Initializing a single Dimmer object with given or default parameters:
        :param pin_number: Raspberry PI GPIO channel according to GPIO.setmode
        :param duty_cycle: PWM duty cycle
        :param frequency: PWM frequency
        """
        GPIO.setup(pin_number, GPIO.OUT)
        self.pwm = GPIO.PWM(pin_number, frequency)
        self.pwm.start(duty_cycle)
        self.pin_number = pin_number

    def set_duty_cycle(self, duty_cycle):
        """ sets a given duty cycle """
        self.pwm.ChangeDutyCycle(duty_cycle)

    def shutdown(self):
        """ Cleans RPi GPIO configuration for this dimmer GPIO channel """
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
        self.dimmers = {
            "bedroom": Dimmer(33),
            "small_room": Dimmer(35),
        }

    def set(self, requested_levels):
        for room, level in requested_levels.items():
            logger.debug("Setting duty cycle for %s dimmer to %f." % (room, level))
            self.dimmers[room].set_duty_cycle(level)

    @staticmethod
    def shutdown(signum, frame):
        logger.debug("Shutting down...")
        GPIO.cleanup()
        sys.exit(0)


if __name__ == '__main__':
    dimmers_control = DimmersController()
    signal.signal(signal.SIGTERM, dimmers_control.shutdown)

    logger.debug("Initialized. Starting loop.")
    while True:
        try:
            requested_light_levels = zmq_data_receive()
            logger.debug("Received a data set. Executing control method.")
            dimmers_control.set(requested_light_levels)
        except KeyboardInterrupt as e:
            logger.error(repr(e))
            dimmers_control.shutdown()
            break
        except Exception as e:
            logger.error(e.__class__.__name__ + " in line " + str(e.__traceback__.tb_lineno) + ": " + str(e))

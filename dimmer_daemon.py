from RPi import GPIO
import zmq


def zmq_data_receive():
    context = zmq.Context()
    subscriber = context.socket(zmq.REP)
    subscriber.bind("ipc://pwm_duty_cycles")
    return subscriber.recv_pyobj()


class Dimmer:
    def __init__(self, pin_number=33, duty_cycle=100, frequency=30000):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_number, GPIO.OUT)
        self.pwm = GPIO.PWM(pin_number, frequency)
        self.pwm.start(duty_cycle)
        self.pin_number = pin_number

    def set_duty_cycle(self, duty_cycle):
        self.pwm.ChangeDutyCycle(duty_cycle)

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup(self.pin_number)

    def shutdown(self):
        self.__del__()


if __name__ == '__main__':
    dimmers = {
    "sypialnia": Dimmer(33),
    "maly_pokoj": Dimmer(35),
    }
    print("Initialized. Starting loop.")
    while True:
        try:
            requested_light_levels = zmq_data_receive()
            for room in requested_light_levels.keys():
                dimmers[room].set_duty_cycle(requested_light_levels[room])
        except TypeError:
            print("WAT TypeError")
        except ValueError:
            print("WAT ValueError")
        except KeyboardInterrupt:
            print("\nShutting down...\n")
            for dimmer in dimmers.values():
                dimmer.shutdown()
            break

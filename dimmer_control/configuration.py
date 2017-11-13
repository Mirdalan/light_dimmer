import logging


# ----------------- LOGGER -----------------
log_file_name = "dimmer_control.log"
log_level = logging.DEBUG


# ------------------- ZMQ ------------------
transfer_protocol = "ipc://pwm_duty_cycles"


# ----------------- DAEMON -----------------
fade_sleep_time = 0.007
frequency_divisor = 1024
levels_tuple = (1024, 320, 280, 240, 200, 160, 120, 80, 40, 0)
duty_high_limit = levels_tuple[1]

rooms = ("Lampka",)
dimmers_setup = ((18, frequency_divisor),)
dimmers = dict(zip(rooms, dimmers_setup))
dimmers_off = dict(zip(rooms, (0, 0)))

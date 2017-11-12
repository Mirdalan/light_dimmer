import logging


# ----------------- LOGGER -----------------
log_file_name = "dimmer_control.log"
log_level = logging.DEBUG


# ------------------- ZMQ ------------------
transfer_protocol = "ipc://pwm_duty_cycles"


# ----------------- DAEMON -----------------
fade_sleep_time = 0.001

rooms = ("Lampka",)
dimmers_setup = (18,)
dimmers = dict(zip(rooms, dimmers_setup))
dimmers_off = dict(zip(rooms, (0, 0)))

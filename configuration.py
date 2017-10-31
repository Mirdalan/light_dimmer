import logging


# ----------------- LOGGER -----------------
log_file_name = "dimmer_control.log"
log_level = logging.DEBUG


# ------------------- ZMQ ------------------
transfer_protocol = "ipc://pwm_duty_cycles"


# ----------------- DAEMON -----------------
frequency = 300
dimmers = {
            "bedroom": (33, frequency),
            "small_room": (35, frequency),
}
dimmers_off = {
    "bedroom": 0.0,
    "small_room": 0.0,
}
fade_sleep_time = 0.01

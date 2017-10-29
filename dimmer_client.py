import zmq


def zmq_data_transmit(_data):
    context = zmq.Context()
    client = context.socket(zmq.REQ)
    client.connect("ipc://pwm_duty_cycles")
    client.send_pyobj(_data)


pwm_duty_cycles = {
    "sypialnia": 100,
    "maly_pokoj": 100,
}

while True:
    try:
        for room in pwm_duty_cycles.keys():
            pwm_duty_cycles[room] = float(input("Podaj wypelnienie dla pomieszczenia %s: " % room))
        zmq_data_transmit(pwm_duty_cycles)
        print("")
    except KeyboardInterrupt:
        print("\nShutting down...\n")
        break

import garageapp


filename = garageapp.process_cmdline_arguments()
config = garageapp.read_configuration(filename)

method = config["method"]
stateHardware = config["stateHardware"]
ip = config["ip"]
port = config["port"]
relayPin, sensorPin, statePin = config["relayPin"], config["sensorPin"], config["statePin"]

while True:
    garageapp.trigger_relay(relayPin)
    input()
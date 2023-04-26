# Pi Garage door opener project

Now uses mosquitto to transmit (not secure right now though)
need to configure the garageapp.py before using.

--Using flask and RPi GPIO pins.
The program works by taking a post request (json)
and then activates the switch in a garage door motor.
The status of the garage is obtained by using an ir sensor
but the ir sensor is not necessary if all you care about is
triggered by using the pi. This can be homekit compatible by
using it with the homebridge plugin HTTP-switch. Status can
also be passed through with that HTTP-switch if you are using
the ir sensor.--

## Future Features

- transmit status via mosquitto
- companion homebridge plugin
- better documentation

Circuit and connection diagrams coming soon.

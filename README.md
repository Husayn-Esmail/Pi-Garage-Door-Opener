# Pi Garage door opener project
Using flask and RPi GPIO pins.
The program works by taking a post request (json)
and then activates the switch in a garage door motor.
The status of the garage is obtained by using an ir sensor
but the ir sensor is not necessary if all you care about is
triggered by using the pi. This can be homekit compatible by 
using it with the homebridge plugin HTTP-switch. Status can
also be passed through with that HTTP-switch if you are using
the ir sensor. I've also set it up in a way such that if the
garage door is open for a certain amount of time, it can send
a text to notify you. again this feature is restricted to the
ir sensor version.


Circuit and connection diagrams coming soon.

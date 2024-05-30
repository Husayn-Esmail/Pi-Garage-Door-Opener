# Pi Garage door opener project

Now uses mosquitto to transmit (not secure right now though)
need to configure the garageapp.py before using.
This program was originally meant to be standalone and meant
to be called directly from the web. I used it like this for
about a year and a half until I decided to migrate the calls
over to mosquitto. This ended up being a much more secure solution
despite the mosquitto implementation being insecure.

I use Apple so I modified it for homekit integration.

The recommended way of using this project is as follows:

1. Get your hardware together
2. Connect to your garagedoor opener
3. Run instance of homebridge
4. Install the homebridge mqtt plugin
5. Add the device to apple home
6. Enjoy not having to open up a port and being able to open/close your garagedoor from anywhere

Please do not leave the user and password as the default admin admin combo.


## Configuration format

the following should be in your configuration file in this order.
replace [\*] with your configuration

[setTargetState\_topic]

[getTargetState\_topic]

[getCurrentState\_topic]

[ip]

[port]

example:

home/mysettarget

home/mygettarget

home/mycurrentstate

192.168.1.89

1883


## The old way
--Using flask and RPi GPIO pins.
The program works by taking a post request (json)
and then activates the switch in a garage door motor.
The status of the garage is obtained by using an ir sensor
but the ir sensor is not necessary if all you care about is
triggered by using the pi. This can be homekit compatible by
using it with the homebridge plugin HTTP-switch. Status can
also be passed through with that HTTP-switch if you are using
the ir sensor.--

## The new way

Uses mqtt hooks to trigger the relay and communicate status. It uses a homebridge server
to call the hooks and deliver the interface to users.

## Current issues

- IR sensor for open/close status is not working and thus the only states are "opening" and "closed" in homekit. It's still functional though


## Future Features

- ~~transmit status via mosquitto~~
- ~~companion homebridge plugin (no longer needed)~~
- ~~better documentation (doing right now)~~
- Fix IR sensor so status can be transmitted properly

Circuit and connection diagrams coming soon. (This is really just how to wire a relay board, not much else so I'm pushing it off. You can google this)

## Project Images

[Top View](images/top.JPG)
[Bottom View](images/bottom.JPG)
[Hooked up view](images/hooked up.JPG)

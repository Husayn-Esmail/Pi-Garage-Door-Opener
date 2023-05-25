#!/bin/bash

echo "enter a username"
read name

mosquitto_passwd -c mqttcredentials $name

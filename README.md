<p align="center" >
<img src="http://bluz.io/static/img/logo.png" alt="" title="">
</p>

Bluz Updater
==========
Bluz is a Development Kit (DK) that implements the Wiring language and talks to the [Particle](https://www.particle.io/) cloud through Bluetooth Low Energy. It can be accessed through a REST API and programmed from a Web IDE.

This app takes in files in the form of a URL and a device ID to flash the files to. The system then starts an update on the Particle cloud and status can be retreieved

##Endpoint
All functions use the common endpoint https://update.bluz.io

##Update
/update/

###POST
Post a new update, which will immediately download the firmware files and flash to the device

####Arguments

The following arguments must be passed in the data body:
device: Device ID of the device to flash
accessToken: Access Token for the device owners account
files: List of files to be flashed

####Response:
Code | Description 
--- | --- 
200| Success 

Returns a UUID which can be used to check the status of the update

####Example:
```
curl --header 'Content-Type:application/json; charset=UTF-8' -d '{"accessToken": "12345", "device": "b1e2abcd, "files": ["http://console.bluz.io/firmware/latest/bluz_dk/system-part1.bin"]}' https://update.bluz.io/update/
```

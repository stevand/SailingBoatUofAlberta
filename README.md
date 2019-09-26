# SailingBoatUofAlberta
Design of ASV Boat at University of Alberta 

## Set up
There are a few dependencies for this project, but they are not strictly necessary unless you wish to run the project on your device or you are working on the corresponding component.

1. You will have to install the [Arduino IDE](https://www.arduino.cc/en/Guide/HomePage) in order to upload code to an Arduino. The code itself can be edited in whatever environment you prefer, so long as you have the software that comes bundled with the IDE.

2. The manufacturer's drivers for our IMU unit can be downloaded [here, under MTi Products](https://www.xsens.com/software-downloads). Their drivers only support python 3.6 and 3.5, so you will have to install one of those (ideally 3.6). There are .whl files inside 'MT SDK/python', which you will need to install in order to use the Xsens Device API. I recommend installing these into a virtual environment. 

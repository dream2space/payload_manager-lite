# Payload Manager

This repo contains code for the Payload Manager for educational Cubesats.

## Raspberry Pi Setup

## Payload Manager Architecture

## List of Programs

The programs are organized as follows:

1. Setting up Camera

2. Setting up Serial communication by UART to Raspberry Pi

3. Setting up Payload Transceiver

4. Scheduling Imaging Mission with Commands

5. Scheduling Downlink with Commands

Finally, putting it all together in the Payload Computer program.

Refer to each section for instructions on how to run the programs.

## Step 1: Setting up the Camera

_Adapted from Raspberry Pi documentation_ [Source](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/2)

Ensure your Raspberry Pi is turned off.

- Locate the Camera Module port

- Gently pull up on the edges of the port’s plastic clip

- Insert the Camera Module ribbon cable; make sure the cable is the right way round

- Push the plastic clip back into place

![attach pi camera](https://projects-static.raspberrypi.org/projects/getting-started-with-picamera/e700e884354667bc3db3dddc19e20931a787c9a7/en/images/connect-camera.gif)

Start up your Raspberry Pi.

Go to the main menu and open the Raspberry Pi Configuration tool.

![configuration](https://projects-static.raspberrypi.org/projects/getting-started-with-picamera/e700e884354667bc3db3dddc19e20931a787c9a7/en/images/pi-configuration-menu.png)

Enable the Camera interface.

![enable camera interface](https://projects-static.raspberrypi.org/projects/getting-started-with-picamera/e700e884354667bc3db3dddc19e20931a787c9a7/en/images/pi-configuration-interfaces-annotated.png)

Reboot the Raspberry Pi.

After Rebooting the Raspberry Pi, run the test program to ensure that the camera module is inserted correctly and all configurations are done correctly.

Open up the terminal by clicking the Terminal icon or pressing `Ctrl+Alt+T`

Enter the following commands in order after each command has been completed:

```bash
cd Desktop
git clone https://github.com/huiminlim/payload_manager-lite
cd payload_manager-lite
chmod 777 install.sh
./install.sh
python3 01-camera_test.py
```

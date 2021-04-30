# Raspberry Pi 3B+ Setup

This documentation describes the setup for the Raspberry Pi off the package for the Payload.

## Overview and Payload Architecture

...

## Step 1: Install Raspbian OS

Download the Raspberry Pi Imager from the website [here](https://www.raspberrypi.org/software/).

Install the Raspberry Pi Imager and launch the Application once installed. The application looks like this.

![Raspberry Pi imager](images/rpiimager.png)

Click `Choose OS` and select the recommended first option, `Raspberry Pi OS (32-bit)`.

![Choose OS](images/choose_os.png)  

Insert the MicroSD card into the PC and click `Choose Storage` to flash the OS onto under the `Storage` tab.

Select the storage volume to flash the OS onto.

![Choose storage](images/CHOOSE_STORAGE.png)  

Wait for the flashing to complete.

## Step 2: Set up the SD Card to enable SSH

Remove and insert the SD card into the PC again.

Enter the `boot` drive that the PC detects.

Create an empty file name `ssh` in `boot`.

This is done by going through the right click menu and creating a file as such.

![picture 5](images/ssh_file.png)  

## Step 3: Set up the Laptop and Ethernet connection to the Raspberry Pi

(*If using Ethernet via USB to access the Raspberry Pi, else using the Monitor or Wifi is possible as well*)

Go to the Laptop's Network Connection and set the Ethernet to obtain IP addresses automatically.

![network](https://www.diyhobi.com/wp-content/uploads/2016/11/set-ethernet-auto-obtain-ip-mylinuxcode.com_.png)

Share the Laptop's WiFi to the Raspberry Pi.

![sharewifi](https://www.diyhobi.com/wp-content/uploads/2016/11/share-wifi-internet-mylinuxcode.png)

## Step 4: Boot up the Raspberry Pi

Boot up the Raspberry Pi and wait for a few minutes until the Yellow LED remains stable for around 5 minutes.

## Step 5: SSH into the Raspberry Pi

Open Putty and key the IP address into the terminal as shown below.

![putty](https://www.diyhobi.com/wp-content/uploads/2016/12/putty-raspberrypi-local.png)

Once successful, the login screen will appear. Login with the default account credentials:

```bash
username: pi
password: raspberry
```

![SSH login](images/ssh_login.png)  

Use `sudo raspi-config` to enter the configuration screen to start VNC.

Navigate to the Interface options and press enter.

![Raspi Config](images/raspiconfig.png)  

Navigate to the VNC option and press enter.

![VNC](images/VNC.png)  

Select yes to enable VNC.

![VNC2](images/VNC2.png)

Leave the configuration page by selecting Finish.

![Finish Raspi](images/finishraspi.png)  

When prompted to reboot, selected yes and wait for 5 minutes until the Yellow LED stabilizes after 5 minutes.

### Step 6: Enable Camera interface

Use `sudo raspi-config` to enter the configuration screen to enable the camera interface.

Similar to the previous step, navigate to the Interface options and press enter.

Select Camera option and press enter.

![Camera interface](images/camerainterface.png)  

Select yes and press enter.

![Camera Interface 2](images/Camerainterface2.png)  

Similarly, leave the configuration page by selecting finish.

When prompted to reboot, selected yes and wait for 5 minutes until the Yellow LED stabilizes after 5 minutes.

### Step 7: Use VNC

Use VNC to view the GUI desktop of the Raspberry Pi.

Enter `raspberrypi.local` into the top bar to connect to the Raspberry Pi via VNC.

![VNC Login](images/vnc_login.png)  

Once entered into the GUI, enter the default username and password.

### Step 8: Set up UART

Source: [here](https://www.raspberrypi.org/documentation/configuration/uart.md) and [here](https://www.circuits.dk/setup-raspberry-pi-3-gpio-uart/)

Open up the terminal and issue the following command.

```bash
dmesg | grep tty
```

The following screen should be observed, with the `PL011` connected to the `ttyAMA01`.

![ttyAMA01](images/AMA01.png)  

Issue the `sudo raspi-config` command and navigate to the `Interface Options` and then to `Serial Port`, the press enter.

![Serial Port](images/Serialport.png)  

When prompted about the login shell over console, select No.

![Login Shell over Console](images/loginshellconsole.png)  

When prompted about enabling hardware serial, select Yes.

![Hardware Serial](images/hardwareserial.png)  

Exit the configuration page and reboot.

Once the reboot is successful, issue the following command into the terminal.

```bash
sudo nano /boot/config.txt
```

Add these 2 lines to the end of the file if they are not already there.

```bash
enable_uart=1
core_freq=250
```

![Config file](images/bootconfig.png)  

Press `Ctrl+X`, `Y` and enter to save and exit the file.

Proceed to reboot the Raspberry Pi for changes to take effect.

### Step 9: Test if UART configurations are successful

Short the TX and RX pins and launch minicom.

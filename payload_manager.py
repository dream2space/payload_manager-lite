from apscheduler.schedulers.background import BackgroundScheduler
from ccsds_packet import CCSDS_Chunk_Packet, CCSDS_Control_Packet
from picamera import PiCamera
import serial
import sys
import os


def main(use_camera, use_downlink):
    # Initialize Scheduler in background
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Initialize Camera
    camera = PiCamera()
    camera.resolution = (640, 480)

    # Open Serial port to receive commands
    # Blocking to wait forever for input
    ser_cmd_input = serial.Serial('/dev/serial0', baudrate=9600, timeout=None)

    # Open Serial port to downlink images
    ser_downlink = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=10)


if __name__ == "__main__":

    use_camera = True
    use_downlink = True

    if len(sys.argv)-1 > 0:
        if "--nodownlink" in sys.argv:
            use_downlink = False

        if "--nocam" in sys.argv:
            use_camera = False

    main(use_camera, use_downlink)

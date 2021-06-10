import os
import sys
import time

import serial
from apscheduler.schedulers.background import BackgroundScheduler
from picamera import PiCamera

import Mission_Parameters as param
from Command_Parser import Command_Parser
from Downlink_Util import execute_downlink
from Mission_Util import execute_mission


def main(use_camera, use_downlink):
    # Initialize Scheduler in background
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Initialize Camera
    camera = PiCamera()
    camera.resolution = (640, 480)

    # Create serial command parser
    command_parser = Command_Parser()

    # Check if mission folder created
    if os.path.isdir(param.MISSION_ROOT_FILEPATH) == False:
        os.makedirs(param.MISSION_ROOT_FILEPATH)
    else:
        # Mission folder exists
        pass

    # Open Serial port to receive commands - Blocking to wait forever for input
    try:
        ser_cmd_input = serial.Serial(
            '/dev/serial0', baudrate=9600, timeout=None)
    except serial.SerialException:
        print(f"Serial Port Exception - Cannot open {'/dev/serial0'}")
        sys.exit()

    # Open Serial port to downlink images
    try:
        ser_downlink = serial.Serial(
            "/dev/ttyUSB0", baudrate=115200, timeout=10)
    except serial.SerialException:
        print(f"Serial Port Exception - Cannot open {'/dev/ttyUSB0'}")
        sys.exit()

    try:
        print("Waiting for commands...")
        # Read payload command from serial
        while True:
            try:
                read_command = ser_cmd_input.readline().decode("utf-8").replace('\r', '').replace('\n', '')
            except UnicodeDecodeError:
                print("\nUnicode Decode Error\n")
                ser_cmd_input.flush()
                time.sleep(1)
                # Request for command again from Payload Computer
                ser_cmd_input.write(b"bcc\r\n")
                continue  # To re-read command from serial

            except ValueError:
                print("\nValue Error! Request from payload computer again\n")
                time.sleep(1)
                # Request for command again from Payload Computer
                ser_cmd_input.write(b"bcc\r\n")
                continue  # To re-read command from serial

            print(f"Received: {read_command}")
            # Parse read command into Command object
            parsed_command = command_parser.parse(read_command)

            # Mission + Downlink command
            if parsed_command.get_type() == 'md':
                print(parsed_command)

                # Create folder for mission
                mission_folder_path = parsed_command.get_mission_folder_path()
                os.mkdir(mission_folder_path)
                print(f"Mission directory created: {mission_folder_path}")

                # Schedule jobs for each datetime object
                list_datetime = parsed_command.get_mission_datetime()
                print(f"List of mission: {list_datetime}")
                count = 0
                for dt in list_datetime:
                    count += 1
                    scheduler.add_job(execute_mission, run_date=dt, args=[
                        camera, mission_folder_path, dt, count])

                # Schedule job for downlink
                down_timestamp = parsed_command.get_down_timestamp()
                scheduler.add_job(execute_downlink, next_run_time=down_timestamp, args=[
                    ser_downlink, mission_folder_path])

            # Request again if command is unknown
            elif parsed_command.get_type() == 'unknown':
                time.sleep(1)
                # Request for command again from Payload Computer
                ser_cmd_input.write(b"bcc\r\n")
                continue  # To re-read command from serial

            # ignore blank command
            elif parsed_command.get_type() == 'blank':
                continue

            print("\n\nWaiting for commands...")

    except KeyboardInterrupt:
        scheduler.shutdown()
        camera.close()
        print("End, exiting")
        sys.exit(0)

    # # Fall through exception -- just in case
    # except Exception as ex:
    #     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    #     message = template.format(type(ex).__name__, ex.args)
    #     print(message)


if __name__ == "__main__":
    use_camera = True
    use_downlink = True

    if len(sys.argv)-1 > 0:
        if "--nodownlink" in sys.argv:
            use_downlink = False

        if "--nocam" in sys.argv:
            use_camera = False

    main(use_camera, use_downlink)

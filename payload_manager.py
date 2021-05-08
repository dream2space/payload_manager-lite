from apscheduler.schedulers.background import BackgroundScheduler
from Command_Parser import Command_Parser
from Mission_Util import execute_mission
from picamera import PiCamera
import parameters as param
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

    # Create serial command parser
    command_parser = Command_Parser()

    # Check if mission folder created
    if os.path.isdir(param.MISSION_ROOT_FILEPATH) == False:
        os.makedirs(param.MISSION_ROOT_FILEPATH)
    else:
        # Mission folder exists
        pass

    # Open Serial port to receive commands
    # Blocking to wait forever for input
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

    # Read payload command from serial
    while True:
        print("Waiting for commands...")
        read_command = ser_cmd_input.readline().decode("utf-8").replace("\r\n", "")
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
            count = 0
            for dt in list_datetime:
                count += 1
                scheduler.add_job(execute_mission, run_date=dt, args=[
                                  camera, mission_folder_path, dt, count])

            # Schedule job for downlink


if __name__ == "__main__":
    use_camera = True
    use_downlink = True

    if len(sys.argv)-1 > 0:
        if "--nodownlink" in sys.argv:
            use_downlink = False

        if "--nocam" in sys.argv:
            use_camera = False

    main(use_camera, use_downlink)

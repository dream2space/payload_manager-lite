from archive.payload_manager_helper import BATCH_SIZE, CHUNK_SIZE
from ccsds_packet import CCSDS_Chunk_Packet, CCSDS_Control_Packet
import serial
import os


TEST_FILEPATH = '/home/pi/Desktop/Mission/2021-04-19_09:57:00'

#### DOWNLINK CONSTANTS ####
BATCH_SIZE = 5
PRE_ENC_CHUNK_SIZE = 120  # bytes, w/o 16 bytes rs encoding yet

# Given mission folder path, obtain list of images path


def obtain_downlink_images_filepaths(mission_folder_path):
    list_filepaths = []
    for file in os.listdir(mission_folder_path):
        list_filepaths.append(mission_folder_path + '/' + file)
    return list_filepaths


def main():
    ser_downlink = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=10)

    # Get list of files to downlink
    filepath_list = obtain_downlink_images_filepaths(TEST_FILEPATH)
    print(filepath_list)


if __name__ == "__main__":
    main()

from archive.payload_manager_helper import BATCH_SIZE, CHUNK_SIZE
from ccsds_packet import CCSDS_Chunk_Packet, CCSDS_Control_Packet
import subprocess
import serial
import pprint
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


# Given filepath to image, compress and encode the image bytes and return the bytes
def extract_enc_img_bytes(img_filepath):
    # Grant permission to script if not already done so
    os.chmod("prep_test.sh", 0o777)
    os.chmod("cleanup.sh", 0o777)

    # Call bash script to execute prep script
    # base64 + gzip
    prep_filepath = './prep_test.sh ' + img_filepath
    subprocess.call(prep_filepath, stdout=subprocess.DEVNULL, shell=True)

    # Open and read in the image
    with open('base_enc.gz', 'rb') as file:
        compressed_enc = file.read()
        file.close()

    # Call bash script to remove currently created compressed files
    subprocess.call('./cleanup.sh base_enc.gz',
                    stdout=subprocess.DEVNULL, shell=True)

    return compressed_enc


def main():
    ser_downlink = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=10)

    # Get list of files to downlink
    filepath_list = obtain_downlink_images_filepaths(TEST_FILEPATH)
    pprint.pprint(filepath_list)  # Print list of files for debug

    # Handle downlink of each image
    total_img_num = len(filepath_list)
    for filepath in filepath_list:
        enc_img_bytes = extract_enc_img_bytes(filepath)
        total_bytes = len(enc_img_bytes)


if __name__ == "__main__":
    main()

from archive.payload_manager_helper import BATCH_SIZE, CHUNK_SIZE
from ccsds_packet import CCSDS_Chunk_Packet, CCSDS_Control_Packet
import serial


TEST_FILEPATH = '/home/pi/Desktop/Mission/2021-04-19_09:57:00'

#### DOWNLINK CONSTANTS ####
BATCH_SIZE = 5
PRE_ENC_CHUNK_SIZE = 120  # bytes, w/o 16 bytes rs encoding yet


def main():
    ser_downlink = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=10)


if __name__ == "__main__":
    main()

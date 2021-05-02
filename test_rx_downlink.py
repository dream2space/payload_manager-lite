from ccsds_packet import CCSDS_Packet_Decoder
from parameters import *
import serial
import time


def main():
    ccsds_decoder = CCSDS_Packet_Decoder()

    com_port = input("Enter payload transceiver port: ")
    ser_payload = serial.Serial(com_port, baudrate=115200, timeout=None)

    start_packet = ser_payload.read(149)
    # ser_payload.timeout = 5

    # Extract out useful data from padded packet
    start_packet = start_packet[:13]

    total_batch_expected = int.from_bytes(start_packet[10:], 'big')
    print(f"Total batches: {total_batch_expected}")

    batch_counter = 1
    packet_count = 1
    recv_bytes = []
    while batch_counter <= total_batch_expected:

        while True:  # For stop packet
            ser_bytes = ser_payload.read(TOTAL_PACKET_LENGTH)

            ret = ccsds_decoder.quick_parse(ser_bytes)
            print(ret)
            if ret['stop'] == False:
                recv_bytes.append(ser_bytes)
            else:
                break

        time.sleep(TIME_BETWEEN_PACKETS*2)
        ser_payload.write(b"ack\r\n")
        packet_count = 1
        batch_counter += 1


if __name__ == "__main__":
    main()

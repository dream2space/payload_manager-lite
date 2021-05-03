from ccsds_packet import CCSDS_Packet_Decoder
from parameters import *
from datetime import datetime
import serial
import time


def main():
    ccsds_decoder = CCSDS_Packet_Decoder()

    com_port = input("Enter payload transceiver port: ")
    ser_payload = serial.Serial(com_port, baudrate=115200, timeout=None)

    start_packet = ser_payload.read(TOTAL_PACKET_LENGTH)
    # ser_payload.timeout = 5

    # Extract out useful data from padded packet
    start_packet = start_packet[:13]

    total_batch_expected = int.from_bytes(start_packet[10:], 'big')
    print(f"Total batches: {total_batch_expected}")

    recv_bytes = []
    transfer_start = datetime.now()
    while True:
        return_val = b"ack\r\n"
        temp_list = []
        curr_batch = -1

        while True:  # For stop packet
            ser_bytes = ser_payload.read(TOTAL_PACKET_LENGTH)

            ret = ccsds_decoder.quick_parse(ser_bytes)
            print(ret)

            if ret["fail"] == True:
                time.sleep(TIMEOUT_TX-2)
                return_val = b"nack\r\n"
                ser_payload.flushInput()
                break
            else:
                if ret['stop'] == False:
                    temp_list.append(ser_bytes)
                    curr_batch = ret['curr_batch']
                else:
                    recv_bytes += temp_list
                    break

        print()
        ser_payload.write(return_val)

        if ret['stop'] and curr_batch == total_batch_expected:
            break

    transfer_end = datetime.now()
    elapsed_time = transfer_end - transfer_start
    print(f"Time elapsed: {elapsed_time}")


if __name__ == "__main__":
    main()

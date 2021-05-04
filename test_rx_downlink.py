from ccsds_packet import CCSDS_Packet_Decoder
from datetime import datetime
from parameters import *
import serial
import time


def main():
    ccsds_decoder = CCSDS_Packet_Decoder()

    com_port = input("Enter payload transceiver port: ")
    ser_payload = serial.Serial(com_port)
    ser_payload.baudrate = 115200
    # Cannot set as nonblocking
    # else send back all bytes at that point
    ser_payload.timeout = None

    start_packet = ser_payload.read(TOTAL_PACKET_LENGTH)

    # Extract out useful data from padded packet
    start_packet = start_packet[:13]

    total_batch_expected = int.from_bytes(start_packet[10:], 'big')
    print(f"Total batches: {total_batch_expected}")

    recv_bytes = []
    temp_list = []
    prev_batch_recv = -1

    is_ack = True
    transfer_start = datetime.now()
    # Receive all batches
    while True:
        ser_bytes = ser_payload.read(TOTAL_PACKET_LENGTH)

        if prev_batch_recv + 1 == total_batch_expected:
            ser_payload.timeout = TIMEOUT_RX

        if ser_bytes == b"":
            # Last packet received
            break

        ret = ccsds_decoder.quick_parse(ser_bytes)

        if ret['fail'] == True:
            is_ack = False
        else:

            if ret['stop'] == False and ret['curr_batch'] != prev_batch_recv:
                temp_list.append(ser_bytes)
                print(f"Append - {ret}")
                temp_store = ret['curr_batch']

            elif ret['stop'] == True:
                # Stop packet received
                recv_bytes += temp_list
                temp_list = []  # Wipe out temp list

                if is_ack:
                    return_val = b"ack\r\n"
                    is_ack = True
                    prev_batch_recv = temp_store
                else:
                    return_val = b"nack\r\n"
                    is_ack = False

                time.sleep(TIME_BEFORE_ACK)
                ser_payload.write(return_val)
                print(f"Sent {return_val}")
                print()

    transfer_end = datetime.now()
    elapsed_time = transfer_end - transfer_start
    print(f"Time elapsed: {elapsed_time}")


if __name__ == "__main__":
    main()

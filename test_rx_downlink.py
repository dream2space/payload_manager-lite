from ccsds_packet import CCSDS_Packet_Decoder
from parameters import *
from datetime import datetime
import serial
import time


def main():
    ccsds_decoder = CCSDS_Packet_Decoder()

    com_port = input("Enter payload transceiver port: ")
    ser_payload = serial.Serial(com_port)
    ser_payload.baudrate = 115200
    ser_payload.timeout = 0         # Non-blocking

    start_packet = ser_payload.read(TOTAL_PACKET_LENGTH)

    # Extract out useful data from padded packet
    start_packet = start_packet[:13]

    total_batch_expected = int.from_bytes(start_packet[10:], 'big')
    print(f"Total batches: {total_batch_expected}")

    recv_bytes = []
    temp_list = []
    curr_batch = -1
    is_ack = True
    is_first_send = True
    transfer_start = datetime.now()
    # Receive all batches
    while True:

        ser_bytes = ser_payload.read(TOTAL_PACKET_LENGTH)

        # If blank, skip
        if ser_bytes == b"":
            # Resend ack/nack if more than 30 sec no new batch since last sent ack/nack
            if is_first_send == False and (last_send_ack_time - datetime.now()).total_seconds() >= 30:
                ser_payload.write(return_val)
            else:
                continue

        # Packet comes in, process it
        ret = ccsds_decoder.quick_parse(ser_bytes)
        print(ret)

        if ret['fail'] == True:
            is_ack = False
        else:
            if ret['stop'] == False:
                temp_list.append(ser_bytes)
                curr_batch = ret['curr_batch']
            else:
                recv_bytes += temp_list
                temp_list = []  # Wipe out temp list
                curr_batch = -1  # Wipe out current batch

                if is_ack:
                    return_val = b"ack\r\n"
                else:
                    return_val = b"nack\r\n"
                ser_payload.write(return_val)
                is_first_send = False
                last_send_ack_time = datetime.now()
                print(f"Sent {return_val}")

                if ret['stop'] and curr_batch == total_batch_expected:
                    break

    transfer_end = datetime.now()
    elapsed_time = transfer_end - transfer_start
    print(f"Time elapsed: {elapsed_time}")


if __name__ == "__main__":
    main()

from CCSDS_Packet import CCSDS_Packet_Decoder
from Mission_Parameters import *
from datetime import datetime
import subprocess
import serial
import time
import os


def main():
    ccsds_decoder = CCSDS_Packet_Decoder()

    com_port = input("Enter payload transceiver port: ")
    ser_payload = serial.Serial(com_port)
    ser_payload.baudrate = 115200
    ser_payload.timeout = None  # Cannot set as nonblocking

    start_packet = ser_payload.read(TOTAL_PACKET_LENGTH)

    # Extract out useful data from padded packet
    start_packet = start_packet[:13]

    total_batch_expected = int.from_bytes(start_packet[10:], 'big')
    print(f"Total batches: {total_batch_expected}")

    recv_packets = []
    # temp_list = []
    prev_batch_recv = -1
    is_packet_failed = False

    transfer_start = datetime.now()
    # Receive all batches
    while True:

        # ---------------------------------------------------------------

        ser_bytes = ser_payload.read(TOTAL_PACKET_LENGTH)

        # ---------------------------------------------------------------

        # Allow timeout for batch after last
        if prev_batch_recv + 1 == total_batch_expected:
            ser_payload.timeout = TIMEOUT_RX

        # Exit loop after final batch
        if ser_bytes == b"":
            break

        ret = ccsds_decoder.quick_parse(ser_bytes)

        # ---------------------------------------------------------------
        # Decoding packet
        # ---------------------------------------------------------------

        # Failed to receive current packet
        if ret['fail'] == True:
            print(ret)
            is_packet_failed = True

        # Successfully received current packet
        else:
            # Append received packet to list
            recv_packets.append(ser_bytes)
            print(f"Append - {ret}")

            # Flag to indicate successfully received packet
            is_packet_failed = False

        # ---------------------------------------------------------------
        # Handle Ack/Nack
        # ---------------------------------------------------------------

        # Send nack
        if is_packet_failed:
            return_val = b"nack\r\n"

        # Send ack
        else:
            return_val = b"ack\r\n"
            prev_batch_recv = ret['curr_batch']

        time.sleep(TIME_BEFORE_ACK)
        ser_payload.write(return_val)
        print(f"Sent {return_val}")
        print()

    print(f"Collected {len(recv_packets)} packets")
    transfer_end = datetime.now()
    elapsed_time = transfer_end - transfer_start
    print(f"Time elapsed: {elapsed_time}")

    # Reassemble packets to image
    with open(f"{GROUND_STN_MISSION_FOLDER_PATH}/out.gz", "wb") as enc_file:
        for packet in recv_packets:
            enc_file.write(ccsds_decoder.parse(packet))
        enc_file.close()

    os.chmod("decode.sh", 0o777)
    subprocess.Popen("./decode.sh out out", shell=True)
    print("Done!")


if __name__ == "__main__":
    main()

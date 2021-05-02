from ccsds_packet import CCSDS_Chunk_Packet, CCSDS_Control_Packet
import serial
import time

TOTAL_PACKET_LENGTH = 149
HEADER_LENGTH = 6
TELEMETRY_TYPE_LENGTH = 1  # bytes
TOTAL_BYTES_LENGTH = 3
TOTAL_BATCH_LENGTH = 3


def main():
    com_port = input("Enter payload transceiver port: ")
    ser_payload = serial.Serial(com_port, baudrate=115200, timeout=None)

    start_packet = ser_payload.read(149)
    ser_payload.timeout = 5

    # Extract out useful data from padded packet
    start_packet = start_packet[:13]

    total_batch_expected = int.from_bytes(start_packet[10:], 'big')
    print(f"Total batches: {total_batch_expected}")

    batch_counter = 1
    packet_count = 1
    while batch_counter <= total_batch_expected:
        while packet_count <= 6:
            ser_payload.read(149)
            packet_count += 1

        time.sleep(0.2)
        ser_payload.write(b"ack\r\n")


if __name__ == "__main__":
    main()

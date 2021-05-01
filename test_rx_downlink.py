from ccsds_packet import CCSDS_Chunk_Packet, CCSDS_Control_Packet
import serial


def main():
    com_port = input("Enter payload transceiver port: ")
    ser_payload = serial.Serial(com_port, baudrate=115200, timeout=None)


if __name__ == "__main__":
    main()

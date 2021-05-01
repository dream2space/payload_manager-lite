from reedsolo import RSCodec


class CCSDS_Packet:
    """A CCSDS Packet class"""

    def __init__(self, packet_seq_num, packet_data):
        self.packet_seq_num = packet_seq_num
        self.packet_data = packet_data

        # Create packet header
        self.header = self._create_packet_header(packet_seq_num, packet_data)

    def __str__(self):
        return f"{self.header}|{self.packet_data}"

    def get_tx_packet(self):
        pass

    # Private method
    def _create_packet_header(self, seq_num, packet_data):
        temp_header = bytearray(0)  # octet 1, 2, ..., 6

        # Handle first octet
        octet = 0b0
        octet = octet << 3 | 0b000      # Version number
        octet = octet << 1 | 0b0        # Packet ID - 0 for telemetry packet
        octet = octet << 1 | 0b0        # Packet Secondary Header Flag - 0 for none
        octet = octet << 11 | 0b10      # App Process ID - define process creating packet
        temp_header = temp_header + octet.to_bytes(2, 'big')

        # Handle second octet
        octet = 0b0
        octet = octet << 2 | 0b11       # Packet sequence control - 0 for no grouping
        octet = octet << 14 | (seq_num % 16384)    # Seq num modulo 16384
        temp_header = temp_header + octet.to_bytes(2, 'big')

        # Handle third octet
        octet = 0b0
        octet = octet << 16 | (len(packet_data) - 1)    # Total octets data - 1
        temp_header = temp_header + octet.to_bytes(2, 'big')

        return temp_header


print(CCSDS_Packet(1, b"hello"))

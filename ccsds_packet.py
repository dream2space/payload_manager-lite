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


class CCSDS_Start_Packet(CCSDS_Packet):

    def __init__(self, packet_seq_num, telemetry_packet_type, total_bytes, total_batch):
        packet_data = self._create_start_packet_data(
            telemetry_packet_type, total_bytes, total_batch)
        super().__init__(packet_seq_num, packet_data)

    def __str__(self):
        return f"{self.header}|{self.packet_data}"

    def get_tx_packet(self):
        return self.header + self.packet_data

    def _create_start_packet_data(self, telemetry_packet_type, total_bytes, total_batch):
        TELEMETRY_TYPE_LENGTH = 1  # bytes
        TOTAL_BYTES_LENGTH = 3
        TOTAL_BATCH_LENGTH = 3

        data = bytearray(0)
        data = telemetry_packet_type.to_bytes(TELEMETRY_TYPE_LENGTH, 'big')
        data = data + total_bytes.to_bytes(TOTAL_BYTES_LENGTH, 'big')
        data = data + total_batch.to_bytes(TOTAL_BATCH_LENGTH, 'big')

        return data


class CCSDS_Chunk_Packet(CCSDS_Packet):

    def __init__(self, packet_seq_num, telemetry_packet_type, current_batch_num, current_chunk_num, chunk):
        self.chunk = chunk
        packet_data = self._create_chunk_packet_data(
            telemetry_packet_type, current_batch_num, current_chunk_num, chunk)
        super().__init__(packet_seq_num, packet_data)

    def __str__(self):
        return f"{self.header}|{self.packet_data}"

    def get_tx_packet(self):
        return self.header + self.packet_data

    def _create_chunk_packet_data(self, telemetry_packet_type, current_batch_num, current_chunk_num, chunk):
        TELEMETRY_TYPE_LENGTH = 1
        CURRENT_CHUNKS_LENGTH = 3  # bytes
        CURRENT_BATCH_LENGTH = 3

        data = bytearray(0)
        data = telemetry_packet_type.to_bytes(TELEMETRY_TYPE_LENGTH, 'big')
        data = data + current_batch_num.to_bytes(CURRENT_BATCH_LENGTH, 'big')
        data = data + current_chunk_num.to_bytes(CURRENT_CHUNKS_LENGTH, 'big')

        rsc = RSCodec(16)  # 16 ecc symbols
        data += rsc.encode(self.chunk)

        return data


if __name__ == "__main__":
    # print(CCSDS_Start_Packet(1, 11, 200, 120))
    # print(CCSDS_Start_Packet(1, 11, 200, 120).get_tx_packet())

    # print(CCSDS_Chunk_Packet(1, 11, 200, 120, b"hello"))
    print(CCSDS_Chunk_Packet(1, 11, 200, 120, b"hello").get_tx_packet())

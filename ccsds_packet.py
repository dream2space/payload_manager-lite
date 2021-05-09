from Mission_Parameters import *
from reedsolo import RSCodec


#### DOWNLINK CONSTANTS ####
BATCH_SIZE = 5
PRE_ENC_CHUNK_SIZE = 120  # bytes, w/o 16 bytes rs encoding yet
TELEMETRY_PACKET_TYPE_DOWNLINK_START = 30
TELEMETRY_PACKET_TYPE_DOWNLINK_PACKET = 31
TELEMETRY_PACKET_TYPE_DOWNLINK_STOP = 32


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


class CCSDS_Control_Packet(CCSDS_Packet):

    def __init__(self, packet_seq_num, telemetry_packet_type, total_bytes, total_batch):
        packet_data = self._create_start_packet_data(
            telemetry_packet_type, total_bytes, total_batch)
        super().__init__(packet_seq_num, packet_data)

    def __str__(self):
        return f"control|seqnum:{self.packet_seq_num}|len:{len(self.get_tx_packet())}"

    def get_tx_packet(self):
        return self._pad_tx_packet(self.header + self.packet_data)

    def _create_start_packet_data(self, telemetry_packet_type, total_bytes, total_batch):
        TELEMETRY_TYPE_LENGTH = 1  # bytes
        TOTAL_BYTES_LENGTH = 3
        TOTAL_BATCH_LENGTH = 3

        data = bytearray(0)
        data = telemetry_packet_type.to_bytes(TELEMETRY_TYPE_LENGTH, 'big')
        data = data + total_bytes.to_bytes(TOTAL_BYTES_LENGTH, 'big')
        data = data + total_batch.to_bytes(TOTAL_BATCH_LENGTH, 'big')

        return data

    def _pad_tx_packet(self, prepad):
        TOTAL_PACKET_LENGTH = 149
        HEADER_LENGTH = 6
        TELEMETRY_TYPE_LENGTH = 1  # bytes
        TOTAL_BYTES_LENGTH = 3
        TOTAL_BATCH_LENGTH = 3

        return prepad + b"A" * (TOTAL_PACKET_LENGTH - HEADER_LENGTH - TELEMETRY_TYPE_LENGTH - TOTAL_BYTES_LENGTH - TOTAL_BATCH_LENGTH)


class CCSDS_Chunk_Packet(CCSDS_Packet):

    def __init__(self, packet_seq_num, telemetry_packet_type, current_batch_num, current_chunk_num, chunk):
        self.rsc = RSCodec(16)  # 16 ecc symbols
        self.chunk = chunk
        packet_data = self._create_chunk_packet_data(
            telemetry_packet_type, current_batch_num, current_chunk_num, chunk)
        super().__init__(packet_seq_num, packet_data)

    def __str__(self):
        return f"chunk|seqnum:{self.packet_seq_num}|len:{len(self.get_tx_packet())}"

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

        data += self.rsc.encode(chunk)

        return data


class CCSDS_Packet_Decoder():
    """CCSDS Class decodes CCSDS Control (Start/Stop) and Chunk packets"""

    def __init__(self):
        self.rsc = RSCodec(16)  # 16 ecc symbols

    # Takes in bytearray to parse
    def parse(self, CCSDS_Packet):

        # Parse header
        # header = self._parse_header(CCSDS_Packet)

        # Detect if it is Chunk or Stop
        packet_data = CCSDS_Packet[6:]
        telemetry_packet_type = packet_data[0]

        if telemetry_packet_type == TELEMETRY_PACKET_TYPE_DOWNLINK_PACKET:
            return self._parse_chunk(packet_data)
        else:
            return self._parse_stop()

    def _parse_header(self, CCSDS_Packet):
        # Extract header
        header = CCSDS_Packet[:6]
        version_number = header[0] >> 5
        type_indicator = (header[0] >> 4) & 0b1
        secondary_header_flag = (header[0] >> 3) & 0b1
        application_id = ((header[0] & 0b11) << 11) | header[1]
        group_flags = header[2] >> 6
        source_seq_count = ((header[2] & 0b00111111) << 8) | header[3]
        packet_length = (header[4] << 8) | header[5]

        ret_header = {'Version Number': version_number, 'Type Indicator': type_indicator,
                      'Secondary Header Flag': secondary_header_flag, 'Application ID': application_id,
                      'Group Flags': group_flags, 'Source Sequence Count': source_seq_count,
                      'Packet length': packet_length}
        return ret_header

    def _parse_chunk(self, packet_data):
        image_payload = packet_data[7:]
        return self.rsc.decode(image_payload)[0]

    def _parse_stop(self):
        return b"stop"

    # Quickly parse and return batch and chunk number
    def quick_parse(self, CCSDS_Packet):
        telemetry_packet_type = CCSDS_Packet[6]

        if telemetry_packet_type == TELEMETRY_PACKET_TYPE_DOWNLINK_STOP:
            return {"fail": False, "stop": True}

        elif telemetry_packet_type == TELEMETRY_PACKET_TYPE_DOWNLINK_PACKET:
            # Extract batch and chunk number
            curr_batch = int.from_bytes(
                CCSDS_Packet[7:10], byteorder='big', signed=False)
            curr_chunk = int.from_bytes(
                CCSDS_Packet[10:13], byteorder='big', signed=False)
            return {"fail": False, "stop": False, "curr_batch": curr_batch, "curr_chunk": curr_chunk}

        else:
            return {"fail": True}


if __name__ == "__main__":
    print(CCSDS_Control_Packet(1, 11, 200, 120))
    print(CCSDS_Control_Packet(1, 11, 200, 120).get_tx_packet())

    print(CCSDS_Chunk_Packet(1, 11, 200, 120, b"hello" * 24))
    print(CCSDS_Chunk_Packet(1, 11, 200, 120, b"hello" * 24).get_tx_packet())

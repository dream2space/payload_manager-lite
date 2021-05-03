
TEST_FILEPATH = '/home/pi/Desktop/Mission/2021-04-19_09:57:00'
# TEST_FILEPATH = '/home/pi/Desktop/test'


#### DOWNLINK CONSTANTS ####
BATCH_SIZE = 5
PRE_ENC_CHUNK_SIZE = 120  # bytes, w/o 16 bytes rs encoding yet
TELEMETRY_PACKET_TYPE_DOWNLINK_START = 30
TELEMETRY_PACKET_TYPE_DOWNLINK_PACKET = 31
TELEMETRY_PACKET_TYPE_DOWNLINK_STOP = 32

TOTAL_PACKET_LENGTH = 149
HEADER_LENGTH = 6
TELEMETRY_TYPE_LENGTH = 1  # bytes
TOTAL_BYTES_LENGTH = 3
TOTAL_BATCH_LENGTH = 3

TELEMETRY_TYPE_LENGTH = 1  # bytes
CURRENT_CHUNKS_LENGTH = 3
CURRENT_BATCH_LENGTH = 3
TOTAL_BYTES_LENGTH = 3
TOTAL_BATCH_LENGTH = 3

TIME_SLEEP_AFTER_START = 2
TIME_BEFORE_ACK = 2
TIME_BETWEEN_PACKETS = 0.2

TIMEOUT_TX = 10
TIMEOUT_RX = TIME_SLEEP_AFTER_START * 3

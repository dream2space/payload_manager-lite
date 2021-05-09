from ccsds_packet import CCSDS_Chunk_Packet, CCSDS_Control_Packet
from parameters import *
import subprocess
import pprint
import time
import os


# Given mission folder path, obtain list of images path
def obtain_downlink_images_filepaths(mission_folder_path):
    list_filepaths = []
    for file in os.listdir(mission_folder_path):
        list_filepaths.append(mission_folder_path + '/' + file)
    return list_filepaths


# Given filepath to image, compress and encode the image bytes and return the bytes
def extract_enc_img_bytes(img_filepath):

    # Grant permission to script if not already done so
    os.chmod("prep_test.sh", 0o777)
    os.chmod("cleanup.sh", 0o777)

    # Call bash script to execute prep script
    # base64 + gzip
    prep_filepath = './prep_test.sh ' + img_filepath
    subprocess.call(prep_filepath, stdout=subprocess.DEVNULL, shell=True)

    # Open and read in the image
    with open('base_enc.gz', 'rb') as file:
        compressed_enc = file.read()
        file.close()

    # Call bash script to remove currently created compressed files
    subprocess.call('./cleanup.sh base_enc.gz',
                    stdout=subprocess.DEVNULL, shell=True)

    return compressed_enc


def prepare_tx_batch(enc_img_bytes):

    # Returns a list of chunks of bytes, given chunk size and bytearray
    def chop_bytes(bytes_arr, chunk_size):
        chunk_arr = []
        idx = 0
        while idx + chunk_size < len(bytes_arr):
            chunk_arr.append(bytes_arr[idx:idx + chunk_size])
            idx = idx + chunk_size
        # Remaining odd sized chunk
        chunk_arr.append(bytes_arr[idx:])
        return chunk_arr

    # Given an list of chunks, split them into list of batches given a batch size
    def split_batch(chunks_arr, batch_size):
        batch_arr = []
        idx = 0
        while idx + batch_size <= len(chunks_arr):
            batch_arr.append(chunks_arr[idx:idx + batch_size])
            idx = idx + batch_size
        # Remaining odd sized chunk
        batch_arr.append(chunks_arr[idx:])
        return batch_arr

    # Chop up bytes into chunks and prepare CCSDS packet
    chunk_list = chop_bytes(enc_img_bytes, PRE_ENC_CHUNK_SIZE)

    # Split chunks into batches
    batch_list = split_batch(chunk_list, BATCH_SIZE)

    # Create CCSDS Packets
    packet_batch_list = []
    packet_seq_num = 1
    for batch_num in range(len(batch_list)):
        batch = batch_list[batch_num]

        chunk_num = 1
        new_batch = []
        for chunk in batch:
            # Create CCSDS Packet for each chunk
            packet = CCSDS_Chunk_Packet(
                packet_seq_num, TELEMETRY_PACKET_TYPE_DOWNLINK_PACKET, batch_num+1, chunk_num, chunk)
            new_batch.append(packet)
            packet_seq_num += 1
            chunk_num += 1

        # Put stop packet at all batches but not the last batch
        if batch_num != len(batch_list)-1:
            stop_packet = CCSDS_Control_Packet(
                packet_seq_num, TELEMETRY_PACKET_TYPE_DOWNLINK_STOP, 0, 0)
            new_batch.append(stop_packet)
            packet_seq_num += 1

        packet_batch_list.append(new_batch)

    return packet_batch_list


def execute_downlink(ser_downlink, mission_folder_path):

    # Get list of files to downlink
    filepath_list = obtain_downlink_images_filepaths(mission_folder_path)
    print("Downlink images:")
    pprint.pprint(filepath_list)  # Print list of files for debug

    # Handle downlink of each image via filepath
    for filepath in filepath_list:

        # Prepare encoded image bytes
        enc_img_bytes = extract_enc_img_bytes(filepath)

        # Prepare tx batches
        batches = prepare_tx_batch(enc_img_bytes)
        print(f"Number of batches: {len(batches)}")

        # Send CCSDS Start Packet
        start_packet = CCSDS_Control_Packet(
            0, TELEMETRY_PACKET_TYPE_DOWNLINK_START, len(enc_img_bytes), len(batches))
        ser_downlink.write(start_packet.get_tx_packet())
        time.sleep(TIME_SLEEP_AFTER_START)

        # Start sending downlink packets
        is_resend = False
        batch_num = 0
        while batch_num < len(batches):

            batch = batches[batch_num]
            packet_count = 1
            for i in range(len(batch)):
                packet = batch[i]

                # Do batch send - 5 packets then a stop packet
                if isinstance(packet, CCSDS_Chunk_Packet):
                    print(
                        f"Sending: packet {packet_count} from batch {batch_num+1}")

                elif isinstance(packet, CCSDS_Control_Packet):
                    print(f"Sending: Stop packet from batch {batch_num+1}")
                    print(packet)

                packet_count += 1
                ser_downlink.write(packet.get_tx_packet())

            if batch_num < len(batches) - 1:
                print("Wait for ack/nack")
                ack = ser_downlink.readline()
                print(ack)

                if ack == b"nack\r\n" or ack == b"":
                    print("Nack or timeout")
                    is_resend = True
                    ser_downlink.flush()

                else:
                    print(f"Received {ack}")
                    batch_num += 1
                print()
                time.sleep(TIME_BETWEEN_PACKETS * 5)

                if is_resend:
                    is_resend = False
                    print(f"Resending = {batch_num+1}")

            else:
                # Sleep first before sending start
                time.sleep(TIME_SLEEP_AFTER_START)
                break

    print("done!")

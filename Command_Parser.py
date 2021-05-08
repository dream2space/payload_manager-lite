from Command import Command, MissionDownlinkCommand
from os import read


class Command_Parser():
    def __init__(self):
        pass

    def parse(self, read_command):
        list_read = read_command.split(' ')

        if "md" in list_read:
            mission_type = list_read[0]
            num = list_read[1]
            interval = list_read[2]
            start_timestamp = list_read[3]
            down_timestamp = list_read[4]
            parsed_command = MissionDownlinkCommand(
                mission_type, num, interval, start_timestamp, down_timestamp)

        else:
            parsed_command = Command("unknown")

        return parsed_command

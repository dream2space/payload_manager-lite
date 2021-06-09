from os import read

from Command import Command, MissionDownlinkCommand


class Command_Parser():
    def __init__(self):
        pass

    def parse(self, read_command):

        # Debug to check ascii code of each char in string
        # print(f"read command is {[ord(c) for c in read_command]}")

        # If empty command
        if len(read_command) == 0:
            return Command("blank")

        list_read = read_command.split(' ')

        if "md" in list_read:
            mission_type = list_read[0]
            start_timestamp = list_read[1]
            num = list_read[2]
            interval = list_read[3]
            down_timestamp = list_read[4]

            try:
                parsed_command = MissionDownlinkCommand(
                    mission_type, num, interval, start_timestamp, down_timestamp)
            except ValueError:
                parsed_command = Command("unknown")

        else:
            parsed_command = Command("unknown")

        return parsed_command

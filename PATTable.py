""" PAT table """
from TSTable import TSTable

from BinaryPacketWrapper import BinaryPacketWrapper


class PATParseException(Exception):
    pass


class PATEntry:

    def __init__(self):
        self.program_num: int = 0
        self.reserved_bits: int = 0
        # PID of program map table
        self.program_map_pid: int = 0


class PATTable(TSTable):

    def __init__(self):
        super().__init__()

        self._entries = []

    def parse(self, wrapper: BinaryPacketWrapper):
        super().parse(wrapper)

        while self._section_parsed_bytes < self._section_length:
            entry = PATEntry()
            entry.program_num = int.from_bytes(wrapper.get_bytes(2), byteorder='big')
            self._section_parsed_bytes += 2

            pid_bytes = int.from_bytes(wrapper.get_bytes(2), byteorder='big')
            entry.reserved_bits = (pid_bytes & 0xe000) >> 13
            if entry.reserved_bits != 0x07:
                raise PATParseException('Invalid value of PAT entry reserved bits')

            entry.program_map_pid = (pid_bytes & 0x1fff)
            self._section_parsed_bytes += 2

            self._entries.append(entry)

    @property
    def entries(self):
        return self._entries

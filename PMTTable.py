""" PMT table """
from TSTable import TSTable

from BinaryPacketWrapper import BinaryPacketWrapper


class PMTParseException(Exception):
    pass


class PMTTable(TSTable):

    def __init__(self, program_num, pmt_pid):
        super().__init__()

        self._program_num = program_num
        self._associated_pids = []
        self._associated_pids.append(pmt_pid)

    def parse(self, wrapper: BinaryPacketWrapper):
        super().parse(wrapper)

        # Ignore reserved and PCR bits
        wrapper.get_bytes(2)
        self._section_parsed_bytes += 2

        # Get program info length
        wrapper.get_bytes(2)
        self._section_parsed_bytes += 2

        while self._section_parsed_bytes < self._section_length:
            wrapper.get_byte()
            self._section_parsed_bytes += 1

            # Get associated PID
            pid_bytes = int.from_bytes(wrapper.get_bytes(2), byteorder='big')
            self._section_parsed_bytes += 2
            associated_pid = pid_bytes & 0x1fff
            self._associated_pids.append(associated_pid)

            # Skip descriptors
            desc_len_bytes = int.from_bytes(wrapper.get_bytes(2), byteorder='big')
            self._section_parsed_bytes += 2
            desc_len = desc_len_bytes & 0x03ff
            wrapper.get_bytes(desc_len)
            self._section_parsed_bytes += desc_len

    @property
    def associated_pids(self):
        return self._associated_pids

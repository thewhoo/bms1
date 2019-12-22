""" Abstract TS table """
from abc import ABC, abstractmethod

from BinaryPacketWrapper import BinaryPacketWrapper


class TSTableParseException(Exception):
    pass


class TSTable(ABC):

    def __init__(self):
        # Table header values
        self._pointer_field: int = 0
        self._pointer_filler_bytes: bytes = None
        self._table_id: int = 0
        self._section_syntax_indicator: bool = False
        self._private_bit: bool = False
        self._reserved_bits: int = 0
        self._section_length_unused_bits: int = 0
        self._section_length: int = 0

        # Table syntax section values
        self._table_id_extension: int = 0
        self._syntax_reserved_bits: int = 0
        self._version_number: int = 0
        self._current_next_indicator: bool = False
        self._current_section_number: int = 0
        self._last_section_number: int = 0

        # Internal counters for determining if entire payload has been parsed
        self._section_parsed_bytes = 0
        self._discovered = False

    def _parse_header(self, wrapper: BinaryPacketWrapper):
        self._pointer_field = wrapper.get_byte()
        self._pointer_filler_bytes = wrapper.get_bytes(self._pointer_field)

        self._table_id = wrapper.get_byte()
        print(self._table_id)
        # Indicates that there is not a valid table after the end of the previous section
        # Rest of bytes in packet are 0xff stuffing
        if self._table_id == 0xff:
            print('skipping table')
            return

        # Parse 2 byte PSI header bitfield
        hdr_bytes = int.from_bytes(wrapper.get_bytes(2), byteorder='big')
        self._section_syntax_indicator = bool(hdr_bytes & 0x8000)
        self._private_bit = bool(hdr_bytes & 0x4000)
        self._reserved_bits = (hdr_bytes & 0x3000) >> 12
        self._section_length_unused_bits = (hdr_bytes & 0x0c00) >> 10
        # Substract the length of CRC32 at the end of section
        self._section_length = (hdr_bytes & 0x03ff) - 4

        print(f'section len: {self._section_length}')

        # Reserved bits should all be set
        if self._reserved_bits != 0x03:
            raise TSTableParseException(f'Invalid value of reserved bits {self._reserved_bits}')
        # Section length unused bits should all be 0
        if self._section_length_unused_bits != 0:
            raise TSTableParseException(
                f'Invalid value of section length unused bits {self._section_length_unused_bits}')

        # Parse syntax section if it follows
        if self._section_syntax_indicator:
            self._table_id_extension = int.from_bytes(wrapper.get_bytes(2), byteorder='big')
            self._section_parsed_bytes += 2

            flag_byte = wrapper.get_byte()
            self._section_parsed_bytes += 1
            self._syntax_reserved_bits = (flag_byte & 0xc0) >> 6
            if self._syntax_reserved_bits != 0x03:
                raise TSTableParseException('Invalid reserved bits in table syntax section')
            self._version_number = (flag_byte & 0x3e) >> 1
            self._current_next_indicator = bool(flag_byte & 0x01)

            self._current_section_number = wrapper.get_byte()
            self._section_parsed_bytes += 1

            self._last_section_number = wrapper.get_byte()
            self._section_parsed_bytes += 1

    def parse(self, wrapper: BinaryPacketWrapper):
        if not self._discovered:
            self._discovered = True
            self._parse_header(wrapper)

    @property
    def discovered(self):
        return self._discovered

    @property
    def parsed_entirely(self):
        return self._discovered and self._section_length == self._section_parsed_bytes

    @property
    def unfinished(self):
        return self.discovered and not self.parsed_entirely

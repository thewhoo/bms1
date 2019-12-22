""" PAT table """
from BinaryPacketWrapper import BinaryPacketWrapper


class PATTableParseException(Exception):
    pass


class PATTable:

    def __init__(self, wrapper: BinaryPacketWrapper, pusi: bool):

        if not pusi:
            return

        #if pusi:
        self._pointer_field = wrapper.get_byte()
        #if self._pointer_field > 0:
        print(f'pusi set, pointerf: {self._pointer_field}')
        self._pointer_filler_bytes = wrapper.get_bytes(self._pointer_field)
        for b in self._pointer_filler_bytes:
            print(f'pf byte: {b}')

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
        self._section_length = (hdr_bytes & 0x03ff)

        print(f'section len: {self._section_length}')

        # Check if syntax section follows section length
        if not self._section_syntax_indicator:
            pass
            #raise PATTableParseException('Section syntax indicator bit not set')
        # Check if private bit is unset
        if self._private_bit:
            #raise PATTableParseException('Private bit is set')
            pass
        # Reserved bits should all be set
        if self._reserved_bits != 0x03:
            #pass
            raise PATTableParseException(f'Invalid value of reserved bits {self._reserved_bits}')
        # Section length unused bits should all be 0
        if self._section_length_unused_bits != 0:
            #pass
            raise PATTableParseException(
                f'Invalid value of section length unused bits {self._section_length_unused_bits}')

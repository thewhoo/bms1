""" Class for MPEG2-TS packet data """
import typing

from BinaryPacketWrapper import BinaryPacketWrapper
from BinaryPacketWrapper import MPEGPacketBinaryReadException
from MPEGAdaptationField import MPEGAdaptationField
import MPEGAdaptationField
from TSData import TSData

HDR_SYNC_BYTE = 0xff000000  # Magic 0x47
HDR_TEI = 0x00800000  # Transport error indicator
HDR_PUSI = 0x00400000  # Payload unit start indicator
HDR_PRIORITY = 0x00200000  # Transport priority
HDR_PID = 0x001fff00  # Packet identifier
HDR_TSC = 0x000000c0  # Transport scrambling control
HDR_AFC = 0x00000030  # Adaptation field control
HDR_CCOUNTER = 0x0000000f  # Continuity counter


class MPEGParseException(Exception):
    pass


def parse_packet(wrapper: BinaryPacketWrapper, ts_data: TSData):
    if wrapper.current_read_bytes > 0:
        raise MPEGParseException('BinaryPacketWrapper offset is not at beginning of packet')

    header = int.from_bytes(wrapper.get_bytes(4), byteorder='big')
    hdr_sync_byte = (header & HDR_SYNC_BYTE) >> 24
    hdr_tei = bool((header & HDR_TEI))
    hdr_pusi = bool((header & HDR_PUSI))
    hdr_priority = bool((header & HDR_PRIORITY))
    hdr_pid = (header & HDR_PID) >> 8
    hdr_tsc = (header & HDR_TSC) >> 6
    hdr_afc = (header & HDR_AFC) >> 4
    hdr_continuity_counter = (header & HDR_CCOUNTER)

    if hdr_sync_byte != 0x47:
        raise MPEGParseException('Invalid sync_byte when parsing MPEG-TS header')

    MPEGAdaptationField.process_adaptation_field(wrapper, hdr_afc)

    # Attempt to parse PAT table if not already parsed
    if hdr_pid == 0 and not ts_data.has_pat_table:
        # print(f'PAT packet: {hdr_pid}')
        ts_data.pat_table.parse(wrapper)
    elif hdr_pid == 16 and not ts_data.has_nit_table:
        # print(f'NIT packet: {hdr_pid}')
        ts_data.nit_table.parse(wrapper)
    elif hdr_pid == 17 and not ts_data.has_sdt_table:
        # print(f'SDT packet: {hdr_pid}')
        ts_data.sdt_table.parse(wrapper)


"""
class MPEGPacket:

    def __init__(self, wrapper: BinaryPacketWrapper):
        if wrapper.current_read_bytes > 0:
            raise MPEGParseException('BinaryPacketWrapper offset is not at beginning of packet')

        header = int.from_bytes(wrapper.get_bytes(4), byteorder='big')

        self._sync_byte = (header & HDR_SYNC_BYTE) >> 24
        self._tei = bool((header & HDR_TEI))
        self._pusi = bool((header & HDR_PUSI))
        self._priority = bool((header & HDR_PRIORITY))
        self._pid = (header & HDR_PID) >> 8
        self._tsc = (header & HDR_TSC) >> 6
        self._afc = (header & HDR_AFC) >> 4
        self._continuity_counter = (header & HDR_CCOUNTER)

        if self._sync_byte != 0x47:
            raise MPEGParseException('Invalid sync_byte when parsing MPEG-TS header')

        # Parse potential adaptation field
        # print(f'afc: {self._afc}')
        if self._afc == 0x10 or self._afc == 0x11:
            if self._pusi:
                print(f'pusi set and afc: {self._afc}')
            self._adaptation_field = MPEGAdaptationField(wrapper)
        else:
            self._adaptation_field = None

        # Check if PSI table is present in this packet
        if self._pid == 0:
            print(f'pid: {self._pid}')
            self._pat_table = PATTable(wrapper, self._pusi)
        elif self._pid == 1:
            print(f'pid: {self._pid}')
            PATTable(wrapper, self._pusi)
        elif self._pid == 2:
            print(f'pid: {self._pid}')
            PATTable(wrapper, self._pusi)
        elif self._pid == 3:
            print(f'pid: {self._pid}')
            PATTable(wrapper, self._pusi)
        elif self._pid == 16:
            print(f'pid: {self._pid}')
            PATTable(wrapper, self._pusi)
        elif self._pid == 17:
            print(f'pid: {self._pid}, pusi: {self._pusi}, afc: {self._afc}')
            PATTable(wrapper, self._pusi)

        # self.dump_header()

    def dump_header(self):
        print(f'sync_byte: {self._sync_byte}')
        print(f'tei: {self._tei}')
        print(f'pusi: {self._pusi}')
        print(f'priority: {self._priority}')
        print(f'pid: {self._pid}')
        print(f'tsc: {self._tsc}')
        print(f'afc: {self._afc}')
        print(f'continuity_counter: {self._continuity_counter}')
"""

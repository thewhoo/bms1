""" Class for MPEG2-TS packet data """
import typing

from BinaryPacketWrapper import BinaryPacketWrapper
from BinaryPacketWrapper import MPEGPacketBinaryReadException
import MPEGAdaptationField

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


class MPEGPacket:

    def __init__(self, wrapper: BinaryPacketWrapper):
        if wrapper.current_read_bytes > 0:
            raise MPEGParseException('BinaryPacketWrapper offset is not at beginning of packet')

        header = int.from_bytes(wrapper.get_bytes(4), byteorder='big')

        self._sync_byte = (header & HDR_SYNC_BYTE) >> 24
        self._tei = (header & HDR_TEI) >> 23
        self._pusi = (header & HDR_PUSI) >> 22
        self._priority = (header & HDR_PRIORITY) >> 21
        self._pid = (header & HDR_PID) >> 8
        self._tsc = (header & HDR_TSC) >> 6
        self._afc = (header & HDR_AFC) >> 4
        self._continuity_counter = (header & HDR_CCOUNTER)

        if self._afc == 0x10 or self._afc == 0x11:
            self._adaptation_field = MPEGAdaptationField.MPEGAdaptationField(wrapper)
        else:
            self._adaptation_field = None

        if self._sync_byte != 0x47:
            raise MPEGParseException('Invalid sync_byte when parsing MPEG-TS header')

        #self.dump_header()

    def dump_header(self):
        print(f'sync_byte: {self._sync_byte}')
        print(f'tei: {self._tei}')
        print(f'pusi: {self._pusi}')
        print(f'priority: {self._priority}')
        print(f'pid: {self._pid}')
        print(f'tsc: {self._tsc}')
        print(f'afc: {self._afc}')
        print(f'continuity_counter: {self._continuity_counter}')

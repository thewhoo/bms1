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
        ts_data.pat_table.parse(wrapper)
    # Attempt to parse NIT table
    elif hdr_pid == 16 and not ts_data.has_nit_table:
        ts_data.nit_table.parse(wrapper)
    # Attempt to parse SDT table
    elif hdr_pid == 17 and not ts_data.has_sdt_table:
        ts_data.sdt_table.parse(wrapper)
    # Check if this is PMT of some program
    else:
        for e in ts_data.pat_table.entries:
            if hdr_pid == e.program_map_pid:
                print(f'found PMT for program {e.program_map_pid:04x}')

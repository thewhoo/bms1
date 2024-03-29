""" MPEG2-TS Adaptation field """
import typing

from BinaryPacketWrapper import BinaryPacketWrapper


class MPEGAFParseException(Exception):
    pass


def process_adaptation_field(wrapper: BinaryPacketWrapper, afc_flag: int):
    # Check if AF control flag indicates presence of adaptation field
    if afc_flag != 0x10 and afc_flag != 0x11:
        return

    af_length = wrapper.get_byte()
    if af_length < 1:
        raise MPEGAFParseException('Invalid adaptation field length')

    wrapper.seek(af_length)


class MPEGAdaptationField:

    def __init__(self, wrapper: BinaryPacketWrapper):
        self._length = wrapper.get_byte()
        if self._length < 1:
            raise MPEGAFParseException('Invalid adaptation field length')

        af_byte = wrapper.get_byte()
        self._discontinuity_indicator = bool(af_byte & 0x80)
        self._random_access_indicator = bool(af_byte & 0x40)
        self._priority_indicator = bool(af_byte & 0x20)
        self._pcr_flag = bool(af_byte & 0x10)
        self._opcr_flag = bool(af_byte & 0x08)
        self._splicing_point_flag = bool(af_byte & 0x04)
        self._transport_private_data_flag = bool(af_byte & 0x02)
        self._af_extension_flag = bool(af_byte & 0x01)

        # Skip over potential AF extension fields
        wrapper.seek(self._length - 1)

""" Wrapper over MPEG2-TS packet binary IO """
import typing
import io

PKT_BYTE_COUNT = 188


class MPEGPacketBinaryReadException(Exception):
    pass


class BinaryPacketWrapper:

    def __init__(self, fp: typing.BinaryIO):
        self._fp = fp
        self._pkt_read_count = 0
        self._read_bytes = 0

    def get_bytes(self, count):
        if self._read_bytes + count > PKT_BYTE_COUNT:
            raise MPEGPacketBinaryReadException('Attempting to read bytes over packet length')

        pkt_bytes = self._fp.read(count)
        self._read_bytes += count
        if len(pkt_bytes) < count:
            raise MPEGPacketBinaryReadException(f'Failed to read {count} bytes from file')

        return pkt_bytes

    def get_byte(self):
        return self.get_bytes(1)[0]

    def seek_packet(self):
        self._fp.seek(PKT_BYTE_COUNT - self._read_bytes, io.SEEK_CUR)
        self._pkt_read_count += 1
        self._read_bytes = 0

    @property
    def pkt_read_count(self):
        return self._pkt_read_count

    @property
    def current_read_bytes(self):
        return self._read_bytes

    @property
    def is_eof(self):
        pkt_bytes = self._fp.read(1)
        if len(pkt_bytes) > 0:
            self._fp.seek(-1, io.SEEK_CUR)
            return False
        else:
            return True

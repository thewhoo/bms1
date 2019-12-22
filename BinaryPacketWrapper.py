""" Wrapper over MPEG2-TS packet binary IO """
import typing
import io
import itertools

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

    def seek(self, offset):
        if self._read_bytes + offset > PKT_BYTE_COUNT:
            raise MPEGPacketBinaryReadException('Attempting to seek over packet length')

        self._fp.seek(offset, io.SEEK_CUR)
        self._read_bytes += offset

    def next_packet(self):
        self.seek(PKT_BYTE_COUNT - self._read_bytes)
        self._pkt_read_count += 1
        self._read_bytes = 0

    # Allow automatic transfer to next packet
    def get_bytes_auto_shift(self, count):
        if self._read_bytes + count > PKT_BYTE_COUNT:
            # Read in rest of bytes in current packet
            remaining = count - (PKT_BYTE_COUNT - self._read_bytes)
            pkt_bytes = self.get_bytes(PKT_BYTE_COUNT - self._read_bytes)
            # Move to next packet
            self.next_packet()
            self.get_bytes(4)
            return bytes(itertools.chain(pkt_bytes, self.get_bytes(remaining)))
        else:
            return self.get_bytes(count)

    def get_byte_auto_shift(self):
        return self.get_bytes_auto_shift(1)[0]

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

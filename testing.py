import sys
import MPEGPacket
from BinaryPacketWrapper import BinaryPacketWrapper

TS_PACKET_LEN = 188
HELP = './bms1 transport_stream.ts'

if len(sys.argv) != 2:
    print(HELP)
    exit(1)
else:
    tsfile = sys.argv[1]

with open(tsfile, 'rb') as f:
    w = BinaryPacketWrapper(f)
    while not w.is_eof:
        MPEGPacket.MPEGPacket(w)
        w.seek_packet()

    print(f"pkts read: {w.pkt_read_count}")

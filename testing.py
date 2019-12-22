import sys
import MPEGPacket
from BinaryPacketWrapper import BinaryPacketWrapper
from TSData import TSData

TS_PACKET_LEN = 188
HELP = './bms1 transport_stream.ts'

if len(sys.argv) != 2:
    print(HELP)
    exit(1)
else:
    tsfile = sys.argv[1]

with open(tsfile, 'rb') as f:
    w = BinaryPacketWrapper(f)
    ts_data = TSData()
    while not w.is_eof:
        MPEGPacket.parse_packet(w, ts_data)
        w.next_packet()

    print(f'Network name: {ts_data.nit_table.network_name}')
    print(f'Network ID: {ts_data.nit_table.network_id}')
    print(f'Bandwidth: {ts_data.nit_table.bandwidth}')
    print(f'Constellation: {ts_data.nit_table.constellation}')
    print(f'Guard interval: {ts_data.nit_table.guard_interval}')
    print(f'Code rate: {ts_data.nit_table.code_rate}')
    print('')

    for e in ts_data.pat_table.entries:
        if e.program_num != 0:
            print(f'0x{e.program_map_pid:04x}-{ts_data.sdt_table.providers[e.program_num]}-{ts_data.sdt_table.svcnames[e.program_num]}')

    print(f"pkts read: {w.pkt_read_count}")
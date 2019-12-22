""" NIT table """
from TSTable import TSTable

from BinaryPacketWrapper import BinaryPacketWrapper


class NITTable(TSTable):

    def __init__(self):
        super().__init__()
        self._network_name: str = ''

        # Terrestrial parameters
        self._bandwidth: str = ''
        self._constellation: str = ''
        self._guard_interval: str = ''
        self._code_rate: str = ''

        self._network_name_set = False
        self._terrestrial_params_set = False

        self._parsed = False

    def _parse_descriptor_section(self, wrapper: BinaryPacketWrapper):
        descriptor_bytes = int.from_bytes(wrapper.get_bytes(2), byteorder='big') & 0x0fff

        descriptor_read_bytes = 0
        while descriptor_read_bytes < descriptor_bytes:
            descriptor_tag = wrapper.get_byte()
            descriptor_len = wrapper.get_byte()
            descriptor_read_bytes += 2

            # Check for network name descriptor
            if descriptor_tag == 0x40 and not self._network_name_set:
                name = wrapper.get_bytes(descriptor_len)
                self._network_name = name.decode('utf-8')
                self._network_name_set = True
            elif descriptor_tag == 0x5A and not self._terrestrial_params_set:
                # Skip to bandwidth
                wrapper.get_bytes(4)

                # Bandwidth
                bw_field = wrapper.get_byte()
                bw_val = (bw_field & 0xe0) >> 5
                self._bandwidth = f'{8 - bw_val} MHz'

                # Constellation
                cs_field = wrapper.get_byte()
                cs_val = (cs_field & 0xc0) >> 6
                if cs_val == 0x0:
                    self._constellation = 'QPSK'
                elif cs_val == 0x1:
                    self._constellation = '16-QAM'
                elif cs_val == 0x2:
                    self._constellation = '64-QAM'

                # Guard interval and code rate
                gi_field = wrapper.get_byte()
                gi_val = (gi_field & 0x18) >> 3
                cr_val = (gi_field & 0xe0) >> 5
                self._guard_interval = f'1/{32 >> gi_val}'
                if cr_val == 0x0:
                    self._code_rate = '1/2'
                elif cr_val == 0x1:
                    self._code_rate = '2/3'
                elif cr_val == 0x2:
                    self._code_rate = '3/4'
                elif cr_val == 0x3:
                    self._code_rate = '5/6'
                elif cr_val == 0x4:
                    self._code_rate = '7/8'

                # Skip rest
                wrapper.get_bytes(4)

                self._terrestrial_params_set = True
            else:
                wrapper.get_bytes(descriptor_len)

            descriptor_read_bytes += descriptor_len

        return descriptor_bytes + 2

    def parse(self, wrapper: BinaryPacketWrapper):
        super().parse(wrapper)
        self._parsed = True

        self._parse_descriptor_section(wrapper)

        ts_loop_len = int.from_bytes(wrapper.get_bytes(2), byteorder='big') & 0x0fff
        ts_loop_read_bytes = 0
        while ts_loop_read_bytes < ts_loop_len:
            ts_stream_id = int.from_bytes(wrapper.get_bytes(2), byteorder='big')
            orig_net_id = int.from_bytes(wrapper.get_bytes(2), byteorder='big')
            ts_loop_read_bytes += 4
            ts_loop_read_bytes += self._parse_descriptor_section(wrapper)

    @property
    def parsed_entirely(self):
        return self._parsed

    @property
    def network_name(self):
        return self._network_name

    @property
    def network_id(self):
        return self._table_id_extension

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def constellation(self):
        return self._constellation

    @property
    def guard_interval(self):
        return self._guard_interval

    @property
    def code_rate(self):
        return self._code_rate

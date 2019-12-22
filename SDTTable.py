""" SDT table """
from TSTable import TSTable

from BinaryPacketWrapper import BinaryPacketWrapper


class SDTTable(TSTable):

    def __init__(self):
        super().__init__()

        self._svcid_provider = {}
        self._svcid_svcname = {}

    def _parse_descriptor_section(self, wrapper: BinaryPacketWrapper, svcid: int):
        descriptor_bytes = int.from_bytes(wrapper.get_bytes_auto_shift(2), byteorder='big') & 0x0fff

        descriptor_read_bytes = 0
        while descriptor_read_bytes < descriptor_bytes:
            descriptor_tag = wrapper.get_byte_auto_shift()
            descriptor_len = wrapper.get_byte_auto_shift()
            descriptor_read_bytes += 2

            # Check for network name descriptor
            if descriptor_tag == 0x48:
                # Skip service type
                wrapper.get_byte_auto_shift()
                # Get provider name
                provider_name_len = wrapper.get_byte_auto_shift()
                provider_name = wrapper.get_bytes_auto_shift(provider_name_len).decode('utf-8')
                self._svcid_provider[svcid] = provider_name
                # Get service name
                service_name_len = wrapper.get_byte_auto_shift()
                service_name = wrapper.get_bytes_auto_shift(service_name_len).decode('utf-8')
                self._svcid_svcname[svcid] = service_name
            else:
                wrapper.get_bytes_auto_shift(descriptor_len)

            descriptor_read_bytes += descriptor_len

        return descriptor_bytes + 2

    def parse(self, wrapper: BinaryPacketWrapper):
        super().parse(wrapper)

        # Skip original network id and reserved byte
        wrapper.get_bytes(3)
        self._section_parsed_bytes += 3

        while self._section_parsed_bytes < self._section_length:
            # Get service id
            svc_id = int.from_bytes(wrapper.get_bytes_auto_shift(2), byteorder='big')
            self._section_parsed_bytes += 2

            # Skip to descriptors
            wrapper.get_byte_auto_shift()
            self._section_parsed_bytes += 1

            self._section_parsed_bytes += self._parse_descriptor_section(wrapper, svc_id)

    @property
    def providers(self):
        return self._svcid_provider

    @property
    def svcnames(self):
        return self._svcid_svcname

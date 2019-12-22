""" NIT table """
from TSTable import TSTable

from BinaryPacketWrapper import BinaryPacketWrapper


class NITTable(TSTable):

    def __init__(self):
        super().__init__()

    def parse(self, wrapper: BinaryPacketWrapper):
        pass

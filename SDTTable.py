""" SDT table """
from TSTable import TSTable

from BinaryPacketWrapper import BinaryPacketWrapper


class SDTTable(TSTable):

    def __init__(self):
        super().__init__()

    def parse(self, wrapper: BinaryPacketWrapper):
        super().parse(wrapper)
        #print('run sdtt parse')

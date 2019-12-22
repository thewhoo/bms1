""" Abstract TS table """
from abc import ABC, abstractmethod

from BinaryPacketWrapper import BinaryPacketWrapper


class TSTable(ABC):

    def __init__(self):
        self._total_length = 0
        self._parsed_bytes = 0
        self._discovered = False

    @abstractmethod
    def parse(self, wrapper: BinaryPacketWrapper):
        pass

    @property
    def discovered(self):
        return self._discovered

    @property
    def parsed_entirely(self):
        return self._discovered and self._total_length == self._parsed_bytes

    @property
    def unfinished(self):
        return self.discovered and not self.parsed_entirely

""" Class for storing metadata for entire transport stream """
from TSTable import TSTable
from SDTTable import SDTTable
from NITTable import NITTable
from PATTable import PATTable


class TSData:

    def __init__(self):
        self._pat_table: PATTable = PATTable()
        self._nit_table: NITTable = NITTable()
        self._sdt_table: SDTTable = SDTTable()

    @property
    def pat_table(self):
        return self._pat_table

    @property
    def nit_table(self):
        return self._nit_table

    @property
    def sdt_table(self):
        return self._sdt_table

    @property
    def has_pat_table(self):
        return self._pat_table.parsed_entirely

    @property
    def has_nit_table(self):
        return self._nit_table.parsed_entirely

    @property
    def has_sdt_table(self):
        return self._sdt_table.parsed_entirely

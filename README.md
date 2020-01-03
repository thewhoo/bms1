# BMS project (BMS 2019/2020)

DVB-T MPEG2-TS metadata parser. BinaryPacketWrapper is responsible for reading raw packets from the input file (tries to maintain packet boundaries and prevent you from reading in nonsense).

TSTable is a base class which can parse the header of SDT, PAT and NIT TS tables.

Use at your own discretion, licensed under the MIT license.

from email.headerregistry import Address
import struct
import sys
import smbus

bus = smbus.SMBus(1)


address = 0x48


def readVoltage(bus, address=address):
    read = bus.read_word_data(address, 2)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = swapped * (78.125 / 1000000)
    return voltage


def readCapacity(bus, address=address):
    read = bus.read_word_data(address, 4)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped / 256
    return capacity

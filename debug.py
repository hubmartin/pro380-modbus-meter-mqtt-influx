#!/usr/bin/env python3
import time
import struct
import json
import paho.mqtt.client
from influxdb import InfluxDBClient
from serial import Serial, PARITY_EVEN

from umodbus.client.serial import rtu

def get_data(start = 0x4000, length = 0x02):
    message = rtu.read_holding_registers(slave_id = 1, starting_address = start, quantity = length)
    response = rtu.send_message(message, serial_port)

    count = 0
    data = {}

    while count < len(response):
        h = format(response[count + 0], '04X')
        l = format(response[count + 1], '04X')
        d = h + l
        val = struct.unpack('!f', bytes.fromhex(d))[0]
        key = str(format(start + count, '04X'))
        data[key] = val
        count += 2

    return data

def get_tariff():
    message = rtu.read_holding_registers(slave_id = 1, starting_address = 0x6048, quantity = 1)
    response = rtu.send_message(message, serial_port)
    tariff = [-1, 1, 0]
    print(response)
    return {"tariff_val" : tariff[response[0]]}

# MODBUS serial RTU
serial_port = Serial(port='/dev/ttyUSB485', baudrate=9600, parity=PARITY_EVEN, stopbits=1, bytesize=8, timeout=1)

print("Serial port connected")

once = True
counter = 0
while once:
    power_values = get_data(start = 0x5000, length = 0x32)
    energy_values = get_data(start = 0x6000, length = 0x3c)
    tariff = get_tariff()

    print(power_values['5012'])

    #once = False
    print("counter", counter, " modulo", counter % 30)
    counter += 1
    time.sleep(1)

serial_port.close()

from machine import I2C, Pin
import time

class HTU21D:
    ADDRESS = 0x40
    TRIGGER_TEMP = 0xE3
    TRIGGER_HUMID = 0xE5

    def __init__(self, i2c):
        self.i2c = i2c

    def _read_sensor(self, command):
        self.i2c.writeto(self.ADDRESS, bytes([command]))
        time.sleep_ms(50)
        data = self.i2c.readfrom(self.ADDRESS, 3)
        raw = (data[0] << 8) | data[1]
        raw &= 0xFFFC  # clear status bits
        return raw

    def temperature(self):
        raw = self._read_sensor(self.TRIGGER_TEMP)
        return -46.85 + (175.72 * raw / 65536)

    def humidity(self):
        raw = self._read_sensor(self.TRIGGER_HUMID)
        return -6 + (125.0 * raw / 65536)

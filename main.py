from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from tsl2561 import TSL2561
from htu21d import HTU21D
import network
import ubinascii
import time

i2c = I2C(0, scl=Pin(4), sda=Pin(5), freq=100000)

oled = SSD1306_I2C(128, 64, i2c)

light_sensor = TSL2561(i2c)
light_sensor.active(True) 
climate_sensor = HTU21D(i2c)
led = Pin(14, Pin.OUT)

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32_AP", password="esp32pass", authmode=3) 

print("Access Point started with SSID 'ESP32_AP'")

connected_macs = set()

while True:
    try:
        #For reading measurements from sensors
        lux = light_sensor.read(autogain=True) 
        temp = climate_sensor.temperature()    
        hum = climate_sensor.humidity()

        #For controlling LED based on luminosity
        if lux < 1:
            led.on()
        else:
            led.off()

        #OLED display
        oled.fill(0)
        oled.text("Light: {:.1f}lx".format(lux), 0, 0)
        oled.text("Temp: {:.1f} C".format(temp), 0, 10)
        oled.text("Humidity: {:.1f}%".format(hum), 0, 20)
        oled.show()

        #Checking for Wi-Fi connected devices
        stations = ap.status('stations')
        current_macs = set()
        for station in stations:
            mac_bytes = station[0]
            mac = ubinascii.hexlify(mac_bytes, ':').decode()
            current_macs.add(mac)

        #Detecting and listing new Wi-Fi connections
        new_macs = current_macs - connected_macs
        for mac in new_macs:
            print(f"New device connected: {mac}")

        connected_macs = current_macs

        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        time.sleep(2)

import network
import time
from machine import Pin, I2C

import ssd1306


    
i2c = I2C(0, scl=Pin(4), sda=Pin(5))

# Initialize OLED Display (128x64 resolution)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display
oled.fill(0)


oled.text("hellow world", 0, 0)

oled.show()

time.sleep(3)

oled.fill(0)


count = 0

wlan = network.WLAN(network.STA_IF)  # Set ESP32 as a station
wlan.active(True)  # Activate Wi-Fi

ssid = "master"
password = "1648195h"



while not wlan.isconnected():
    oled.fill(0)
    
    if count == 4 :
        break
    
    try:
        if not wlan.isconnected():
            wlan.connect(ssid, password)
            print('its connecting')
            count = count +1
            mess = f"its connecting"
            mess2 = f"step = {count}"
            oled.text(mess, 0, 0)
            oled.text(mess2 , 0 , 16)
            oled.show()
            time.sleep(4)
    except OSError as e :
         oled.text("wifi error", 0, 0)
         oled.show()


oled.fill(0)

if wlan.isconnected():
    oled.text("connected:", 0, 0)
    oled.text(f"{wlan.ifconfig()[0]}",0,16)
    oled.show()
    time.sleep(4)

else:
    oled.text("it never connects", 0, 16)
    oled.show()
    
    


import urequests
import ssd1306

try:
  import usocket as socket
except:
  import socket
  
import network
import time

from machine import Pin, I2C


import esp
esp.osdebug(None)

import gc
gc.collect()


#Initialize I2C
i2c = I2C(0, scl=Pin(4), sda=Pin(5))

# Initialize OLED Display (128x64 resolution)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display
oled.fill(0)

#Display text
oled.text("in the main.py", 0, 0)
# oled.text("MicroPython OLED", 0, 16)
# 
oled.show()


led = Pin(7 , Pin.OUT)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)



file  = open('file.html' , 'rt')

lines = file.readlines()

string = ''

for i in lines:
    string = string + i + "\n"


#socket programming to send request to micro controller
while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  oled.fill(0)
  oled.text('Got connection from ', 0, 0)
  oled.text(str(addr), 0, 20)
  oled.show()

  
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  
  if led_on == 6:
    print('LED ON')
    led.value(1)
    oled.fill(0)
    oled.text("led is on", 0, 0)
    oled.show()
    
    state = 'on'
    other2 = 'null'
    url1 = f'https://infinitysmart.ir/add?state={state}&other2={other2}'

    response = urequests.get(url1)
    oled.text(f"{response.text}", 0, 20) 
    oled.show()
    
  elif led_off == 6:
    print('LED OFF')
    led.value(0)
    oled.fill(0)
    oled.text("led is off", 0, 0)
    oled.show()
    
    state = 'off'
    other2 = 'null'
    url2 = f'https://infinitysmart.ir/add?state={state}&other2={other2}'

    response = urequests.get(url2)
    oled.text(f"{response.text}", 0, 20) 
    oled.show()
    
  else:
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(string)
    conn.close()


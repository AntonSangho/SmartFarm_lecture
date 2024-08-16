from machine import Pin
from machine import I2C

# PicoW Pin assignment
#sdaPIN = Pin(8) # SDA
#sclPIN = Pin(9) # SCL

sdaPIN = Pin(14) # SDA
sclPIN = Pin(15) # SCL

i2c = I2C(1, sda=sdaPIN, scl=sclPIN) #0번 I2C 사용
devices = i2c.scan() # I2C 장치 검색

if len(devices) == 0:
    print("No I2C device")
else:
    print("I2C device found :", len(devices))

#for device in devices:
    #print(" Hexa address: ", hex(device))

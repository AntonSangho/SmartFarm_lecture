# Fan control with GPIO pin26 with 2N3904 NPN transistor in Micropython
# Control Fan with button state change.


import machine
import utime

# Pin 11 set to output
fan = machine.Pin(14, machine.Pin.OUT)

# Pin 3 set to input
button = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

# fan on and off state change with button state change



# fan on and off with while loop 

while True:
    #fan.on()
    #utime.sleep(5)
    fan.off()
    utime.sleep(0)




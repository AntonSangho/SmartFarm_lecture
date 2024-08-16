from machine import Pin, SoftI2C, PWM
import utime
from neopixel import NeoPixel
import ssd1306
from ds3231_port import DS3231
import ahtx0


# 네오픽셀과 환풍기 핀 초기화
Rled = Pin(9, Pin.OUT)
Fan = machine.Pin(26, machine.Pin.OUT)
np0 = NeoPixel(machine.Pin(2), 30)
np1 = NeoPixel(machine.Pin(15), 30)
Rbutton = Pin(3, Pin.IN, Pin.PULL_UP)
Lbutton = Pin(14, Pin.IN, Pin.PULL_UP)

#OLED 초기화
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# I2C에 연결된 DS3231 초기화
ds3231 = DS3231(i2c) 
print('DS3231 time:', ds3231.get_time())

# AHT20 초기화 
#i2c=machine.I2C(0,sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN), freq=400000)
#i2c=machine.I2C(i2c)
sensor = ahtx0.AHT20(i2c)

# Buzzer 초기화 
buzzer = PWM(Pin(7))
buzzer.freq(800)
buzzer.duty_u16(1000)
utime.sleep(3)
buzzer.duty_u16(0)

# 버튼 상태를 추적하는 변수 초기화
Rbutton_state = False
Lbutton_state = False

# 네오픽셀 상태를 추적하는 변수 초기화 
def np_on():
    for i in range(0, np0.n):
        np0[i] = (250,250,250)
    for i in range(0, np1.n):
        np1[i] = (250,250,250)
    np0.write()
    np1.write()
def np_off():
    for i in range(0, np0.n):
        np0[i] = (0,0,0)
    for i in range(0, np1.n):
        np1[i] = (0,0,0)
    np0.write()
    np1.write()

# 버튼이 눌렸을 때 호출될 핸들러 함수 정의
def Rbutton_handler(pin):
    global Rbutton_state
    # 버튼 상태 전환
    Rbutton_state = not Rbutton_state
    if Rbutton_state == True:
        # Buzzer indicator  
        oled.fill(0)
        oled.show()
        oled.text('Fan On', 0, 10)
        oled.show()
    else:
        oled.fill(0)
        oled.show()
        oled.text('Fan Off', 0, 10)
        oled.show()
        
    print("Fan_state:", end =' ')
    print(Rbutton_state)
    Rled.value(Rbutton_state)
    Fan.value(Rbutton_state)

def Lbutton_handler(pin):
    global Lbutton_state
    # 버튼 상태 전환
    Lbutton_state = not Lbutton_state
    if Lbutton_state == True:
        # Buzzer indicator
        oled.fill(0)
        oled.show()
        oled.text('Neopixel On', 0, 10)
        oled.show()
    else:
        oled.fill(0)
        oled.show()
        oled.text('Neopixel Off', 0, 10)
        oled.show()
    print("Neopixel_state:", end =' ' )
    print(Lbutton_state)
    # np_on or np off
    if Lbutton_state == True:
        np_on()
    else:
        np_off()


# 버튼에 핸들러 등록
Rbutton.irq(trigger=Pin.IRQ_FALLING, handler=Rbutton_handler)
Lbutton.irq(trigger=Pin.IRQ_FALLING, handler=Lbutton_handler)

while True:
    #oled.fill(0)
    #current_time = ds3231.get_time()
    #formatted_time = "{:02}:{:02}".format(current_time[3], current_time[4])
    #oled.text(formatted_time, 0, 0)
    #oled.show()
    #utime.sleep(10)
    print(sensor.relative_humidity)
    utime.sleep(1)
#while True:
    #oled.fill(0)
    #oled.show()
    #oled.text(ds3231.get_time(), 0, 0)
    ##utime.sleep(0.1)
    #utime.sleep(1)

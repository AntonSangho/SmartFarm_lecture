"""
DataPi_v1.py
"""
import random
from machine import Pin, SoftI2C, PWM 
import utime
from neopixel import NeoPixel
import ssd1306
from machine import RTC
from ds3231_port import DS3231
import AHT21
import ENS160

# 상태변수 
sensging_active = False
recording_active = False
recording_interval = 10   
file = None

# LED, 버튼, 부저 설정
Led = Pin("LED", Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(22))

# RTC I2C 포트를 설정합니다.
i2c0 = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
rtc = DS3231(i2c0)

# OLED 픽셀 크기 설정
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c0)

# AHT21 I2C 포트를 설정합니다.
i2c1 = machine.I2C(1,scl=machine.Pin(15), sda=machine.Pin(14),freq=400000)
aht = AHT21.AHT21(i2c1)

# 가스 센서 I2C 포트를 설정합니다. 
ens = ENS160.ENS160(i2c1)
ens.reset()
utime.sleep(0.5)
ens.operating_mode = 2
#utime.sleep(2.0)

# 파일 생성 
f = open('data.csv', 'a')

def record_data():
    # 온습도 센서에서 데이터 읽기
    rht = aht.read()
    humidity = rht[0]
    temperature = rht[1]
    # 가스 센서에서 데이터 읽기
    aqi:int = ens.AQI
    eco2:int = ens.CO2
    tvoc:int = ens.TVOC

    now = rtc.get_time()
    print("Time: {}/{} {}:{}:{}".format(now[1], now[2], now[3], now[4], now[5]))
    print("Humidity: {:.2f}%".format(humidity))
    print("Temperature: {:.2f}C".format(temperature))
    print("AQI: {}, ECO2: {}, TVOC: {}".format(aqi, eco2, tvoc))
    oled.fill(0)
    oled.text("[TeamName]", 0, 0)
    oled.text("Time: {}:{}:{}".format(now[3], now[4], now[5]), 0, 10)
    oled.text("Temp: {:.2f}C".format(temperature), 0, 20)
    oled.text("Humid: {:.2f}%".format(humidity), 0, 30)
    oled.text("ECO2: {}".format(eco2), 0, 40)
    oled.text("TVOC: {}".format(tvoc), 0, 50)

    oled.show() 
    # 파일에 데이터 기록
    f.write("{}/{} {}:{}:{},{:.2f},{:.2f},{},{},{}\n".format(now[1], now[2], now[3], now[4], now[5], humidity, temperature, aqi, eco2, tvoc))

    utime.sleep(1)  

# 부저를 울리는 함수
def button_buzzer(freq):
    buzzer.duty_u16(30000)
    buzzer.freq(freq)
    utime.sleep(0.1)
    buzzer.duty_u16(0)

# 부팅을 알리는 부저 소리
def start_buzzer():
    buzzer.freq(1000)
    buzzer.duty_u16(30000)
    utime.sleep(0.1)
    buzzer.freq(2000)
    buzzer.duty_u16(30000)
    utime.sleep(0.1)
    buzzer.freq(3000)
    buzzer.duty_u16(30000)
    utime.sleep(0.1)
    buzzer.duty_u16(0)


# 버튼의 상태를 추적하는 변수 초기화    
button_state = False
countdown_start_time = None 

# 버튼이 눌렸을 때 호출될 핸들러 함수 정의
def button_handler(pin):
    global recording_active, file
    if pin.value() == 0:  # 버튼이 눌렸을 때
        recording_active = not recording_active
        if recording_active:
            print("기록을 시작합니다.")
            oled.fill(0)
            oled.text("Recording", 0, 0)
            oled.show()
            Led.value(1)
            np_on()
            button_buzzer(2000)
            file = open('data.csv', 'a')
        else:
            print("기록을 중지합니다.")
            oled.fill(0)
            oled.text("Stop", 0, 0)
            oled.show()
            np_off()
            button_buzzer(2000)
            if file:
                Led.value(0)
                file.close()
                np_off()
    global button_state, countdown_start_time
    # 버튼 상태 전환
    button_state = not button_state
    if button_state == True:
        countdown_start_time = utime.ticks_ms()
        np_on()
        record_data()
    else:
        np_off()
    
# 버튼에 핸들러 등록
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# 네오픽셀 핀 초기화
np = NeoPixel(machine.Pin(21), 1)

# 네오픽셀 상태를 추적하는 변수 초기화 
def np_on():
    for i in range(0, np.n):
        np[i] = (70,50,20)
    np.write()
def np_off():
    for i in range(0, np.n):
        np[i] = (0,0,0)
    np.write()

# ds3231으로 부터 시간을 가져오는 함수 정의
def get_time():
    rtc = RTC()
    return rtc.datetime()

start_buzzer()
while True:
    if recording_active:
        record_data()
        utime.sleep(recording_interval)
    else:
        Led.value(0)
    

from machine import Pin, SoftI2C, PWM
import time
from neopixel import NeoPixel
import ssd1306
from ds3231_port import DS3231
import AHT21
import ENS160

# 핀 설정
led = Pin('LED', Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_UP)
fan = Pin(10, Pin.OUT)
buzzer = PWM(Pin(22))  # 부저 핀 설정

# I2C 및 센서 초기화
i2c0 = SoftI2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c0)
rtc = DS3231(i2c0)

i2c1 = SoftI2C(scl=Pin(15), sda=Pin(14))
aht = AHT21.AHT21(i2c1)
ens = ENS160.ENS160(i2c1)
ens.reset()
time.sleep(0.5)
ens.operating_mode = 2

# 네오픽셀 초기화 (핀 6, 7 사용)
np1 = NeoPixel(Pin(6), 30)
np2 = NeoPixel(Pin(7), 30)

# 버튼 상태 변수
button_state = False

# 부저 음 출력 함수
def play_buzzer(freq):
    buzzer.duty_u16(30000)  # 볼륨 설정
    buzzer.freq(freq)  # 주파수 설정
    time.sleep(0.1)
    buzzer.duty_u16(0)  # 부저 끄기

# 버튼 눌림 이벤트 처리 함수
def button_handler(pin):
    global button_state
    button_state = not button_state

    if button_state:
        play_buzzer(1000)  # 시작 시 부저 소리
        display_message("Start")
        activate_fan_and_neopixel()
        time.sleep(1)  # 'Start' 메시지 유지 시간
        display_sensor_data()
    else:
        play_buzzer(500)  # 종료 시 부저 소리
        display_message("Stop")
        deactivate_fan_and_neopixel()
        time.sleep(1)  # 'Stop' 메시지 유지 시간
        clear_display()

# 버튼 인터럽트 설정
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# OLED에 메시지 표시 함수
def display_message(msg):
    oled.fill(0)
    oled.text(msg, 0, 30)
    oled.show()

# 센서 데이터 표시 함수
def display_sensor_data():
    now = rtc.get_time()
    rht = aht.read()
    humidity = rht[0]
    temperature = rht[1]
    eco2 = ens.CO2
    tvoc = ens.TVOC

    oled.fill(0)
    oled.text(f"Time: {now[3]:02}:{now[4]:02}:{now[5]:02}", 0, 0)
    oled.text(f"Temp: {temperature:.2f}C", 0, 10)
    oled.text(f"Humid: {humidity:.2f}%", 0, 20)
    oled.text(f"ECO2: {eco2}", 0, 30)
    oled.text(f"TVOC: {tvoc}", 0, 40)
    oled.show()

# 팬과 네오픽셀 활성화 함수 (보라색)
def activate_fan_and_neopixel():
    fan.value(1)
    for i in range(np1.n):
        np1[i] = (255, 0, 255)  # 보라색
    np1.write()

    for i in range(np2.n):
        np2[i] = (255, 0, 255)  # 보라색
    np2.write()

# 팬과 네오픽셀 비활성화 함수
def deactivate_fan_and_neopixel():
    fan.value(0)
    for i in range(np1.n):
        np1[i] = (0, 0, 0)  # 끄기
    np1.write()

    for i in range(np2.n):
        np2[i] = (0, 0, 0)  # 끄기
    np2.write()

# 디스플레이 지우기 함수
def clear_display():
    oled.fill(0)
    oled.show()

# 메인 루프
while True:
    time.sleep(0.1)  # CPU 사용률 절감을 위한 지연


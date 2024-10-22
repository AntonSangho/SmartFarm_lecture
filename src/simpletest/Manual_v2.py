"""
코드 설명 
버튼을 누르면 환풍기가 작동하고, 네오픽셀이 켜지며 부저가 울립니다.
"""

from machine import Pin, PWM
import time
from neopixel import NeoPixel
# 환풍기 핀 초기화
led = Pin('LED', Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_UP)
Fan = machine.Pin(10, machine.Pin.OUT)
buzzer = PWM(Pin(22))  # 부저 핀 설정

# 버튼 상태를 추적하는 변수 초기화
button_state = False

# 버튼이 눌렸을 때 호출될 핸들러 함수 정의
def button_handler(pin):
    global button_state
    # 버튼 상태 전환
    button_state = not button_state
    if button_state == True:
        np0_on()
        np1_on()
        np2_on()
        play_buzzer(1000)
        print("On")
    else:
        np0_off()
        np1_off()
        np2_off()
        play_buzzer(500)
        print("Off")

# 부저 음 출력 함수
def play_buzzer(freq):
    buzzer.duty_u16(30000)  # 볼륨 설정
    buzzer.freq(freq)  # 주파수 설정
    time.sleep(0.1)
    buzzer.duty_u16(0)  # 부저 끄기

# 부팅을 알리는 부저 소리
def start_buzzer():
    buzzer.freq(1000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    buzzer.freq(2000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    buzzer.freq(3000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    buzzer.duty_u16(0)

   
# 버튼에 핸들러 등록
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# 네오픽셀 핀 초기화
np0 = NeoPixel(machine.Pin(21), 1)
np1 = NeoPixel(machine.Pin(6), 30)
np2 = NeoPixel(machine.Pin(7), 30)

# 네오픽셀 상태를 추적하는 변수 초기화 
def np0_on():
    for i in range(0, np0.n):
        np0[i] = (255,0,255)
    np0.write()
    Fan.value(button_state)
def np0_off():
    for i in range(0, np0.n):
        np0[i] = (0,0,0)
    np0.write()
    Fan.value(button_state)
def np1_on():
    for i in range(0, np1.n):
        np1[i] = (255,0,255)
    np1.write()
    Fan.value(button_state)
def np1_off():
    for i in range(0, np1.n):
        np1[i] = (0,0,0)
    np1.write()
    Fan.value(button_state)
def np2_on():
    for i in range(0, np2.n):
        np2[i] = (255,0,255)
    np2.write()
    Fan.value(button_state)
def np2_off():
    for i in range(0, np2.n):
        np2[i] = (0,0,0)
    np2.write()
    Fan.value(button_state)

# 부팅 소리
start_buzzer()
while True:
    time.sleep(0.1)


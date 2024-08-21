"""
네오픽셀을 켜고 끄는 의사코드.
1. 네오픽셀 핀 설정
2. 네오픽셀 함수 정수
3. 무한 루프
    4. 네오픽셀 켜기
    5. 1초 대기
    6. 네오픽셀 끄기
    7. 1초 대기

"""

from machine import Pin
import time
from neopixel import NeoPixel
# 환풍기 핀 초기화
led = Pin('LED', Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_UP)

# 버튼 상태를 추적하는 변수 초기화
button_state = False

# 버튼이 눌렸을 때 호출될 핸들러 함수 정의
def button_handler(pin):
    global button_state
    # 버튼 상태 전환
    button_state = not button_state
    if button_state == True:
        np1_on()
        np2_on()
    else:
        np1_off()
        np2_off()
    
# 버튼에 핸들러 등록
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# 네오픽셀 핀 초기화
np1 = NeoPixel(machine.Pin(13), 30)
np2 = NeoPixel(machine.Pin(14), 30)

# 네오픽셀 상태를 추적하는 변수 초기화 
def np1_on():
    for i in range(0, np1.n):
        np1[i] = (255,0,0)
    np1.write()
def np1_off():
    for i in range(0, np1.n):
        np1[i] = (0,0,0)
    np1.write()

def np2_on():
    for i in range(0, np2.n):
        np2[i] = (0,255,0)
    np2.write()
def np2_off():
    for i in range(0, np2.n):
        np2[i] = (0,0,0)
    np2.write()


while True:
    # 네오픽셀 켜기
    #np1_on()
    #np2_on()
    time.sleep(1)
    # 네오픽셀 끄기
    #np1_off()
    #np2_off()
    #time.sleep(1)


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

# 네오픽셀 핀 초기화
np0 = NeoPixel(machine.Pin(21), 1)

# 네오픽셀 상태를 추적하는 변수 초기화 
def np_on():
    for i in range(0, np0.n):
        np0[i] = (255,0,0)
    np0.write()
def np_off():
    for i in range(0, np0.n):
        np0[i] = (0,0,0)
    np0.write()

while True:
    # 네오픽셀 켜기
    #np_on()
    #time.sleep(1)
    # 네오픽셀 끄기
    np_off()
    time.sleep(1)




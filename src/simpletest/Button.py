"""
버튼을 누르면 LED가 꺼지고, 버튼을 누르지 않으면 LED가 켜지는 의사코드 

1. LED 핀 설정
2. 버튼 핀 설정
3. 무한 루프
    4. 버튼의 상태 확인
    5. 버튼이 눌렸을 때
        6. LED 끄기
    7. 버튼이 눌리지 않았을 때
        8. LED 켜기
    9. 0.1초 대기
"""

from machine import Pin
from utime import sleep
import utime 

led = Pin('LED', Pin.OUT)

# GPIO 20번 핀에 연결된 버튼을 입력 모드로 설정합니다. 내부 풀업 저항을 활성화합니다.
button = Pin(20, Pin.IN, Pin.PULL_UP)


# 무한 루프를 통해 버튼의 상태를 지속적으로 확인하고 LED를 제어합니다.
while True:
    # button의 상태를 출력합니다. (눌렸을 때 0, 눌리지 않았을 때 1)
    print(button.value())

    if button.value() == 0:
        led.value(False)
    else:
        led.value(True)

    # 0.1초마다 반복합니다.
    utime.sleep(0.1)




"""
"""

from machine import Pin
from utime import sleep
import utime 

# 글로벌 변수를 선언합니다.
button_pressed_count = 0

def button1_pressed(change):
    global button_pressed_count
    button_pressed_count += 1

button1 = Pin(20, Pin.IN, Pin.PULL_UP)
button1.irq(handler=button1_pressed, trigger=Pin.IRQ_FALLING)

button_pressed_count_old = 0

led = Pin('LED', Pin.OUT)

# GPIO 20번 핀에 연결된 버튼을 입력 모드로 설정합니다. 내부 풀업 저항을 활성화합니다.
#button = Pin(20, Pin.IN, Pin.PULL_UP)


# 무한 루프를 통해 버튼의 상태를 지속적으로 확인하고 LED를 제어합니다.
while True:
    # 버튼이 눌렸을 때 LED를 켭니다.
    if button_pressed_count_old != button_pressed_count:
        print('Button 1 value :', button_pressed_count)
        button_pressed_count_old = button_pressed_count

    # button의 상태를 출력합니다. (눌렸을 때 0, 눌리지 않았을 때 1)
    #print(button.value())

    #if button.value() == 0:
    #    led.value(False)
    #else:
    #    led.value(True)

    ## 0.1초마다 반복합니다.
    #utime.sleep(0.1)




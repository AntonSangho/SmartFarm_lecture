"""
의사코드
1. 버튼을 누르면 환풍기가 작동하고, 버튼을 누르지 않으면 환풍기가 작동하지 않는다.
2. 버튼을 누르면 버튼의 상태를 출력한다.
"""

from machine import Pin
import utime

# 환풍기 핀 초기화
led = Pin('LED', Pin.OUT)
Fan = machine.Pin(10, machine.Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_UP)

# 버튼 상태를 추적하는 변수 초기화
button_state = False

# 버튼이 눌렸을 때 호출될 핸들러 함수 정의
def button_handler(pin):
    global button_state
    # 버튼 상태 전환
    button_state = not button_state
    print("환풍기에 입력 값:", end =' ')
    print(button_state)
    led.value(button_state)
    Fan.value(button_state)

# 버튼에 핸들러 등록
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

while True:
    utime.sleep(1)


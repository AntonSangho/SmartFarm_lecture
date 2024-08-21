"""
의사코드
1. 버튼을 누르면 환풍기가 켜지고 10초 동안 작동한다.
2. 10초가 지나면 환풍기가 꺼진다.
3. 버튼을 다시 누르면 10초 카운트가 다시 시작된다.
4. 환풍기가 켜져 있을 때는 버튼을 눌러도 아무 일도 일어나지 않는다.
5. 환풍기가 꺼져 있을 때는 버튼을 누르면 환풍기가 켜진다.

"""

from machine import Pin
import utime

# 환풍기 핀 초기화
led = Pin(25, Pin.OUT)
Fan = machine.Pin(14, machine.Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_UP)
count = 0

# 버튼 상태를 추적하는 변수 초기화
button_state = False

# 10초 타이머 시작 시간 초기화
start_time = utime.ticks_ms()

# 버튼이 눌렸을 때 호출될 핸들러 함수 정의

def button_handler(pin):
    global button_state
    global count
    # 버튼 상태 전환
    button_state = not button_state
    print("환풍기에 입력 값:", end =' ')
    print(button_state)
    led.value(button_state)
    Fan.value(button_state)

    if button_state: # 버튼이 눌려서 팬이 켜질 때
        count = 10   # 10초 카운트다운 
        start_time = utime.ticks_ms()
    
# 버튼에 핸들러 등록
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

while True:
    if button_state and count > 0 :# 팬이 켜져 있고 카운트다운이 진행 중일 때 
        print(f"남은 시간: {count}초")
        count -= 1
        utime.sleep(1)
       
        if count <=0 :# 카운트다운이 끝났을 때  
            Fan.value(False)
            led.value(False)
            button_state = False
            print("팬이 꺼졌습니다.")
    else:
        utime.sleep(1)


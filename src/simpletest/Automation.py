"""
"""
import random
from machine import Pin, SoftI2C 
import utime
from neopixel import NeoPixel
import ssd1306
from machine import RTC

# 환풍기 핀 초기화
led = Pin('LED', Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_UP)

# OLED i2c 통신 설정
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

# OLED 픽셀 크기 설정
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# 버튼의 상태를 추적하는 변수 초기화    
button_state = False
countdown_start_time = None 

# 버튼이 눌렸을 때 호출될 핸들러 함수 정의
def button_handler(pin):
    global button_state, countdown_start_time
    # 버튼 상태 전환
    button_state = not button_state
    if button_state == True:
        countdown_start_time = utime.ticks_ms()
        #np_on()
    else:
        np_off()
    
# 버튼에 핸들러 등록
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# 네오픽셀 핀 초기화
np = NeoPixel(machine.Pin(21), 1)

# 네오픽셀 상태를 추적하는 변수 초기화 
def np_on():
    for i in range(0, np.n):
        np[i] = (160,160,160)
    np.write()
def np_off():
    for i in range(0, np.n):
        np[i] = (0,0,0)
    np.write()

# ds3231으로 부터 시간을 가져오는 함수 정의
def get_time():
    rtc = RTC()
    return rtc.datetime()


while True:
    utime.sleep(1)
    # OLED 화면 초기화 (기존 내용 지우기)
    oled.fill(0)
    
    # OLED 화면에 rtc 시간 출력 
    current_time = get_time()
    oled.text("Time: ", 0, 0)
    oled.text("{:02d}:{:02d}:{:02d}".format(current_time[4], current_time[5], current_time[6]), 0, 10)

    if button_state and countdown_start_time is not None:
        # 경과 시간 계산 
        elapsed_time = utime.ticks_diff(utime.ticks_ms(), countdown_start_time)//1000
        # 남은 시간 계산 
        remaining_time = 10 - elapsed_time 
        if remaining_time >0:
            np_on()
            print(f"남은 시간: {remaining_time}초")
        else:
            np_off()
            button_state = False
            countdown_start_time = None
            
    # OLED 화면에 출력
    oled.show()



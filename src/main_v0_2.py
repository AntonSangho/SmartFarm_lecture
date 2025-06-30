import time, machine
from ds3231_port import DS3231
from machine import I2C, Pin, PWM
import ahtx0
from bh1750 import BH1750
import neopixel
import ssd1306  # OLED 디스플레이 라이브러리 추가

#--------- 핀 설정 및 센서 초기화 ---------#

# 내장 LED 설정
led = Pin('LED', Pin.OUT)

# 버튼 설정 (눌렀을 때 0, 평소에는 1을 반환하는 PULL_UP 방식)
button = Pin(20, Pin.IN, Pin.PULL_UP)

# 부저 설정
buzzer = PWM(Pin(22))

# NeoPixel LED 설정 (핀 21, 12개의 LED)
np0 = neopixel.NeoPixel(Pin(21), 12)

# I2C 버스 0번 설정 (RTC, 조도 센서, OLED용)
i2c0 = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
# 시간 모듈(RTC) 초기화
rtc = DS3231(i2c0)
# 조도 센서 초기화
bh1750 = BH1750(0x23, i2c0)

# OLED 디스플레이 설정 (128x64 해상도)
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c0)

# 온습도 센서 통신 설정
i2c1 = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)
# 온습도 센서 초기화
sensor = ahtx0.AHT20(i2c1)

# 기록 간격 설정 (30분 = 1800초)
recording_interval = 1
last_record_time = 0
data_file = None

# LED 조명 켜기/끄기 시간 설정 (24시간 형식)
# 이 값을 직접 수정하여 LED 켜기/끄기 시간을 변경할 수 있습니다
light_on_hour = 6    # LED 켜는 시간 (시)
light_on_minute = 0   # LED 켜는 시간 (분)
light_off_hour = 19    # LED 끄는 시간 (시)
light_off_minute = 0  # LED 끄는 시간 (분)

# LED 색상 설정
LED_COLOR = (80, 40, 220)  # 성장기에 좋은 색으로 설정 (보라색)
LED_STANDBY_COLOR = (255, 0, 0)  # 대기 상태일 때 색상 (빨간색)

#--------- 기능 함수 정의 ---------#

# 네오픽셀 켜기 (전체)
def np_on():
    for i in range(0, np0.n):
        np0[i] = LED_COLOR  # 성장기에 좋은 색으로 설정 (보라색)
    np0.write()  # LED에 변경사항 적용

# 네오픽셀 끄기 (대기 모드: 첫 번째만 빨간색)
def np_standby():
    for i in range(0, np0.n):
        if i == 0:  # 첫 번째 LED만 빨간색으로 설정
            np0[i] = LED_STANDBY_COLOR
        else:
            np0[i] = (0, 0, 0)  # 나머지 LED는 끄기
    np0.write()  # LED에 변경사항 적용

# 네오픽셀 완전히 끄기
def np_off():
    for i in range(0, np0.n):
        np0[i] = (0, 0, 0)  # LED 끄기 (검은색)
    np0.write()  # LED에 변경사항 적용

# OLED 디스플레이 업데이트 함수
def update_oled_display(recording_active, temperature, humidity, light, now):
    oled.fill(0)  # 화면 지우기
    
    # 첫 번째 줄: 버전 정보와 상태
    if recording_active:
        oled.text("[v0.1] Recording", 0, 0)
    else:
        oled.text("[v0.1] Standby", 0, 0)
    
    # 두 번째 줄: 현재 시간
    oled.text("Time: {:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5]), 0, 10)
    
    # 세 번째 줄: 온도
    oled.text("Temp: {:.1f}C".format(temperature), 0, 20)
    
    # 네 번째 줄: 습도
    oled.text("Humid: {:.1f}%".format(humidity), 0, 30)
    
    # 다섯 번째 줄: 조도
    oled.text("Light: {:.1f}lux".format(light), 0, 40)
    
    # 여섯 번째 줄: LED 상태
    if recording_active:
        if is_light_on_time():
            oled.text("LED: ON", 0, 50)
        else:
            oled.text("LED: STANDBY", 0, 50)
    else:
        oled.text("LED: OFF", 0, 50)
    
    oled.show()  # 화면에 표시

# 현재 시간이 LED를 켜야 할 시간인지 확인 (하루를 넘어가는 경우도 처리)
def is_light_on_time():
    now = rtc.get_time()  # 현재 시간 가져오기
    current_hour = now[3]  # 현재 시간 (시)
    current_minute = now[4]  # 현재 시간 (분)
    
    # 현재 시간을 분 단위로 변환 (예: 8시 30분 -> 510분)
    current_time_in_minutes = current_hour * 60 + current_minute
    
    # 켜는 시간과 끄는 시간을 분 단위로 변환
    on_time_in_minutes = light_on_hour * 60 + light_on_minute
    off_time_in_minutes = light_off_hour * 60 + light_off_minute
    
    # 하루를 넘어가는 경우 (켜는 시간이 끄는 시간보다 크거나 같은 경우)
    # 예: 켜는 시간 19:00, 끄는 시간 06:00인 경우
    if on_time_in_minutes >= off_time_in_minutes:
        # 현재 시간이 켜는 시간 이후이거나 끄는 시간 이전이면 켜짐
        return current_time_in_minutes >= on_time_in_minutes or current_time_in_minutes < off_time_in_minutes
    else:
        # 일반적인 경우 (같은 날에 켜고 끄는 경우)
        return on_time_in_minutes <= current_time_in_minutes < off_time_in_minutes

# 현재 시간 디버깅 출력 함수
def print_current_time():
    now = rtc.get_time()  # 현재 시간 가져오기
    print("현재 시간: {:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
        now[0], now[1], now[2], now[3], now[4], now[5]))
    
    # 켜는/끄는 시간 분단위로 변환
    current_hour = now[3]  # 현재 시간 (시)
    current_minute = now[4]  # 현재 시간 (분)
    current_time_in_minutes = current_hour * 60 + current_minute
    on_time_in_minutes = light_on_hour * 60 + light_on_minute
    off_time_in_minutes = light_off_hour * 60 + light_off_minute
    
    print("현재 시간(분): {}, 켜는 시간(분): {}, 끄는 시간(분): {}".format(
        current_time_in_minutes, on_time_in_minutes, off_time_in_minutes))
    
    # 하루를 넘어가는 경우 표시
    if on_time_in_minutes >= off_time_in_minutes:
        print("하루를 넘어가는 설정입니다 (밤->아침)")
    else:
        print("같은 날 내에서 설정되었습니다")
        
    print("LED 켜야 하나요? {}".format(is_light_on_time()))

# 버튼 눌렀을 때 짧은 부저음
def button_buzzer(freq):
    buzzer.duty_u16(30000)  # 부저 켜기 (소리 크기 설정)
    buzzer.freq(freq)       # 주파수 설정 (높은 값 = 높은 소리)
    time.sleep(0.1)         # 0.1초 동안 소리내기
    buzzer.duty_u16(0)      # 부저 끄기

# 프로그램 시작 시 멜로디 부저음
def start_buzzer():
    # 점점 높아지는 3단계 소리
    buzzer.freq(1000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    
    buzzer.freq(2000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    
    buzzer.freq(3000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    
    buzzer.duty_u16(0)  # 부저 끄기

# 데이터 기록 함수
def record_data():
    global data_file, last_record_time
    
    # 현재 시간 가져오기
    now = rtc.get_time()
    current_time = time.time()
    
    # 센서에서 데이터 읽기
    humidity = sensor.relative_humidity
    temperature = sensor.temperature
    light = bh1750.measurement
    
    # 측정값 출력
    print("Time: {:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
        now[0], now[1], now[2], now[3], now[4], now[5]))
    print("Humidity: {:.2f}%".format(humidity))
    print("Temperature: {:.2f}C".format(temperature))
    print("Light: {:.2f} lux".format(light))
    
    # OLED 디스플레이 업데이트 (매번 호출)
    update_oled_display(recording_active, temperature, humidity, light, now)
    
    # 파일이 없으면 열기
    if data_file is None:
        try:
            data_file = open('data.csv', 'a')
            # 빈 파일인지 확인하고 필요하면 헤더 추가
            if data_file.seek(0, 2) == 0:  # 파일 끝이 0이면 빈 파일
                data_file.write("Time, Temperature, Humidity, Light\n")
        except:
            print("파일을 열 수 없습니다.")
            return
    
    # 정해진 간격마다 데이터 기록
    if current_time - last_record_time >= recording_interval:
        try:
            # 파일에 데이터 기록
            data_file.write("{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}, {:.2f}, {:.2f}, {:.2f}\n".format(
                now[0], now[1], now[2], now[3], now[4], now[5], 
                temperature, humidity, light))
            
            # 버퍼에 있는 데이터를 즉시 디스크에 기록
            data_file.flush()
            
            # 파일을 닫았다가 다시 열어 데이터 안전성 확보
            data_file.close()
            data_file = open('data.csv', 'a')
            
            last_record_time = current_time
            print("데이터 기록 완료!")
        except Exception as e:
            print("데이터 기록 중 오류 발생:", e)

# 대기 모드에서 OLED 표시 함수
def show_standby_display():
    now = rtc.get_time()
    
    # 센서 데이터 읽기 (대기 모드에서도 현재 상태 표시)
    try:
        humidity = sensor.relative_humidity
        temperature = sensor.temperature
        light = bh1750.measurement
        
        # OLED에 대기 상태 표시
        update_oled_display(False, temperature, humidity, light, now)
        
    except Exception as e:
        # 센서 읽기 실패 시 기본 정보만 표시
        oled.fill(0)
        oled.text("[v0.1] Standby", 0, 0)
        oled.text("Time: {:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5]), 0, 10)
        oled.text("Sensor Error", 0, 20)
        oled.text("Press button", 0, 30)
        oled.text("to start", 0, 40)
        oled.show()

#--------- 메인 프로그램 ---------#

# 상태 변수 초기화
recording_active = False  # 기록 활성화 상태
button_pressed = False    # 버튼 상태 추적
last_light_check = 0      # 마지막으로 조명 상태를 확인한 시간
light_status = False      # LED 상태 추적 (True: 켜짐, False: 꺼짐 또는 대기)
last_display_update = 0   # 마지막 디스플레이 업데이트 시간

# 시작 시 설정
np_off()                  # 네오픽셀 끄기
led.on()                  # 내장 LED 켜기 (프로그램 실행 중 표시)
start_buzzer()            # 시작 멜로디 재생

# OLED 초기 화면 표시
oled.fill(0)
oled.text("[v0.1] Starting", 0, 0)
oled.text("System ready", 0, 20)
oled.text("Press button", 0, 30)
oled.text("to start recording", 0, 40)
oled.show()

# 안내 메시지 출력
print("프로그램이 시작되었습니다.")
print("온습도,조도를 측정합니다.")
print("버튼을 누르면 기록과 네오픽셀이 시작/중지됩니다.")
print("현재 LED 켜는 시간: {:02d}시 {:02d}분, 끄는 시간: {:02d}시 {:02d}분".format(
    light_on_hour, light_on_minute, light_off_hour, light_off_minute))

# 시작할 때 현재 시간과 LED 상태 확인
print_current_time()

try:
    # 메인 루프
    while True:
        # 1. 버튼 상태 확인 및 처리
        if button.value() == 0 and not button_pressed:  # 버튼이 새로 눌렸을 때
            button_pressed = True  # 버튼 상태 기록
            
            # 기록 상태 전환 (켜기 <-> 끄기)
            recording_active = not recording_active
            
            if recording_active:
                print("기록이 시작되었습니다.")
                # LED 상태를 시간에 따라 즉시 설정 (현재 시간 바로 확인)
                print_current_time()  # 디버깅을 위해 현재 시간 출력
                current_time = time.time()
                last_light_check = current_time - 10  # 강제로 LED 상태 업데이트 발생시키기
                
                button_buzzer(2000)   # 시작 부저음 (높은 음)
                
                # 파일 열기
                if data_file is None:
                    data_file = open('data.csv', 'a')
                    # 빈 파일이면 헤더 추가
                    if data_file.seek(0, 2) == 0:
                        data_file.write("Time, Temperature, Humidity, Light\n")
                
                # 시작하자마자 첫 기록 수행
                last_record_time = time.time() - recording_interval  # 즉시 기록되도록 설정
            else:
                print("기록과 네오픽셀이 중지되었습니다.")
                np_off()              # 네오픽셀 끄기
                button_buzzer(1000)   # 중지 부저음 (낮은 음)
                
                # 파일 안전하게 닫기
                if data_file is not None:
                    data_file.flush()
                    data_file.close()
                    data_file = None
                
            # 버튼이 떼어질 때까지 대기 (중복 인식 방지)
            while button.value() == 0:
                time.sleep(0.1)
                
        elif button.value() == 1 and button_pressed:  # 버튼이 떼어졌을 때
            button_pressed = False  # 버튼 상태 초기화
            time.sleep(0.2)         # 디바운스 (버튼 신호 안정화)
        
        # 2. 기록이 활성화된 경우 데이터 측정 및 저장, LED 상태 업데이트
        if recording_active:
            # 데이터 기록 (OLED 업데이트 포함)
            record_data()
            
            # 1초마다 시간에 따라 LED 상태 업데이트 (더 빠른 응답성)
            current_time = time.time()
            if current_time - last_light_check >= 1:  # 5초에서 1초로 변경
                if is_light_on_time():
                    # LED 켜는 시간 - LED 끄는 시간 사이면 모든 LED 켜기
                    np_on()
                    # 상태가 변경되었을 때만 메시지 출력
                    if not light_status:
                        print("네오픽셀이 켜졌습니다 (LED 켜는 시간대: {:02d}:{:02d}-{:02d}:{:02d})".format(
                            light_on_hour, light_on_minute, light_off_hour, light_off_minute))
                        print_current_time()  # 디버깅을 위해 현재 시간 출력
                        light_status = True
                else:
                    # 그 외 시간은 대기 모드 (첫 LED만 빨간색)
                    np_standby()
                    # 상태가 변경되었을 때만 메시지 출력
                    if light_status:
                        print("네오픽셀이 대기 모드입니다 (LED 끄는 시간대: {:02d}:{:02d}-{:02d}:{:02d})".format(
                            light_off_hour, light_off_minute, light_on_hour, light_on_minute))
                        print_current_time()  # 디버깅을 위해 현재 시간 출력
                        light_status = False
                last_light_check = current_time
        else:
            # 3. 대기 모드에서도 주기적으로 OLED 디스플레이 업데이트
            current_time = time.time()
            if current_time - last_display_update >= 5:  # 5초마다 디스플레이 업데이트
                show_standby_display()
                last_display_update = current_time
        
        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:  # Ctrl+C로 프로그램 중단 시
    pass
finally:  # 프로그램 종료 시 항상 실행
    print("프로그램을 종료합니다.")
    
    # 종료 메시지를 OLED에 표시
    oled.fill(0)
    oled.text("Shutting down...", 0, 20)
    oled.text("Goodbye!", 0, 30)
    oled.show()
    time.sleep(2)
    
    np_off()               # 네오픽셀 끄기
    oled.fill(0)           # OLED 화면 끄기
    oled.show()
    button_buzzer(500)     # 프로그램 종료 부저음 (매우 낮은 음)
    
    # 파일 안전하게 닫기
    if data_file is not None:
        data_file.flush()
        data_file.close()
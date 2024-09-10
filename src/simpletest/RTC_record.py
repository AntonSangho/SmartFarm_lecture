import time, machine
import AHT21
from ds3231_port import DS3231
from machine import I2C
import ssd1306

# RTC I2C 포트를 설정합니다.
i2c0 = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
rtc = DS3231(i2c0)
    
# OLED 디스플레이를 설정합니다.
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c0)

# AHT21 I2C 포트를 설정합니다.
i2c1 = machine.I2C(1,scl=machine.Pin(15), sda=machine.Pin(14),freq=400000)
# 온습도 센서와 RTC 센서를 연결합니다.
aht = AHT21.AHT21(i2c1)

f = open('data.csv', 'a')
f.write("Time, Temperature, Humidity\n")

print("ATH21의 온도와 습도를 측정합니다.")

def record_data():
    while True :
        now = rtc.get_time()
        rht = aht.read()
        humidity = rht[0]
        temperature = rht[1]
        # format: 년도, 월, 일, 요일, 시간, 분, 초 
        print("Time: {}/{}/{} {}:{}:{}".format(now[0], now[1], now[2], now[3], now[4], now[5]))
        print("Humidity: {:.2f}%".format(humidity))
        print("Temperature: {:.2f}C".format(temperature))
        # OLED에 시간, 온도, 습도를 표시합니다.
        oled.fill(0)
        oled.text("Date: {}/{}/{}".format(now[0], now[1], now[2]), 0, 0)
        oled.text("Time: {}:{}:{}".format(now[3], now[4], now[5]), 0, 10)
        oled.text("Temp: {:.2f}C".format(temperature), 0, 20)
        oled.text("Humid: {:.2f}%".format(humidity), 0, 30)
        oled.show()
        # 시간, 분, 초, 온도, 습도를 파일에 저장합니다.
        f.write("{}/{}/{} {}:{}:{}, {:.2f}, {:.2f}\n".format(now[0], now[1], now[2], now[3], now[4], now[5], temperature, humidity))
        # 기록 주기를 1초로 설정합니다.
        time.sleep(1)

try:
    record_data()
except KeyboardInterrupt:
    pass
finally:
    print("프로그램을 종료합니다.")
    f.close()





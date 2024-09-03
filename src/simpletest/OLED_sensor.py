from machine import Pin, SoftI2C
import ssd1306
import AHT21

# 온도 센서 i2c 통신 
i2c = machine.I2C(1,scl=machine.Pin(15), sda=machine.Pin(14),freq=400000)
aht = AHT21.AHT21(i2c)

# OLED i2c 통신 설정
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

# OLED 픽셀 크기 설정
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

while True :
    rht = aht.read()
    #print(rht)
    humidity = rht[0]
    temperature = rht[1]
    
     # 출력 내용 포맷팅
    humidity_text = "Humid: {:.2f}%".format(humidity)
    temperature_text = "Temp: {:.2f}C".format(temperature)
    
    # 콘솔에 출력 (디버깅용)
    print(humidity_text)
    print(temperature_text)
    
    # OLED 화면 초기화 (기존 내용 지우기)
    oled.fill(0)
    
    # OLED 화면에 텍스트 출력
    oled.text(humidity_text, 0, 0)    # 습도
    oled.text(temperature_text, 0, 10)  # 온도
    
    # OLED 화면에 출력
    oled.show()


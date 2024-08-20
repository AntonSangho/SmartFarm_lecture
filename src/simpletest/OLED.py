'''
의사코드
1. 라이브러리 import
2. I2C 객체 생성
3. OLED 객체 생성
4. OLED 객체에 문자열 출력
5. OLED 화면에 출력
'''

from machine import Pin, SoftI2C
import ssd1306

# i2c 통신 설정
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

# OLED 픽셀 크기 설정
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# OLED 화면에 문자열 출력
oled.text('Hello, World 1!', 0, 0)
oled.text('Hello, World 2!', 0, 10)
oled.text('Hello, World 3!', 0, 20)

# OLED 화면에 출력
oled.show()

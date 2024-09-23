"""
DataPi_v1_2.py
"""
import random
import utime
from machine import Pin, SoftI2C, PWM, RTC
from neopixel import NeoPixel
import ssd1306
from ds3231_port import DS3231
import AHT21
import ENS160

# Constants for pin numbers and other configurations
LED_PIN = "LED"
BUTTON_PIN = 20
BUZZER_PIN = 22
I2C0_SCL_PIN = 5
I2C0_SDA_PIN = 4
I2C1_SCL_PIN = 15
I2C1_SDA_PIN = 14
OLED_WIDTH = 128
OLED_HEIGHT = 64
RECORDING_INTERVAL = 1

# State variables
sensing_active = False
recording_active = False
file = None

# Initialize hardware components
def initialize_hardware():
    global Led, button, buzzer, rtc, oled, aht, ens, file

    # LED, button, buzzer setup
    Led = Pin(LED_PIN, Pin.OUT)
    button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
    button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)
    buzzer = PWM(Pin(BUZZER_PIN))

    # RTC I2C port setup
    i2c0 = SoftI2C(scl=Pin(I2C0_SCL_PIN), sda=Pin(I2C0_SDA_PIN), freq=400000)
    rtc = DS3231(i2c0)

    # OLED display setup
    oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c0)

    # AHT21 I2C port setup
    i2c1 = SoftI2C(scl=Pin(I2C1_SCL_PIN), sda=Pin(I2C1_SDA_PIN), freq=400000)
    aht = AHT21.AHT21(i2c1)

    # Gas sensor I2C port setup
    ens = ENS160.ENS160(i2c1)
    ens.reset()
    utime.sleep(0.5)
    ens.operating_mode = 2

    # Open data file
    file = open('data.csv', 'a')

# Function to handle button press
def button_handler(pin):
    global recording_active
    recording_active = not recording_active
    if recording_active:
        print("Recording started")
    else:
        print("Recording stopped")

# 부팅을 알리는 부저 소리
def start_buzzer():
    buzzer.freq(1000)
    buzzer.duty_u16(30000)
    utime.sleep(0.1)
    buzzer.freq(2000)
    buzzer.duty_u16(30000)
    utime.sleep(0.1)
    buzzer.freq(3000)
    buzzer.duty_u16(30000)
    utime.sleep(0.1)
    buzzer.duty_u16(0)

# 부저를 울리는 함수
def button_buzzer(freq):
    buzzer.duty_u16(30000)
    buzzer.freq(freq)
    utime.sleep(0.1)
    buzzer.duty_u16(0)

# Record data from sensors
def record_data():
    # Read data from AHT21 sensor
    rht = aht.read()
    humidity = rht[0]
    temperature = rht[1]

    # Read data from ENS160 sensor
    aqi = ens.AQI
    eco2 = ens.CO2
    tvoc = ens.TVOC

    # Get current time from RTC
    now = rtc.get_time()

    # Print data to console
    print("Time: {}/{} {}:{}:{}".format(now[1], now[2], now[3], now[4], now[5]))
    print("Humidity: {:.2f}%".format(humidity))
    print("Temperature: {:.2f}C".format(temperature))
    print("AQI: {}, ECO2: {}, TVOC: {}".format(aqi, eco2, tvoc))

    # Display data on OLED
    oled.fill(0)
    oled.text("[TeamName]", 0, 0)
    oled.text("Time: {}:{}:{}".format(now[3], now[4], now[5]), 0, 10)
    oled.text("Temp: {:.2f}C".format(temperature), 0, 20)
    oled.text("Humid: {:.2f}%".format(humidity), 0, 30)
    oled.text("ECO2: {}".format(eco2), 0, 40)
    oled.show()

    # Write data to file
    file.write("{}/{} {},{},{},{:.2f},{:.2f},{},{},{}\n".format(now[1], now[2], now[3], now[4], now[5], humidity, temperature, aqi, eco2, tvoc))

    # Start the buzzer for 1 second
    start_buzzer()

    utime.sleep(1)


# Main function
def main():
    initialize_hardware()
    start_buzzer()
    while True:
        if recording_active:
            record_data()
            utime.sleep(RECORDING_INTERVAL)

if __name__ == "__main__":
    main()

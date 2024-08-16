import time, machine
import AHT21

i2c = machine.I2C(1,scl=machine.Pin(15), sda=machine.Pin(14),freq=400000)
aht = AHT21.AHT21(i2c)

print("ATH21의 온도와 습도를 측정합니다.")

while True:
    rht = aht.read()
    #print(rht)
    humidity = rht[0]
    temperature = rht[1]
    print("Humidity: {:.2f}%".format(humidity))
    print("Temperature: {:.2f}C".format(temperature))
    time.sleep(1)




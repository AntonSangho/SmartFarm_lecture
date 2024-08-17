import time, machine
import AHT21
import os 

i2c = machine.I2C(1,scl=machine.Pin(15), sda=machine.Pin(14),freq=400000)
aht = AHT21.AHT21(i2c)
f = open('data.csv', 'a')
f.write("Time, Temperature, Humidity\n")

print("ATH21의 온도와 습도를 측정합니다.")

def record_data():
    while True :
        rht = aht.read()
        print(rht)
        humidity = rht[0]
        temperature = rht[1]
        print("Humidity: {:.2f}%".format(humidity))
        print("Temperature: {:.2f}C".format(temperature))
        f.write("{:.2f}, {:.2f}\n".format(temperature, humidity))
        time.sleep(1)

try:
    record_data()
except KeyboardInterrupt:
    pass
finally:
    print("프로그램을 종료합니다.")
    f.close()





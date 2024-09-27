from machine import Pin
import utime
led = Pin("LED", Pin.OUT)
def write_to_file(text):
    try:
        led.value(1)
        with open("test.txt", "a") as file:
            file.write("{} - {}\n".format(text, utime.localtime()))
            file.flush()  # 바로 저장
        led.value(0)
    except:
        led.value(0)
write_to_file("Start")
try:
    while True:
        write_to_file("Hello, this is a test!")
        utime.sleep(1)  # 1초에 한번
except KeyboardInterrupt:
    write_to_file("Turn off")

'''
의사코드
1. 팬을 제어하기 위해 machine 모듈을 임포트한다.
2. utime 모듈을 임포트한다.
3. 팬을 제어하기 위해 Pin 14을 출력으로 설정한다.
4. 무한 루프를 사용하여 팬을 켜고 끈다.
5. 팬을 켜고 1초 동안 대기한다.
'''
import machine
import utime

# 14번 핀을 출력으로 설정 
fan = machine.Pin(10, machine.Pin.OUT)

while True:
    fan.on()
    utime.sleep(1)
    #fan.off()
    #utime.sleep(1)



    
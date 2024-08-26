from machine import Pin, PWM
from utime import sleep

# GPIO 22번 핀에 부저를 PWM 모드로 설정합니다.
buzzer = PWM(Pin(22))

# 다양한 음을 연주하기 위한 주파수와 길이 설정
melody = [
    (262, 0.5),  # 도(C)
    (294, 0.5),  # 레(D)
    (330, 0.5),  # 미(E)
    (349, 0.5),  # 파(F)
    (392, 0.5),  # 솔(G)
    (440, 0.5),  # 라(A)
    (494, 0.5),  # 시(B)
    (523, 0.5)   # 높은 도(C)
]

# 멜로디 연주
for note, duration in melody:
    buzzer.freq(note)            # 음 설정
    buzzer.duty_u16(30000)       # 세기 설정
    sleep(duration)              # 음 지속 시간
    buzzer.duty_u16(0)           # 소리 끄기
    sleep(0.1)                   # 음 사이의 짧은 휴지

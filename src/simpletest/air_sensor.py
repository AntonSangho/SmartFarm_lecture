import time, machine
import ENS160

# I2C 초기화
i2c = machine.I2C(1,scl=machine.Pin(15), sda=machine.Pin(14),freq=400000)
ens = ENS160.ENS160(i2c)
ens.reset()
time.sleep(0.5)
'''
ENS160 동작 모드 설정 
0 = Deep Sleep Mode (low power standby)
1 = Idle mode (low-power)
2 = Standard Gas Sensing Mode
''' 
ens.operating_mode = 2
time.sleep(2.0)
print("Taking ENS160 measurements... ")

while True:
    # ENS160 센서에서 데이터 읽기
    aqi:int = ens.AQI
    ''' 
    Reads the calculated Air Quality Index (AQI) according to the UBA
    1 = Excellent
    2 = Good
    3 = Moderate
    4 = Poor
    5 = Unhealthy
    ''' 
    eco2:int = ens.CO2
    tvoc:int = ens.TVOC

    print("AQI: " + str(aqi) + ", ECO2: " + str(eco2) + ", TVOC: " + str(tvoc))
    time.sleep(1.0)



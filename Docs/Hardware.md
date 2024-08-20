# GPIO 연결  
## I2C (RTC / Light Sensor) 
### RTC
| RaspberryPi Pico W | DS3231 |
|-----------|------|
|   GP4     | SCL  |
|   GP5     | SDA  |

### Light Sensor
| RaspberryPi Pico W | BH1750 |
|-----------|------|
|   GP4     | SCL  |
|   GP5     | SDA  |

## SPI
| RaspberryPi Pico W | SDcard |
|-----------|------|
|   GP20    | MOSI |
|   GP19    | SCK  |
|   GP17    | SC   |
|   GP16    | MISO |
## One-Wire
| RaspberryPi Pico W| ds18b20 |
|-----------|------|
|   GP26    | DI   |
## NeoPixel 
| RaspberryPi Pico W | WS281B |
|-----------|------|
|   GP21    | LED  |

## Buzz 
| RaspberryPi Pico W | MLT-7525 |
|-----------|------|
|   GP22    | Buzz |

## Button
| RaspberryPi Pico W | TacktileSwitch |
|-----------|------|
|   GP20    | SW1 |

## ADC
| RaspberryPi Pico W | TacktileSwitch |
|-----------|------|
|   GP27    | BAT_DIV |


# [SDCARD 포멧하기](https://linuxize.com/post/how-to-format-usb-sd-card-linux/)
1. [sdcard_script.sh 파일 경로로 이동](/src/simpletest/)  
2. ``` sudo chmod +x sdcard_script.pyq```
3. ```sudo ./sdcard_script.py```
















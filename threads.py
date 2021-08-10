import socket
from threading import *
from datetime import datetime
from log_files import print_log
from time import sleep
import sys
import board
import os
import adafruit_dht
import Adafruit_DHT
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

HOST = '172.16.100.234'
#HOST = sys.argv[1]
PORT = 8888
def socket_thread():
    print(f'Thread {current_thread().getName()}')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
            s.bind((HOST, PORT))
            print(f'Bound to socket {HOST}:{PORT}')

            s.listen(5)

            while True:
                conn, addr = s.accept()
                print(f'Connected to {conn.getsockname()} at {datetime.now()}')
                print_log(conn)
                data = str(DATA)

                conn.send(data.encode())
                print(f'Data sent to {conn.getsockname()} at {datetime.now()}')


    except KeyboardInterrupt:
        s.close()
        sys.exit(0)

def sensor_thread():
    global DATA
    FILE_NAME = 'readings.txt'
    PIN_P8_10 = "P8_10"
    sensor_sig = "P8_11"
    print(f'Thread {current_thread().getName()}')
    DATA = [11, 22, 33, 44, 55, 66, 77, 88, 99]
    value = 1.1
    DATA.append(value)

    GPIO.setup(PIN_P8_10, GPIO.OUT)
    ADC.setup()


    while True:
        try:
            GPIO.output(PIN_P8_10, GPIO.HIGH)
            sleep(1)
            GPIO.output(PIN_P8_10, GPIO.LOW)
            sleep(1)

            value = ADC.read_raw("P9_40")
            #yes
            print(f'Value = {value}')
            DATA[9] = value

            f = open(FILE_NAME, "a")
            msg = f'Value: {value} read at {datetime.now()}\n'
            f.write(msg)
            f.close()

            file_size = os.path.getsize(FILE_NAME)
            if file_size > 10000:
                os.system('rm readings.txt; touch readings.txt')
                print(f'{FILE_NAME} deleted')
        
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit(1)
        except RuntimeError as e:
            print('Runtime error')
            print(e)
            pass


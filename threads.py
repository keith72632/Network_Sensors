import socket
from threading import *
from datetime import datetime
from log_files import print_log
from time import sleep
import sys
import os
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import smbus

HOST = '172.16.100.227'
#HOST = sys.argv[1]
PORT = 8888

def twos_comp(val, bits):
    if(val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def c_to_f(val):
    return (val * 1.8) + 32

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
    DATA = [11, 22, 33, 44, 55, 66, 77, 88, 99, 80]
    value = 1.1
    DATA.append(value)

    GPIO.setup(PIN_P8_10, GPIO.OUT)
    i2c_ch = 2
    i2c_addr = 0x5a

    reg_temp = 0x00
    reg_config = 0x01
        
    bus = smbus.SMBus(i2c_ch)

    while True:
        try:
            GPIO.output(PIN_P8_10, GPIO.HIGH)
            sleep(1)
            GPIO.output(PIN_P8_10, GPIO.LOW)
            sleep(1)

            val = bus.read_i2c_block_data(i2c_addr, reg_config, 2)

            #print(f'Value = {value}')
            #print(f'Old Config = {val}')
            
            #set to 4hz sampling(CR1, CR0 = 0b10)
            #val[1] &= 0b00111111
            #val[1] |= (0b10 << 6)

            #read CONFIG to verify change
            #val = bus.read_i2c_block_data(i2c_addr, reg_config, 2)
            #print(f'New Config: {val}')
            #val = bus.read_i2c_block_data(i2c_addr, reg_temp, 2)

            temp_c = (val[0] << 4) | (val[1] >> 4)
            temp_c = str(temp_c)

            temp_c = f'{temp_c[:2]}.{temp_c[2:]}'
            temp_c = float(temp_c)
            temp_f = c_to_f(temp_c)
            
            DATA[0] = temp_f

            f = open(FILE_NAME, "a")
            msg = f'Value: {temp_f} read at {datetime.now()}\n'
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
            f = open('errors.txt', 'a')
            f.write(f'Runtime error {e}')
            break


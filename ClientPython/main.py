import time
import random

import serial
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0',baudrate=256000, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE)
    while [1]:
        test=""
        for i in range(0,1024):
            rand = random.getrandbits(1)
            if rand==0:
                test=test+"1"
            else:

                test=test+"0"
        ser.write(test.encode())
        #time.sleep(0.01)


#    while[1]:
#        for j in range(1,10):
#            test=""
#            for i in range(0,512):
#                if i%j==0:
#                    test=test+"1"
#                else:
#                    test=test+"0"
#            ser.write(test.encode())
#            time.sleep(0.1)


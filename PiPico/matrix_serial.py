from machine import Pin, UART
import time

CLK = Pin(13, Pin.OUT)
ABin = Pin(12, Pin.OUT)
RDin = Pin(10, Pin.OUT)
WEin = Pin(9, Pin.OUT)
AEin = Pin(8, Pin.OUT)
SEin = Pin(7, Pin.OUT)
GRin = Pin(6, Pin.OUT)
A0 = Pin(5, Pin.OUT)
A1 = Pin(4, Pin.OUT)
A2 = Pin(3, Pin.OUT)
A3 = Pin(2, Pin.OUT)

CLK.low()
ABin.low()
RDin.low()
WEin.low()
AEin.low()
SEin.low()
GRin.low()
A0.low()
A1.low()
A2.low()
A3.low()

uart = UART(0, 256000, parity=None, stop=1, bits=8, rx=Pin(17), tx=Pin(16))
uart.write("MATRIX TEST")
matrix=[]

def doImage(line1,line2,line3,line4,line5,line6,line7,line8,line9,line10,line11,line12,line13,line14,line15,line16):
  doStuff(0,0,0,0,line8)
  doStuff(0,0,0,1,line12)
  doStuff(0,0,1,0,line4)
  doStuff(0,0,1,1,line14)
  doStuff(0,1,0,0,line6)
  doStuff(0,1,0,1,line10)
  doStuff(0,1,1,0,line2)
  doStuff(0,1,1,1,line15)
  doStuff(1,0,0,0,line7)
  doStuff(1,0,0,1,line11)
  doStuff(1,0,1,0,line3)
  doStuff(1,0,1,1,line13)
  doStuff(1,1,0,0,line5)
  doStuff(1,1,0,1,line9)
  doStuff(1,1,1,0,line1)
  doStuff(1,1,1,1,line16)
  
def cycleClock():
  CLK.high()
  CLK.low()
def writeState(pin, state):
    if state==1:
        pin.high()
    else:
        pin.low()
        
def doStuff(a1, a2, a3, a4, line):
    writeState(A0, a1)
    writeState(A1, a2)
    writeState(A2, a3)
    writeState(A3, a4)
    cycleClock()
    writeState(AEin, 1)

    cycleClock()
    writeState(WEin, 1)
  
    cycleClock()
    writeState(WEin, 0)
  
    cycleClock()
    writeState(AEin, 0)
    cycleClock()
    for entry in line:
        writeState(RDin, entry)
        writeState(GRin, entry)
        cycleClock()
        

def main():
    while [1]:
        matrix=[]
        for i in range(0,16):
            counter=1
            line=[]
            while [1]:
                #time.sleep(0.01)
                val=uart.read(1)
                if val!=None:
                    if ord(val)==49:
                        line.append(1)
                    else:
                        line.append(0)
                    counter=counter+1
                    if counter>64:
                        matrix.append(line)
                        break
        #doImage(line1,line2,line3,line4,line5,line6,line7,line8,line9,line10,line11,line12,line13,line14,line15,line16)
        doImage(matrix[0],matrix[1],matrix[2],matrix[3],matrix[4],matrix[5],matrix[6],matrix[7],matrix[8],matrix[9],matrix[10],matrix[11],matrix[12],matrix[13],matrix[14],matrix[15])
        

if __name__ == "__main__":
    main()


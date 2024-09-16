from machine import Pin
import time
import gc
import os
from usocket import socket
from machine import Pin,SPI
import network

CLK = Pin(8, Pin.OUT)
ABin = Pin(3, Pin.OUT)
RDin0 = Pin(15, Pin.OUT)
RDin1 = Pin(16, Pin.OUT)
RDin2 = Pin(17, Pin.OUT)
WEin = Pin(9, Pin.OUT)
AEin = Pin(10, Pin.OUT)
SEin = Pin(2, Pin.OUT)
GRin0 = Pin(13, Pin.OUT)
GRin2 = Pin(12, Pin.OUT)
GRin1 = Pin(11, Pin.OUT)
A0 = Pin(7, Pin.OUT)
A1 = Pin(6, Pin.OUT)
A2 = Pin(5, Pin.OUT)
A3 = Pin(4, Pin.OUT)
ip=""
currentSequence=0
currentReceived=""

CLK.low()
ABin.low()
RDin0.low()
RDin1.low()
RDin2.low()
WEin.low()
AEin.low()
SEin.low()
GRin0.low()
GRin1.low()
GRin2.low()
A0.low()
A1.low()
A2.low()
A3.low()




def doImage(lineArr):
  doStuff(0,0,0,0,lineArr[8],lineArr[24],lineArr[40])
  doStuff(0,0,0,1,lineArr[4],lineArr[20],lineArr[36])
  doStuff(0,0,1,0,lineArr[12],lineArr[28],lineArr[44])
  doStuff(0,0,1,1,lineArr[2],lineArr[18],lineArr[34])
  doStuff(0,1,0,0,lineArr[10],lineArr[26],lineArr[42])
  doStuff(0,1,0,1,lineArr[6],lineArr[22],lineArr[38])
  doStuff(0,1,1,0,lineArr[14],lineArr[30],lineArr[46])
  doStuff(0,1,1,1,lineArr[1],lineArr[17],lineArr[33])
  doStuff(1,0,0,0,lineArr[9],lineArr[25],lineArr[41])
  doStuff(1,0,0,1,lineArr[5],lineArr[21],lineArr[37])
  doStuff(1,0,1,0,lineArr[13],lineArr[29],lineArr[45])
  doStuff(1,0,1,1,lineArr[3],lineArr[19],lineArr[35])
  doStuff(1,1,0,0,lineArr[11],lineArr[27],lineArr[43])
  doStuff(1,1,0,1,lineArr[7],lineArr[23],lineArr[39])
  doStuff(1,1,1,0,lineArr[15],lineArr[31],lineArr[47])
  doStuff(1,1,1,1,lineArr[0],lineArr[16],lineArr[32])
  
  #doStuff(0,0,0,0,lineArr[7],lineArr[23],lineArr[39])
  #doStuff(0,0,0,1,lineArr[11],lineArr[27],lineArr[43])
  #doStuff(0,0,1,0,lineArr[3],lineArr[19],lineArr[35])
  #doStuff(0,0,1,1,lineArr[13],lineArr[29],lineArr[45])
  #doStuff(0,1,0,0,lineArr[5],lineArr[21],lineArr[37])
  #doStuff(0,1,0,1,lineArr[9],lineArr[25],lineArr[41])
  #doStuff(0,1,1,0,lineArr[1],lineArr[17],lineArr[33])
  #doStuff(0,1,1,1,lineArr[14],lineArr[30],lineArr[46])
  #doStuff(1,0,0,0,lineArr[6],lineArr[22],lineArr[38])
  #doStuff(1,0,0,1,lineArr[10],lineArr[26],lineArr[42])
  #doStuff(1,0,1,0,lineArr[2],lineArr[18],lineArr[34])
  #doStuff(1,0,1,1,lineArr[12],lineArr[28],lineArr[44])
  #doStuff(1,1,0,0,lineArr[4],lineArr[20],lineArr[36])
  #doStuff(1,1,0,1,lineArr[8],lineArr[24],lineArr[40])
  #doStuff(1,1,1,0,lineArr[0],lineArr[16],lineArr[32])
  #doStuff(1,1,1,1,lineArr[15],lineArr[31],lineArr[47])
  
def cycleClock():
  CLK.high()
  CLK.low()
def writeState(pin, state):
    if state>=1:
        pin.high()
    else:
        pin.low()
        
def doStuff(a1, a2, a3, a4, line1,line2, line3):
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
    for i in range(192):
        # Line1 unten
        #Line2 Mitte
        writeState(GRin0, int(line1[i]))
        writeState(GRin1, int(line2[i]))
        writeState(GRin2, int(line3[i]))
        cycleClock()

def w5x00_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
    nic.ifconfig('dhcp')
    
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
    print('IP address :', nic.ifconfig())
    ip=nic.ifconfig()[0]
def displayImage(data):
    lines=data.split(";")
    doImage(lines)
    #Need to double do this to avoid artifacts
    doImage(lines)
    
def handleData(data):
    sequence=0
    global currentReceived
    global currentSequence
    splitted=data.split("+")
    if splitted[0] is None:
        return
    sequence=int(splitted[0])
    recv=splitted[1].replace("'",'')
    if sequence >= currentSequence:
        currentReceived+=recv
        currentSequence=sequence
    if  currentSequence >= 9:
        displayImage(currentReceived)
        currentReceived=""
        currentSequence=0

def main():
    splash=open("./splash.dat", "r")
    lineArr=[]
    for line in splash:
        lineArr.append(line)
    splash.close
    doImage(lineArr)
    s = os.statvfs('/')
    print(f"Free storage: {s[0]*s[3]/1024} KB")
    print(f"Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used.")
    print(f"CPU Freq: {machine.freq()/1000000}Mhz")
    w5x00_init()
    s = socket()
    s.bind((ip, 80))
    s.listen(50)

    while True:
        conn, addr = s.accept()
        print('Connect from %s' % str(addr))
        request = conn.recv(40096)
        request = str(request)
        if "data#" in request:
            handleData(request.split("#")[1])
        response = "test"
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Connection: close\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Content-Length: %s\n\n' % len(response))
        conn.send(response)
        conn.close()






if __name__ == "__main__":
    main()




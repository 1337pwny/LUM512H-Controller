import requests

def sendMessage(data):
    print(data)
    response = requests.post("http://192.168.111.115",data)
while True:
    for j in range(11):
        sr=str(j+1)+".dat"
        f=open(sr,"r")
        stri=f.read()
        i=0
        sequence=0
        buffer="data#"+str(sequence)+"+"
        for char in stri:
            if i >= 1000:
                sendMessage(buffer)
                i=0
                sequence+=1
                buffer = "data#" + str(sequence) + "+"
            buffer=buffer+str(char)
            i+=1
        sendMessage(buffer)
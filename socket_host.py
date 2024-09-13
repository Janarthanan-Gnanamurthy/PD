import socket
import time
import re

s = socket.socket()
emg =[]         
flag = False 
s.bind(('192.168.56.3', 8080 ))
print("server running")
s.listen(0)    
             
 
while True:
 
    client, addr = s.accept()
 
    while True:
        # print(client)
        content = client.recv(1024).decode()
 
        if len(content) ==0:
           break
        else:
            # print(content)
            # time.sleep(1)
            if "EMG:" in content :
                flag = True
            if flag == True:
                emg.append(content)
                flag = False
            if len(emg) > 10:
                emg_readings = [re.search(r'EMG:(\d+\.\d+)', line).group(1) for line in emg if re.search(r'EMG:(\d+\.\d+)', line)]
                emg_readings_float = [float(reading) for reading in emg_readings]
                average_emg = sum(emg_readings_float) / len(emg_readings_float)
                print("average EMG: ", average_emg)
                emg = []
    # print("Closing connection")
    client.close()
import datetime
import time
import serial #need to download pyserial
import json #get the JSON library for JSON data "output"
cels = '°C'
oldtemp = '0'
oldtime = 0
i = 0
br = "\n" #not important
time.sleep(1.5);

#attributes for serial
ser = serial.Serial()
ser.baudrate = 9600
ser.port='COM3'

#try to open serial    
try:
    ser.open()
except Exception: 
    print("error open serial port: ")
    exit()

#after opening serial, remove all data in serial buffer
if ser.isOpen():
    ser.flushInput()
    ser.flushOutput()
    print('Opening serial...')
else:
    print("Cannot open serial port")

print(ser.name) #print the name of the serial port
print(time.strftime('%H:%M:%S')); #print the current time of date

while ser.is_open == True:

    serTemp = ser.readlines(1)
    temp = ''.join(str(e) for e in serTemp) 
    time.sleep(0.5)
    ser.flushInput() #needed to literally flush possible serial buffered data to be on time

    if(oldtemp != temp): #just cheks if the incoming data is "new" in compared to last added data dump
        
        times = time.strftime('%H:%M:%S')
        #convert time to seconds
        h,m,s = times.split(":")
        currsecs = int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds())
        timediff = currsecs - oldtime
        str1 = 'Time:' + '+' + str(timediff) +'s'
        print(str1) #print how much time has passed since last dump
        
        #when if, count the time difference between times and put +smth
        str2 = temp[2:7] #cut the input data from 2 to 7 position of letters, could have problem if temperature goes over 100 or under 0
        print(str2)
        
        #just bunch of string theory, this all is for the sake of creating the new data into JSON file look nice
        dataTime = str1
        dataTemp = "Temp:" + str2 

        str3 = "{"
        str4 = "}"
        str5 = str3 + dataTime + ", " + dataTemp + str4
        strF = '"' + str5 + '"'
        vals = strF
        data = json.loads(vals)

        with open('./temps.json', 'a') as outfile: #open "session" for JSON file writing
            if (i == 0):
                outfile.write(times) #add current time
                outfile.write(': \n'); #next row
            json.dump(data, outfile, indent= 2 ) #dump the whole string with +time and temperature
            outfile.write(', \n')
            i += 1 #i for monitoring how many times temperature has been written
            print(i); #shows only in console, since it would take more space to write it into the JSON
        oldtime = currsecs #change the value of time, this is needed in order to calculate time difference between temperature cheks
    else:
        None
    oldtemp = temp #replace temprature data value, this is needed in order to check if same temperature was previusly added
                    #if the temperature has not changed in the matter of time lasted, will not write new line into JSON
                    #will save more space in the file, if nothing has changed, sleep 0.5s. really not needed, but gives treshold to new data 
    if(str2 >= "80"):
        print("System error")
        print("Restarting system...")
        print("");
        time.sleep(1);
        ser.close()
        ser.open();
    else:
        continue;
else:              
    time.sleep(0.5)

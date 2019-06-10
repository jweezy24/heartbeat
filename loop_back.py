import wiringpi as wpi
import time
import serial as ser


def main():
    #serial = None
    serial0 = ser.Serial("/dev/ttyS2",115200,timeout=6.0)
  
    try:

        while True:
            #serial0.flush()
            #time.sleep(2)
            #val = serial0.in_waiting
            #b = serial0.read(1024)
            #uB = set(b)
            #print("Unique " , len(uB))
            ser.Serial("/dev/ttyS2", 115200).write("Hello".encode())
            #b = serial1.read(val)  
            #print(b)
        #wpi.serialClose(serial)
    except Exception as e:
        print("Error: \t " + str(e) )
        #ser.Serial("/dev/ttyS2",9600).close()
        #serial0.close()

main()    

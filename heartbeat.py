import os
import time

time_low = 0
time_high = 1

def main():
    pidfile='/var/run/waggle/heartbeat.pid'
    cur_PID = os.getpid()
    f = open(pidfile)
    for i in f:
        print(i)

if __name__ == "__main__":
    main()

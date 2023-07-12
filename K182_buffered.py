import pyvisa as visa
import time

rm = visa.ResourceManager()

DVM = rm.open_resource("TCPIP::192.168.0.88::GPIB0,8")
DVM.timeout = 10000   # in ms

DVM.write("DCLX")      # clear to default settings
DVM.write("RENX")      # Remote mode
DVM.write("U2X")      # Get firmware test
print("Keithley 182 Firmware:")
print(DVM.read())
print("Configuring ...")
DVM.write("B1X")      # 6.5 digit resolution
DVM.write("I2X")      # Circular buffer on, length = 1024
#DVM.write("F1G0X")   # Reading Source: One reading from buffer, reading without prefix
DVM.write("F1G6X")    # Reading Source: One reading from buffer, reading with time stamp and buffer location
#DVM.write("F0G0X")   # Reading Source: direct ADC
DVM.write("O1P0N1X")  # Enabled analog filter, disabled dig filter
DVM.write("R1X")      # 3mV range
DVM.write("S2X")      # 100ms integration period
DVM.write("T4X")      # Trigger on X multiple

print("Waiting for the circular buffer to be half full ...")
#time.sleep(1024/2*.1) # wait for buffer half full
time.sleep(10) # wait for buffer half full

last_time = 0.0

while True:           # start reading perhaps?
    print("Sample from buffer:")
    reading=DVM.read()
    print("VVVVVVVVVVVVV,BufP,second, ms")
    print(reading)
    timestamp=float(reading.split(',')[2].strip())
    time_difference = last_time-timestamp
    print("Seconds between this and the last reading:")
    print(time_difference)
    last_time = timestamp
    time.sleep(time_difference)
    

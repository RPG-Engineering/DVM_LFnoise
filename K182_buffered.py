import pyvisa as visa
from time import time

rm = visa.ResourceManager()

DVM = rm.open_resource("TCPIP::192.168.0.88::GPIB0,8")
DVM.timeout = 10000   # in ms

DVM.write("DCL")      # clear to default settings
DVM.write("REN")      # Remote mode
DVM.write("U2")      # Get firmware test
print("Keithley 182 Firmware:")
print(read_data("X"))

DVM.write("B1X")      # 6.5 digit resolution
DVM.write("I2X")      # Circular buffer on, length = 1024
#DVM.write("F1G0X")   # Reading Source: One reading from buffer, reading without prefix
DVM.write("F1G6X")    # Reading Source: One reading from buffer, reading with time stamp and buffer location
#DVM.write("F0G0X")   # Reading Source: direct ADC
DVM.write("O1P0N1X")  # Enabled analog filter, disabled dig filter
DVM.write("R1X")      # 3mV range
DVM.write("S2X")      # 100ms integration period
DVM.write("T4X")      # Trigger on X multiple

time.sleep(1024/2*.1) # wait for buffer half full

while True:           # start reading perhaps?
    print(read_data("X"))
    

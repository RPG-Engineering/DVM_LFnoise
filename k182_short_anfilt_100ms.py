import pyvisa as visa
import time
import csv


rm = visa.ResourceManager()

DVM = rm.open_resource("TCPIP::192.168.0.88::GPIB0,8")
DVM.timeout = 10000   # in ms

DVM.write("DCLX")      # clear to default settings
DVM.write("RENX")      # Remote mode
DVM.write("U2X")       # Get firmware to test
print("Keithley 182 Firmware:")
print(DVM.read())
print("Configuring ...")
DVM.write("B1X")      # 6.5 digit resolution
#DVM.write("I1,1024X") # Linear buffer on, length = 1024
DVM.write("G0X")     # Reading without prefix
#DVM.write("G6X")      # Reading with time stamp and buffer location
#DVM.write("F1X")      # Reading Source: One reading from buffer
DVM.write("F0X")     # Reading Source: direct ADC
DVM.write("O1P0N1X")  # Enabled analog filter, disabled dig filter
DVM.write("R1X")      # 3mV range
DVM.write("S2X")      # 100ms integration period
#DVM.write("T7X")      # Trigger one shot external
DVM.write("T4X")      # Trigger one shot external
DVM.write("Z1X")      # Relative readings

f = open('k182_short_anfilt_100ms.csv', 'w')
writer = csv.writer(f)
header = ['seconds', 'volt', ]
writer.writerow(header)

python_start_time = time.time()

while True:
    reading=float(DVM.read())
    timestamp = time.time()-python_start_time
    row = [timestamp, reading, ]
    print(row)
    writer.writerow(row)


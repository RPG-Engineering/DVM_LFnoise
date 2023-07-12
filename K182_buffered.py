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
DVM.write("I1,1024X") # Linear buffer on, length = 1024
#DVM.write("G0X")     # Reading without prefix
DVM.write("G6X")      # Reading with time stamp and buffer location
DVM.write("F1X")      # Reading Source: One reading from buffer
#DVM.write("F0X")     # Reading Source: direct ADC
DVM.write("O1P0N1X")  # Enabled analog filter, disabled dig filter
DVM.write("R1X")      # 3mV range
DVM.write("S2X")      # 100ms integration period
DVM.write("T4X")      # Trigger on X multiple

python_start_time = time.time()
python_last_time = time.time()
keithley_last_time = 0.0

while True:
    print("Sample from buffer:")
    reading=DVM.read()
    print("VVVVVVVVVVVVV,BufP,second, ms")
    print(reading)
    keithley_timestamp=float(reading.split(',')[2].strip())
    keithley_time_difference = keithley_timestamp-keithley_last_time
    print("Keithley seconds between this and the last reading:")
    print(keithley_time_difference)
    keithley_last_time = keithley_timestamp
    
    buffer_position=int(reading.split(',')[1].strip())
    if (buffer_position == 50):
        DVM.write("I1,1024X") # Linear buffer on, length = 1024
    

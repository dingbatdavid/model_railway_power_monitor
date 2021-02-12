
# Model Railway Power Monitor
# Code has been put together from various sources and
# modified by me David Peck for the Raspberry Pi Pico
# V1.0 Feb 2021
# Filename model_railway_power_monitor.py
# Save as code.py on Pico to auto run on startup


import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import busio 
from time import sleep
SCL = board.GP1
SDA = board.GP0
i2c_bus = busio.I2C(SCL, SDA)

#Initialise LCD and set background Colour
i2c_bus.try_lock()
i2c_bus.writeto(0x72, bytes([0x7C]))
sleep(1)
i2c_bus.writeto(0x72, bytes([0x08]))
sleep(1)
i2c_bus.writeto(0x72, bytes([0x7C]))
sleep(1)
i2c_bus.writeto(0x72, bytes([0x2D]))
sleep(1)
i2c_bus.writeto(0x72, "   Model Railway    Accessory")
sleep(1)
i2c_bus.writeto(0x72, " and StreetLighting Power Info.")
sleep(1)
i2c_bus.writeto(0x72, "        V1.0")
sleep(1)
i2c_bus.writeto(0x72, bytes([0x7C]))
sleep(1)
i2c_bus.writeto(0x72, bytes([0x2B]))
sleep(1)
i2c_bus.writeto(0x72, bytes([0x00]))
sleep(1)
i2c_bus.writeto(0x72, bytes([0xFF]))
sleep(1)
i2c_bus.writeto(0x72, bytes([0x00]))
sleep(1)
i2c_bus.unlock()


ina219 = INA219(i2c_bus, 0x40) # Accessory Supply
ina219_1 = INA219(i2c_bus, 0X41) # Street Light Supply
range = ina219.bus_voltage_range
range = ina219_1.bus_voltage_range

# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S

ina219_1.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219_1.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S

# optional : change voltage range to 16V
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

ina219_1.bus_voltage_range = BusVoltageRange.RANGE_16V

# measure and display loop
while True:
    bus_voltage = ina219.bus_voltage  # voltage on V- (load side)
    shunt_voltage = ina219.shunt_voltage  # voltage between V+ and V- across the shunt
    current = ina219.current  # current in mA
    power = ina219.power  # power in watts
    
    bus_voltage_1 = ina219_1.bus_voltage  # voltage on V- (load side)
    shunt_voltage_1 = ina219_1.shunt_voltage  # voltage between V+ and V- across the shunt
    current_1 = ina219_1.current  # current in mA
    power_1 = ina219_1.power  # power in watts  

    # Write info to LCD, the sleep period is to allow the LCD to update     
    i2c_bus.try_lock()
    
    i2c_bus.writeto(0x72, bytes([0x7C]))
    sleep(1)
    
    i2c_bus.writeto(0x72, bytes([0x2D]))
    sleep(1)
            
    i2c_bus.writeto(0x72, "  Accessory Power   ")
    sleep(1)
    
    i2c_bus.writeto(0x72, "Supply  :{:5.2f} V".format(bus_voltage + shunt_voltage) + "    ") 
    sleep(1)
    
    i2c_bus.writeto(0x72, "Current :{:7.4f} A".format(current / 1000) + "  ")
    sleep(1)
    
    i2c_bus.writeto(0x72, "Power   :{:5.2f} W".format(power))
    
    sleep(2)  

    i2c_bus.writeto(0x72, bytes([0x7C]))
    sleep(1)
    
    i2c_bus.writeto(0x72, bytes([0x2D]))
    sleep(1)
    
    i2c_bus.writeto(0x72, " Street Light Power ")
    sleep(1)
    
    i2c_bus.writeto(0x72, "Supply  :{:5.2f} V".format(bus_voltage_1 + shunt_voltage_1) + "    ") 
    sleep(1)
    
    i2c_bus.writeto(0x72, "Current :{:7.4f} A".format(current_1 / 1000) + "  ")
    sleep(1)
    
    i2c_bus.writeto(0x72, "Power   :{:5.2f} W".format(power_1))
    
    i2c_bus.unlock()
   
   # Check internal calculations haven't overflowed (doesn't detect ADC overflows)
    if ina219.overflow:
        print("Internal Math Overflow Detected!")
        print("")
        
    if ina219_1.overflow:
        print("Internal Math Overflow Detected!")
        print("")
    
    time.sleep(2)
    
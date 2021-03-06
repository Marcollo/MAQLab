from Devices.Keithley import SM2400
import time

dev = SM2400.SM2400("com3")

print(dev.devicetype)
print(dev.manufactorer)
print(dev.serialnumber)
print(dev.model)

'''
print(dev.getparameter())
print(dev.idstring)
print(dev.model)
print(dev.serialnumber)
print(dev.manufactorer)
print(dev.devicetype)
'''


'''
print("Voltage source")
#dev.set_mode_voltage_source(20, 0.5)
dev.disable_human_security_mode()
dev.set_mode_voltage_source()
# dev.set_current_limits(0.2)
dev.apply_current = 1
#dev.volt = 1
#dev.measure()
#dev.set_output_on()
#dev.measure()
#print(dev.volt, dev.current)
#print(dev.volt)

for i in range(-300, 300):
    dev.apply_volt = i/100
    time.sleep(0)
    dev.measure()
    print(dev.current_as_string, dev.volt_as_string)
    #time.sleep(0.1)
'''

'''
dev.setOutput_off()
'''


'''
print("Current source")
# dev.disable_human_security_mode()

dev.set_mode_current_source()
# dev.set_volt_limits(180)
dev.apply_volt = 13
time.sleep(1)
# dev.apply_current = -0.101

for i in range(200, 300):
    dev.apply_current = (i / 10000) * -1
    #dev.volt = i/10
    dev.measure()
    print(dev.volt_as_string, dev.current_as_string)
    time.sleep(0.1)
'''


print("Voltmeter")
dev.set_mode_volt_meter()
for i in range(1, 10):
    dev.measure()
    print(dev.volt)
    time.sleep(0.1)

'''
print("Amperemeter")
dev.set_mode_ampere_meter()
for i in range(1, 10):
    dev.measure()
    print(dev.current)
    time.sleep(1)
'''

'''
print("Sink Mode")
dev.set_mode_sink(0)
# time.sleep(5)
for i in range(10, 200):
    dev.current = i / 100
    print(dev.volt, dev.current)
    time.sleep(0.5)

time.sleep(1)
'''

'''
print("ohmmeter")
dev.set_mode_ohmmeter_4wire()
for i in range (0, 2000):
    #print(dev.getValue())
    #dev.setSinkCurrent(i/10)
    dev.measure()
    print(dev.volt, dev.current, dev.resistance)
    time.sleep(0.1)

#dev.setModeSink(0)
dev.set_output_off()
time.sleep(5)
# dev.setOutput_off()
'''


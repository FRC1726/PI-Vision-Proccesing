import serial

port =serial.Serial(
    "/dev/ttyUSB0",
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout = 0,
    timeout = 10,
    rtscts=False,
    dsrdtr=False,import serial

port =serial.Serial(
    "/dev/ttyUSB0",
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout = 0,
    timeout = 10)

data=bytes([0x0c,0x80,0x09,0x00,0xf0,0xce,0x61,0x9d,0x01,0x00,0x01,0x00,0x00,0x00]) 

print(port.isOpen()) 
print("Port opened...") 
port.write(data) 
print("Data sent")

while True:
    print("inside while")
    response=port.read(8)
    print(response)
    print ("Data Received")
    break
    xonxoff=False)

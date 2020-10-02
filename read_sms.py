import time
import serial

phone = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)

try:
    phone.write(b'ATZ\r')  # set to base user profile
    print phone.readall()

    phone.write(b"AT+CMGF=1\r")  # set messages to text format
    print(phone.readall())

    while 1:
        phone.write(b'AT+CMGL="ALL"\r')
        data = phone.readall()
        print(data)
        time.sleep(5)
finally:
    phone.close()

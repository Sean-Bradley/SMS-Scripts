import time
import serial
import subprocess
from curses import ascii

# An example script that shows how to receive an SMS message containing 'get_temp' and
# then respond by sending an SMS message back to the requesting number

phone = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)
# phone.write(ascii.ctrl('z'))
# exit()

try:
    phone.write(b'ATZ\r')  # set to base user profile
    print(phone.readall())

    phone.write(b"AT+CMGF=1\r")  # set messages to text format
    print(phone.readall())

    while 1:
        phone.write(b'AT+CMGL="ALL"\r')  # read all stored messages
        data = phone.readall()
        # print(data)

        CMGLs = data.split("+CMGL:")
        print("CMGLs length = " + str(len(CMGLs)))
        for cmgl in CMGLs:
            num = ""
            cmglID = -1
            for line in cmgl.splitlines():
                if len(line) > 0 and line != 'OK' and line != 'AT+CMGL="ALL"':
                    print(line)
                    parts = line.split(",")
                    if len(parts) > 2:
                        cmglID = parts[0].strip()
                        parts[2] = parts[2].replace('"', "")
                        # print(parts[2])
                        num = parts[2]
                        #print("num=" + num)
                    # validate the requestors mobile number
                    elif len(parts) == 1 and num == "+senders_mobile_no":
                        if parts[0] == "get_temp":
                            print("received get_temp command at CMGL " + cmglID)

                            # read the RPi temperature
                            cmd = '/opt/vc/bin/vcgencmd measure_temp'
                            process = subprocess.Popen(
                                cmd, stdout=subprocess.PIPE, shell=True)
                            output, error = process.communicate()
                            print(output)
                            #print("sending to " + num)

                            # sends the sms
                            phone.write(b'AT+CMGS="' + num.encode() + b'"\r')
                            time.sleep(0.5)
                            phone.write(output.encode() + b"\r")
                            time.sleep(0.5)
                            phone.write(ascii.ctrl('z'))
                            time.sleep(0.5)
                            print("message sent")
                            print(phone.readall())

                            # delete the message so that it doesn't get reprocessed
                            phone.write(b"AT+CMGD=" + cmglID + "\r")
                            print(phone.readall())

        time.sleep(5)

finally:
    phone.close()

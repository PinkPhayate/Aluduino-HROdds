#coding utf-8
import serial
import re

trans_dict = {'22':'0',
            '12':'1',
            '24':'2',
            '94':'3',
            '8':'4',
            '28':'5',
            '90':'6',
            '66':'7',
            '82':'8',
            '74':'9'}
def analyze(input):
    w = input.strip()
    if w in trans_dict.keys():
        num = trans_dict[input.strip()]

    else:
        print("couldn't transcript: " +  w)
        num = 'CANT'
    print(num)
    return num

def send_number(num):
    print(num)

def main():
    with serial.Serial('/dev/cu.usbmodem14111',115200,timeout=1) as ser:
        counter = 0
        nums = []
        while True:
            try:
                c = ser.readline()
            except(serial.serialutil.SerialException):
                print('unexpected return value')
                c = ''
            print(c)
            if 0<len(c):
                num = analyze(c.decode())
                if(num != 'CANT'):
                    nums.append(num)
            if 2<counter:
                counter = -1
            counter += 1
        ser.close()

if __name__=="__main__":
    main()

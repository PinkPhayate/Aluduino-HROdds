import csv
import sys
import serial   #モジュール名はpyserialだが, importする際はserialである
from oddsman import oddsman
import time
import serial_con as sc
import re
ow = oddsman.OddsWatcher()


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


MACHINE_NAME = "/dev/cu.usbmodem14111"
PORT         = "115200"

def save_cash(race_id, odds_list):
    print('save_cash')
    ### cache server に保存

def test_get_race_odds(mode=None):
    if mode == 'test':   # test mode
        race_id = '201209030811'
        odds_list = ow.get_race_odds(race_id)
    else:
        odds_list = ow.get_nearest_odds()
    save_cash(race_id=race_id, odds_list=odds_list)
    print(odds_list)
    return odds_list

def export(odds_list):
    with serial.Serial( MACHINE_NAME, PORT, timeout=1) as ser:
        no = 1
        # odds_list = get_odds_list()
        for odds in odds_list:
            ser.write(str(no).encode('utf-8'))
            print(no)
            time.sleep(2)
            ser.write(str(odds).encode('utf-8'))
            print(odds)
            no += 1
            time.sleep(2)
            break

        # ser.write("999".encode('utf-8'))
        ser.close()

def change_mode():
    # with serial.Serial( MACHINE_NAME, PORT, timeout=1) as ser:
    #     ser.write("10000".encode('utf-8'))
    serial_read()

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

def serial_read():
    with serial.Serial( MACHINE_NAME, PORT, timeout=1) as ser:
        ser.write("10000".encode('utf-8'))
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

def main():
    export()

if __name__ == "__main__":
    args = sys.argv
    odds_list = test_get_race_odds(args[1])
    export(odds_list)
    change_mode()

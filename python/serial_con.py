import csv
import sys
import serial   #モジュール名はpyserialだが, importする際はserialである
import time
import serial_con as sc
import re
import oddsman_wrapper as wrapper
import cached as chd

trans_dict   = {'22': '0',
                '12': '1',
                '24': '2',
                '94': '3',
                '8': '4',
                '28': '5',
                '90': '6',
                '66': '7',
                '82': '8',
                '74': '9'}


MACHINE_NAME = "/dev/cu.usbmodem14111"
PORT         = "115200"
args = sys.argv

def save_cash(race_id, odds_list):
    print('save_cash')
    ### cache server に保存

def test_get_race_odds(mode=None):
    odds_list = chd.get_race_odds_list()
    if odds_list is None:
        odds_list = wrapper.get_race_odds(mode)
        chd.set_race_odds_list(odds_list)
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

def notify():
    """
    acknowledge odds about all race hource
    """
    odds_list = get_race_odds(args[1])
    with serial.Serial( MACHINE_NAME, PORT, timeout=1) as ser:
        for i, odds in enumerate(odds_list):
            ser.write(str(i).encode('utf-8'))
            print(i)
            time.sleep(2)
            ser.write(str(odds).encode('utf-8'))
            print(odds)
            time.sleep(2)
        ser.close()

def analyze(input):
    """
    method for translate number from alduino to python language
    """
    w = input.strip()
    if w == '67':
        return

    num = trans_dict[w] if w in trans_dict.keys() else '*'
    print(w)
    return num

def end_input(ser, num):
    odds_list = test_get_race_odds(args[0])
    rtval = wrapper.retrieve_odds(odds_list, num)
    if rtval is not None:
        ser.write(str(rtval).encode('utf-8'))
    else:
        ser.write(str("10000").encode('utf-8'))


def serial_read():
    with serial.Serial( MACHINE_NAME, PORT, timeout=1) as ser:
        nums = []
        while True:
            try:
                c = ser.readline()
            except(serial.serialutil.SerialException):
                print('unexpected return value')
                c = ''
            if 0<len(c):
                # print(c)
                num = analyze(c.decode())
                if(num is not None):
                    nums.append(num)
                elif num is None and 0 < len(nums):
                    end_input(ser, nums)
                    nums = []
                elif num is None:
                    print('notification mode')
                    break
        ser.close()
    notify()
    return

# while(True):
#     serial_read()


odds_list = test_get_race_odds(args[1])
print(odds_list)

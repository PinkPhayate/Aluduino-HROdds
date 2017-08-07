import csv
import sys
import serial   #モジュール名はpyserialだが, importする際はserialである
import time
import serial_con as sc
import re
import oddsman_wrapper as wrapper
import cached as chd
from time import sleep
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


MACHINE_NAME = "/dev/cu.usbmodem1421"
PORT         = "115200"
args = sys.argv
mode = None
if 1 < len(args):
    mode = 'test' if args[1]=='test' else None

def save_cash(race_id, odds_list):
    print('save_cash')
    ### cache server に保存

def test_get_race_odds(mode=None):
    odds_list = chd.get_race_odds_list()
    if odds_list is None:
        odds_list = wrapper.get_race_odds(mode)
        chd.set_race_odds_list(odds_list)
    else:
        odds_list = odds_list.decode('utf-8')
    return odds_list

def get_race_odds_real_time():
    odds_list = chd.get_race_odds_list()
    if odds_list is None:
        odds_list = wrapper.get_race_odds(mode)
        chd.set_race_odds_list(odds_list)
    else:
        odds_list = odds_list.decode('utf-8')
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
            # break

        # ser.write("999".encode('utf-8'))
        ser.close()

def notify():
    """
    acknowledge odds about all race hource
    """
    odds_list = wrapper.get_race_odds(mode)
    with serial.Serial( MACHINE_NAME, PORT, timeout=1) as ser:
        for i, odds in enumerate(odds_list):
            ser.write(str(i+1).encode('utf-8'))
            print(i+1)
            time.sleep(2)
            ser.write(str(odds).encode('utf-8'))
            print(odds)
            time.sleep(2)
            # break;
        print("notify mode has finished")
        ser.close()

def notify_one(num):
    if not is_float(num):
        return
    num = int(float(num))
    # print(num)
    odds_list = wrapper.get_race_odds(mode)
    odds = wrapper.retrieve_odds(odds_list, num)

    print('key is: ' + str(num))
    print('return value is: ', end='')
    if odds is None:
        print('couldnt find that odds: ' + str(num))
        odds = 999.0

    with serial.Serial( MACHINE_NAME, PORT, timeout=1) as ser:
        print(str(odds).encode('utf-8'))
        ser.write(str(odds).encode('utf-8'))
        ser.close()


def analyze(input):
    """
    method for translate number from alduino to python language
    """
    w = input.strip()
    # if w == '1000':
    #     return 'notify'
    try:
        analyzed_value = w.decode()
    except:
        print('couldnt decode word is:',end='')
        # print(w)
        return None
    return analyzed_value


def is_float(s):
    try:
        float(str(s))
        return True
    except ValueError:
        return False

def serial_read():
    with serial.Serial( MACHINE_NAME, PORT, timeout=1) as ser:
        nums = []
        while True:
            try:
                c = ser.readline()
                # print(c)
                if 0<len(c):
                    break
            except(serial.serialutil.SerialException):
                print('unexpected return value')
                c = None
        print('break')
        if 0<len(c):
            num = analyze(c)
            print('analyzed number: ', end='')
            print(num)
            # num = analyze(c.decode())
            if num is None:
                print('input number is invalid')
            elif num == '1000':
                print('notification mode')
                notify()
            else:
                notify_one(num)
        ser.close()

    return

# while(True):

while True:
    serial_read()
    sleep(10)
# odds_list = test_get_race_odds(args[1])
# print(odds_list)

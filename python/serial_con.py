import csv
import sys
import serial   #モジュール名はpyserialだが, importする際はserialである
from oddsman import oddsman
import time
import serial_con as sc
ow = oddsman.OddsWatcher()


MACHINE_NAME = "/dev/cu.usbmodem14111"
PORT         = "9800"
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

def export(odds_list):
    with serial.Serial( MACHINE_NAME, PORT, timeout=1) as ser:
        no = 1
        odds_list = get_odds_list()
        for odds in odds_list:
            ser.write(str(no).encode('utf-8'))
            print(no)
            time.sleep(2)
            ser.write(str(odds).encode('utf-8'))
            print(odds)
            no += 1
            time.sleep(2)

        ser.write(str(-1).encode('utf-8'))
        ser.close()

def main():
    export()

if __name__ == "__main__":
    args = sys.argv
    test_get_race_odds(args[1])

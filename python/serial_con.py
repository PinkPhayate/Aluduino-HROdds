
import serial   #モジュール名はpyserialだが, importする際はserialである
from oddsman import oddsman
import time

ow = oddsman.OddsWatcher()
race_id = '201702010412'
odds_list = ow.get_race_odds(race_id)
print(odds_list)

def main():
    with serial.Serial('/dev/cu.usbmodem14111',9800,timeout=1) as ser:
        no = 1;
        for odds in odds_list:
            # ser.write(b"015.1")
            ser.write(str(no).encode('utf-8'))
            time.sleep(2)
            ser.write(str(odds).encode('utf-8'))
            no += 1
            time.sleep(2)

        ser.write(str(-1).encode('utf-8'))
        ser.close()
        # while True:
        #     # inp = int(input())
        #     # inp = int(input())
        #
        #     # flag=bytes("1.11",'utf-8')
        #
        #     #シリアル通信で文字を送信する際は, byte文字列に変換する
        #     #input()する際の文字列はutf-8
        #     # inp = 55
        #     # ser.write(inp.to_bytes(2, 'little'))
        #     # ser.write(bytes([inp]))
        #     ser.write(b"015.1")
        #     ser.write(b"016.1")
        #     ser.write(b"034.1")
        #     ser.write(b"0.00")
        #
            # ser.write(bytes(12.3))

            #シリアル通信:送信

            # if(flag==bytes('a','utf-8')):
            #     break;
        # ser.close()

if __name__ == "__main__":
    main()

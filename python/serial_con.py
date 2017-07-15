
import serial   #モジュール名はpyserialだが, importする際はserialである

def main():
    with serial.Serial('/dev/cu.usbmodem14611',9800,timeout=1) as ser:
        while True:
            # inp = int(input())
            inp = int(input())

            # flag=bytes("1.11",'utf-8')

            #シリアル通信で文字を送信する際は, byte文字列に変換する
            #input()する際の文字列はutf-8
            # inp = 55
            # ser.write(inp.to_bytes(2, 'little'))
            # ser.write(bytes([inp]))
            ser.write(b"015.1")

            # ser.write(bytes(12.3))

            #シリアル通信:送信

            # if(flag==bytes('a','utf-8')):
            #     break;
        ser.close()

if __name__ == "__main__":
    main()

import curses
from bluepy.btle import Peripheral
from concurrent.futures import ThreadPoolExecutor

# MACアドレス
MAC = ['']

# RX characteristic UUID
RX_UUID = 'cba20002-224d-11e6-9fb8-0002a5d5c51b'

# REQコマンド (バルブをオン/オフにする)
TURN_ON = bytes([0x57, 0x0f, 0x47, 0x01, 0x01])
TURN_OFF = bytes([0x57, 0x0f, 0x47, 0x01, 0x02])

def control_bulb(mac, command, action):
    '''
    BulbをON/OFFする

    Parameters:
        mac (str): MACアドレス
        command (bytes): コマンド
        action (str): ON/OFF
    '''
    try:
        # デバイスに接続
        with Peripheral(mac) as peripheral:
            # RX characteristicを取得
            rx_char = peripheral.getCharacteristics(uuid=RX_UUID)[0]
            # コマンドを送信
            rx_char.write(command, withResponse=True)
    except Exception as e:
        print(f'Error: {e}')

def main(stdscr):
    try:
        while True:
            key = stdscr.getch()
            if key == ord('0'):  # 0キー
                with ThreadPoolExecutor(max_workers=len(MAC)) as executor:
                    executor.map(lambda mac: control_bulb(mac, TURN_OFF, 'OFF'), MAC)
            elif key == curses.KEY_ENTER or key == 10:  # Enterキー
                with ThreadPoolExecutor(max_workers=len(MAC)) as executor:
                    executor.map(lambda mac: control_bulb(mac, TURN_ON, 'ON'), MAC)
            else:
                print('Detected unrecognized input!!')
    except KeyboardInterrupt:
        print('Exiting the program.')

if __name__ == "__main__":
    curses.wrapper(main)
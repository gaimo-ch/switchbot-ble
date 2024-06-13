from bluepy.btle import Peripheral
from concurrent.futures import ThreadPoolExecutor

# MACアドレス
MAC_ADDR = ['']

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
            print(action)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    # MAC_ADDRの数だけスレッドを立てて並列処理を行う
    with ThreadPoolExecutor(max_workers=len(MAC_ADDR)) as executor:
        # Bulbsをオンにする
        executor.map(lambda mac: control_bulb(mac, TURN_ON, 'ON'), MAC_ADDR)
        # Bulbsをオフにする
        # executor.map(lambda mac: control_bulb(mac, TURN_OFF, 'OFF'), MAC_ADDR)

from bluepy.btle import Peripheral
from concurrent.futures import ThreadPoolExecutor

# MACアドレス
MAC_ADDRESS = ['']

# RX characteristic UUID
RX_UUID = 'cba20002-224d-11e6-9fb8-0002a5d5c51b'

# REQコマンド
TURN_ON = bytes([0x57, 0x01, 0x01])
TURN_OFF = bytes([0x57, 0x01, 0x02])
WHITE = bytes([0x57, 0x0F, 0x47, 0x01, 0x13, 0x64, 0x19])
ORANGE = bytes([0x57, 0x0F, 0x47, 0x01, 0x12, 0x64, 0xFC, 0x60, 0x12])

def control_bulb(mac_address, command, message):
    '''
    BulbをON/OFFする

    Parameters:
        mac (str): MACアドレス
        command (bytes): コマンド
        message (str): ON/OFF
    '''
    try:
        # デバイスに接続
        with Peripheral(mac_address) as peripheral:
            # RX characteristicを取得
            rx_char = peripheral.getCharacteristics(uuid=RX_UUID)[0]
            # コマンドを送信
            rx_char.write(command, withResponse=True)
            print((f'Bulb is {message}'))
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    # MAC_ADDRの数だけスレッドを立てて並列処理を行う
    with ThreadPoolExecutor(max_workers=len(MAC_ADDRESS)) as executor:
        # Bulbsをオンにする
        executor.map(lambda mac_address: control_bulb(mac_address, TURN_ON, 'ON'), MAC_ADDRESS)
        # Bulbsをオフにする
        # executor.map(lambda mac_address: control_bulb(mac_address, TURN_OFF, 'OFF'), MAC_ADDRESS)
        # Bulbsを白色にする
        # executor.map(lambda mac_address: control_bulb(mac_address, WHITE, 'WHITE'), MAC_ADDRESS)
        # Bulbsをオレンジ色にする
        # executor.map(lambda mac_address: control_bulb(mac_address, ORANGE, 'ORANGE'), MAC_ADDRESS)


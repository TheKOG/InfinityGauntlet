import bluetooth
import time
from record import Record
from snap import is_Snap,Load
import torchaudio

class BluetoothConnection:
    def __init__(self):
        self.find = True
        self.nearby_devices = None
 
    def find_nearby_devices(self):
        print("Detecting nearby Bluetooth devices...")
        loop_num = 3
        i = 0
        self.nearby_devices = bluetooth.discover_devices()
        while self.nearby_devices.__len__() == 0 and i < loop_num:
            self.nearby_devices = bluetooth.discover_devices()
            if self.nearby_devices.__len__() > 0:
                break
            i = i + 1
            time.sleep(2)
            print("No Bluetooth device around here! trying again {}...".format(str(i)))
        if not self.nearby_devices:
            print("There's no Bluetooth device around here. Program stop!")
        else:
            print("{} nearby Bluetooth device(s) has(have) been found:".format(self.nearby_devices.__len__()), self.nearby_devices)
 
    def find_target_device(self, target_name):
        self.find_nearby_devices()
        if self.nearby_devices:
            # print(self.nearby_devices)
            for addr in self.nearby_devices:
                # print(addr)
                print(bluetooth.lookup_name(addr))
                if bluetooth.lookup_name(addr)==target_name:
                    print("Found target bluetooth device with address:{} name:{}".format(addr, target_name))
                    self.find = True
                    return addr
            if not self.find:
                print("could not find target bluetooth device nearby. "
                      "Please turn on the Bluetooth of the target device.")
        return None
 
    def connect_target_device(self, target_name):
        target_address=self.find_target_device(target_name=target_name)
        # target_address='54:43:B2:AC:D7:8E'
        # print('fuckpps')
        if(target_address==None):
            print("device not found.")
            return
        print("Ready to connect")
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((target_address, 1))
        print("Connection successful. Now ready to send the data")
        print("counting")
        timeset=0
        while True:
            Record("tmp/tmp.wav",debug=False)
            timeset+=1
            if(timeset%60==0):
                sock.send("TEST")
                timeset=0
            waveform,sample_rate = torchaudio.load("tmp/tmp.wav")
            if(waveform.numpy()[0].max()<0.06):
                continue
            val=is_Snap("tmp/tmp.wav")
            if(val>0.9):
                print("Snap!")
                sock.send("SWITCH")

if __name__ == '__main__':
    target_name = "ESP32_KOG"
    Load('pth/best_pth')
    while True:
        try:
            BluetoothConnection().connect_target_device(target_name=target_name)
        except:
            pass
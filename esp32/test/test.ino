/*
 * ESP32BLE控制舵机实现开关灯
 * 新增315MHz无线遥控<------>11.23
 * Author:猿一
 * 2021.11.14
 */

#include "BluetoothSerial.h"
#include "Servo.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;
Servo servo1,servo2;
static const int servoPin1 = 22;
static const int servoPin2 = 13;
static const int OpenParameter = 70;   //开启开关舵机的角度
// static const int CloseParameter = 5; //关闭开关舵机的角度
static const int ResetParemeter = 0; //舵机复位角度
String readMsg = "";
int state=0;
void setup(){
  Serial.begin(115200);
  SerialBT.begin("ESP32_KOG"); //蓝牙设备名称
  delay(50);
  Serial.println("The device started, now you can pair it with bluetooth!");
  servo1.attach(
    servoPin1,
    Servo::CHANNEL_NOT_ATTACHED,
    0,
    180
  );
  servo1.write(ResetParemeter);
  servo2.attach(
    servoPin2,
    Servo::CHANNEL_NOT_ATTACHED,
    0,
    180
  );
  servo2.write(ResetParemeter);
}
/*
   蓝牙串口接收
*/
void ReceiverBleMessage(){
  while (SerialBT.available() > 0){
    readMsg += char(SerialBT.read());
    delay(2);
  }
}
void loop(){
  ReceiverBleMessage();
  if(readMsg == "SWITCH"){
    if(state==0){
      servo1.write(OpenParameter);
      delay(500);
      servo1.write(ResetParemeter);
      Serial.print("Receiver:");
      Serial.println(readMsg);
    }else{
      servo2.write(OpenParameter);
      delay(500);
      servo2.write(ResetParemeter);
      Serial.print("Receiver:");
      Serial.println(readMsg);
    }
    state=1-state;
  }
  readMsg="";
}




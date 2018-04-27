#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3);//设置模拟串口针脚(RX, TX)
String WiFiSSID = "Honor 8";//无线路由器Wi-Fi名称
String WiFiPASSWORD = "947432168";//无线路由器Wi-Fi密码
int flag = 0;
void setup() {
  Serial.begin(9600);
  mySerial.begin(115200);//设置模拟串口波特率
}
void loop() {
  if(flag == 0){
  delay(10000);  //等待ESP8266通电启动
  mySerial.print("+++");
  delay(1000);
  mySerial.print("AT\r\n");//进入AT指令模式
  delay(1000);
  mySerial.print("ATE0\r\n");//关闭AT指令回显
  delay(1000);
  mySerial.print("AT+CWMODE=3\r\n");//作为客户端接入Wi-Fi网络  
  delay(2000);
  mySerial.print("AT+CWJAP=\"");//连接到无线路由器
  mySerial.print(WiFiSSID);
  mySerial.print("\",\"");
  mySerial.print(WiFiPASSWORD);
  mySerial.print("\"\r\n");
  delay(20000);
  mySerial.print("AT+CIPMUX=0\r\n");  //设置为单连接
  delay(1000);
  mySerial.print("AT+CIPMODE=1\r\n");  //设置模块传输模式为TCP客户端模式
  delay(1000);
  mySerial.print("AT+SAVETRANSLINK=1,\"118.25.39.129\",8080,\"TCP\"\r\n");  //连接物联网云平台的TCP服务端，端口8181，服务器地址121.42.180.30
  delay(20000);
  mySerial.print("AT+RST\r\n");  //重启
  flag=1;
}
}

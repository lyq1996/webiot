# webiot
A Iot System Based On Web.  
基于Web的物联网系统。

## 介绍
这是我的毕业设计，主要实现了下面两个功能:

* 网页上控制照明灯等家电的开关
* 网页上监控环境温湿度(暂未完成，以后有时间再搞)

剩下的有时间再写。

## Demo
> http://118.25.39.129/ (服务器已过期)

![Aaron Swartz](https://raw.githubusercontent.com/lyq1996/webiot/master/demo.png)  

![Aaron Swartz](https://raw.githubusercontent.com/lyq1996/webiot/master/demo_1.png)

## 思路
### 服务器与单片机
1. 市面上有很多串口Wi-Fi芯片，我选用的一款ESP8266。将ESP8266与单片机连接在一起，就实现了单片机的网络接入。
2. 串口Wi-Fi芯片联网后，设置工作模式在TCP client，与服务器的TCP Server相连接。
3. 此时，服务器发往串口Wi-Fi芯片的数据都将被单片机的串口所接收。
4. 单片机主程序读取串口，作出相对应的操作。

### 服务器与Web页面
1. Web页面为用户提供一个提交按钮和开关状态选框，点击提交后json数据将通过GET的方式，传递到运行在后端的PHP程序。
2. 后端PHP程序将当前开关状态写入到本地的status.json(我一点都不会数据库啊)

### TCP Server的工作
1. TCP Server不断的读取本地的status.json，查看是否更改了开关的状态
2. 如果更改，发到TCP Client上。
3. 如果没有更改，继续读取本地status.json。
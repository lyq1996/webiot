import socket
import time     
import sys
import threading
import json

class MainClass():
        def init(self):
                self.threads = []
                self.host = '10.105.121.191'
                self.port = 8080
                print 'Start a socket:TCP...'
                self.socket_tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	        self.socket_tcp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)   
                self.socket_tcp.bind((self.host,self.port))
                self.socket_tcp.listen(5)
                print 'TCP listen in %s:%d'%(self.host,self.port)
                try:	
                        while True:
           			print 'Waiting Client to Connect...'
                                self.socket_con,self.addr = self.socket_tcp.accept()
                                client_ip,port = self.addr
                                print 'Client Connected, IP:',client_ip,'Port:',port
                                self.StartThreads()
                except KeyboardInterrupt:
			self.socket_tcp.close()
                        self.stop_thread()
			sys.exit()	
        
        def StartThreads(self):
                thread = WorkThread(self.socket_con,self.addr)
                thread.start()
                self.threads.append(thread)

        def stop_thread(self):
                while self.threads:
                        try:
                                thread_num = len(self.threads)
                                for i in range(thread_num):
                                        thread = self.threads[i]
                                        thread.stop()
                                time.sleep(0.1)
                                print self.threads
                                self.threads = []
                                return
                        except Exception,error:
                                print 'Threading Stop Error:'
                                print error


class WorkThread(threading.Thread):
        def __init__(self,socket_arg,addr):
                threading.Thread.__init__(self)
                self.connect = socket_arg
                self.connect.settimeout(1)
                self.ip,self.port = addr
                self.ifdo = True
                try:
                        with open('/home/wwwroot/iotlyqip/web/status.json') as json_file:
                                json_data = json.load(json_file)
                                self.efan = json_data['efan']
                                self.light = json_data['light']
                                self.led = json_data['led']
                                json_file.close()
                except Exception,error:
                        print 'Client Checkout! Reason:'
                        print error
                        self.ifdo = False
                if self.ifdo:
                        tosendjson = {"object": "efan","control": self.efan}
                        datarecv = self.datasend(json.dumps(tosendjson))
                        if datarecv:
                                print datarecv
                if self.ifdo:
                        tosendjson = {"object": "light","control": self.light}
                        datarecv = self.datasend(json.dumps(tosendjson))
                        if datarecv:
                                print datarecv
                if self.ifdo:
                        tosendjson = {"object": "led","control": self.led}
                        datarecv = self.datasend(json.dumps(tosendjson))
                        if datarecv:
                                print datarecv
                
        def stop(self):
                self.ifdo = False

        def datasend(self, data):
                try:
                        self.connect.send(data+'\n')
                        recvdata =self.connect.recv(1024)
                except Exception,error:
                        print 'Client Checkout! Reason:'
                        print error
                        self.ifdo = False
                        return
                return recvdata

        def run(self):
                while self.ifdo:
                        try:
                                with open('/home/wwwroot/iotlyqip/web/status.json') as json_file:
                                        json_data = json.load(json_file)
                                        efan1 = json_data['efan']
                                        light1 = json_data['light']
                                        led1 = json_data['led']
                                        json_file.close()
                                        if efan1 != self.efan:
                                                self.efan = efan1
                                                tosendjson = {"object": "efan","control": self.efan}
                                                recvdata = self.datasend(json.dumps(tosendjson))       
                                                if not recvdata:
                                                        break
                                                print recvdata
                                        if light1 != self.light:
                                                self.light = light1
                                                tosendjson = {"object": "light","control": self.light}
                                                recvdata = self.datasend(json.dumps(tosendjson))       
                                                if not recvdata:
                                                        break
                                                print recvdata
                                        if led1 != self.led:
                                                self.led = led1
                                                tosendjson = {"object": "led","control": self.led}
                                                recvdata = self.datasend(json.dumps(tosendjson))       
                                                if not recvdata:
                                                        break
                                                print recvdata
                        except Exception,error:
                                print 'Error While Loading Json:'
                                print error
                                continue                                               
                self.connect.close()
                print 'Disconnect with:%s'%(self.ip)

tcpserver = MainClass()
tcpserver.init()
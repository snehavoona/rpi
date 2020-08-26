
import RPi.GPIO as GPIO
import time
from socket import *


def server(ipAddr,port):
    server = socket(AF_INET,SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        server.bind((ipAddr,port))
        server.listen(5)
        while(1):
            (clientsock,addr) = server.accept()
            rd = clientsock.recv(5000).decode()
            client_data = rd.split("\n")
            print("received data from %s"%(str(addr)))
            res_data = "HTTP/1.1 200 OK\r\nContent-Type:application/json;\nAccess-Control-Allow-Origin:*\ncharset=utf-8\r\n\r\n"
            #res_data += "<html><body>connected</body><html>\r\n\r\n"
            if(len(client_data)>0):
                #print("--------dddddd---------",client_data)
                print("client data----",client_data[0])
                data = client_data[0].split()[1].replace("/","").split("?")
                params_list = [p for p in data if p]
                params_list=[ x.split("=") for x in params_list]
                params={}
                for x,y in params_list:
                    params.update({x:y})

                callFun(params['id'])
            res_data +='{"status":true}'
			#res_data += '{"status":true}'
            #res_data +="<html><button type="button" onclick="alert(\'You ressed the button!\')">TRIPOD TURNSTILE</button></html>"
            clientsock.send(res_data.encode())
            clientsock.shutdown(SHUT_WR)
    except KeyboardInterrupt:
        print("server stopped")
    except Exception as e:
        print("error ",e)
    server.close()

def callFun(a):
    print("exeuted ----",a)
    GPIO.setmode(GPIO.BCM)

    in1 = 23
    in2 = 24
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    #while True:
    for x in range(10):
    	GPIO.output(in1, GPIO.HIGH)
    	time.sleep(0.2)
    	GPIO.output(in1, GPIO.LOW)
    	#GPIO.output(in2, GPIO.HIGH)
    	time.sleep(0.2)
    	#GPIO.output(in2, GPIO.LOW)

    GPIO.cleanup()


print("starting server")
server("10.60.62.69",8002)
#callFun(1)




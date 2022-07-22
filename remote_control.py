import os
import json
import keyboard
import urllib3.request
import time

## Lower the number, higher the accuracy
## This number should smaller than 2
accuracy = 0.15


camera_hostname = "192.168.100.99" 



class Controller:
    def __init__(self) -> None:
        print("Activate Camera Controller")
    
    def ping_camera(self):
        print("Ping Camera")
        response = os.system("ping  " + camera_hostname)
        #and then check the response...
        if response == 0:
            print(camera_hostname, 'is up!')
        else:
            print(camera_hostname, 'is down!')
            
    def send_zoom_in_command(self):
        print("Send Zoom In Command")
        try:
            http = urllib3.PoolManager()
            response_zoom_in = http.request('GET', 'http://192.168.100.99/cgi-bin/ptzctrl.cgi?ptzcmd&zoomin&5',timeout=2.50)
        except urllib3.exceptions.NewConnectionError:
        # Maybe set up for a retry, or continue in a retry loop
            print("Zoom in Command Timeout")
            return
        
        time.sleep(accuracy)

        try:
            response_stop = http.request('GET','http://192.168.100.99/cgi-bin/ptzctrl.cgi?ptzcmd&zoomstop&5', timeout=2.50)
        except urllib3.exceptions.NewConnectionError:
        # Maybe set up for a retry, or continue in a retry loop
            print("Zoom stop Command Timeout")
            return
        
        
        if (response_zoom_in.status == 200 and response_stop.status == 200):
            print("Zoom in successfully")
        else:
            print("Zoom In Failure")
            print('Response Content 1:\n',response_zoom_in.data)
            print('Response Content 2:\n',response_stop.data)
    
    def send_zoom_out_command(self):
        print("Send Zoom Out Command")
        http = urllib3.PoolManager()

        
        try:
            response_zoom_out = http.request('GET','http://192.168.100.99/cgi-bin/ptzctrl.cgi?ptzcmd&zoomout&5', timeout=2.50)
        except urllib3.exceptions.NewConnectionError:
        # Maybe set up for a retry, or continue in a retry loop
            print("Zoom Out Command Timeout\n")
            return

        time.sleep(accuracy)
        
        try:
            response_stop = http.request('GET', 'http://192.168.100.99/cgi-bin/ptzctrl.cgi?ptzcmd&zoomstop&5', timeout=2.50)
        except urllib3.exceptions.NewConnectionError:
        # Maybe set up for a retry, or continue in a retry loop
            print("Zoom Out Command Timeout\n")
            return
        
        if (response_zoom_out.status == 200 and response_stop.status == 200):
            print("Zoom Out successfully")
        else:
            print("Zoom Out Failure")
            print('Response Content 1:\n',response_zoom_out.data)
            print('Response Content 2:\n',response_stop.data)
            
    def listen_command(self):
        while(True):
            temp_ley = keyboard.read_key()
            if temp_ley == "":
                continue
            elif temp_ley == "q":
                print("Quit the controller.\n")
                break
            elif temp_ley == "i":
                self.send_zoom_in_command()
            elif temp_ley == "o":
                self.send_zoom_out_command()
            elif temp_ley == "p":
                self.ping_camera()
            elif temp_ley == "h":
                print("'p': Ping the camera.")
                print("'i': Camera zoom in.")
                print("'o': Camera zoom out.")
                print("'q': Exit camera controller.\n")
            else:
                print("Print 'h' to see the manual\n")
                
        

if __name__ == "__main__":
    controller = Controller()
    controller.listen_command()

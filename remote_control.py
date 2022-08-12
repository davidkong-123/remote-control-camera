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

        ##zoom level is from 0 to 36
        self.zoom_level = 0
    
    def ping_camera(self):
        print("Ping Camera")
        response = os.system("ping  " + camera_hostname)
        #and then check the response...
        if response == 0:
            print(camera_hostname, 'is up!')
        else:
            print(camera_hostname, 'is down!')

    def set_zoom_level(self, level):
        if self.zoom_level == level:
            print(f"Current zoom level is {level} already")
            return
        elif self.zoom_level > level:
            offset = zoom_level - level
            for i in range(offset):
                self.send_zoom_out_command()
            zoom_level = level
        else:
            offset = level - zoom_level
            for i in range(offset):
                self.send_zoom_in_command()
        print(f"Set current level to {zoom_level} successfully")
            

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
            self.count += 1
            print("zoom in count:", self.count)
        else:
            print("Zoom In Failure")
            print('Response Content 1:\n',response_zoom_in.data)
            print('Response Content 2:\n',response_stop.data)
    
    def zoom_out_all(self):
        for i in range(40):
            send_zoom_out_command()
        print("Finish zoom out all")

    def zoom_in_all(self):
        for i in range(40):
            send_zoom_in_command()
        print("Finish zoom in all")

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
            temp_key = keyboard.read_key()
            if temp_key == "":
                continue
            elif temp_key == "q":
                print("Quit the controller.\n")
                break
            elif temp_key == "i":
                self.send_zoom_in_command()
            elif temp_key == "o":
                self.send_zoom_out_command()
            elif temp_key == "p":
                self.ping_camera()
            elif temp_key == "a":
                self.zoom_out_all()
            elif temp_key == "w":
                self.zoom_in_all()
            elif temp_key == "h":
                print("'p': Ping the camera.")
                print("'i': Camera zoom in one level.")
                print("'o': Camera zoom out one level.")
                print("'a': Camera zoom in to max level.")
                print("'w': Camera zoom out to min level.")
                print("'q': Exit camera controller.\n")
            else:
                print("Print 'h' to see the manual\n")
                
        

if __name__ == "__main__":
    controller = Controller()
    controller.listen_command()

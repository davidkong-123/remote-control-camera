import requests
import os
import keyboard


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
            response_zoom_in = requests.get('http://192.168.100.99/cgi-bin/ptzctrl.cgi?5=&ptzcmd=&zoomin=', timeout=2.50)
        except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
            print("Zoom in Command Timeout")
            return
        
        try:
            response_stop = requests.get('http://192.168.100.99/cgi-bin/ptzctrl.cgi?5=&ptzcmd=&zoomstop=', timeout=2.50)
        except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
            print("Zoom stop Command Timeout")
            return
        
        
        if (response_zoom_in.status_code == 200 and response_stop.status_code == 200):
            print("Zoom in successfully")
        else:
            print("Zoom In Failure")
            print('Response Content 1:\n',response_zoom_in.text)
            print('Response Content 2:\n',response_stop.text)
    
    def send_zoom_out_command(self):
        print("Send Zoom Out Command")
        try:
            response_zoom_out = requests.get('http://192.168.100.99/cgi-bin/ptzctrl.cgi?5=&ptzcmd=&zoomout=', timeout=2.50)
        except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
            print("Zoom Out Command Timeout\n")
            return
        
        try:
            response_stop = requests.get('http://192.168.100.99/cgi-bin/ptzctrl.cgi?5=&ptzcmd=&zoomstop=', timeout=2.50)
        except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
            print("Zoom Out Command Timeout\n")
            return
        
        if (response_zoom_out.status_code == 200 and response_stop.status_code == 200):
            print("Zoom Out successfully")
        else:
            print("Zoom Out Failure")
            print('Response Content 1:\n',response_zoom_out.text)
            print('Response Content 2:\n',response_stop.text)
            
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

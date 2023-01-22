import pyqrcode
from pyqrcode import create
import tkinter as tk
from tkinter import * 
import http.server
import socketserver
import threading
import socket
import os
from PIL import Image, ImageTk

# Window configuration
my_w = tk.Tk()
my_w.resizable(False, False)
my_w.title("File share")
my_w.eval('tk::PlaceWindow . center')
w_width = 640
w_height = 360
padding_x= (my_w.winfo_screenwidth()/2) - (w_width/2)
padding_y = (my_w.winfo_screenheight()/2) - (w_height/2)
my_w.geometry('%dx%d+%d+%d' % (w_width, w_height, padding_x, padding_y))

# Qrcode generate Button
generate_button = tk.Button(my_w,font=22,text='Generate QR code', command=lambda:my_generate())
generate_button.place(relx=0.2, rely=0.5, anchor=CENTER)

# Qrcode image position
qrcode_label=tk.Label(my_w)
qrcode_label.place(relx=0.6, rely=0.5, anchor=CENTER)

host_name=tk.Label(my_w)
host_name.place(relx=0.1, rely=0.6)

host_url=tk.Label(my_w)
host_url.place(relx=0.1, rely=0.7)

# Server configuration
PORT = 8010
os.environ['USERPROFILE']
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']),'Desktop')
os.chdir(desktop)
Handler = http.server.SimpleHTTPRequestHandler
hostname = socket.gethostname()

socket_info = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_info.connect(("8.8.8.8", 80))
link = "http://" + socket_info.getsockname()[0] + ":" + str(PORT)

def my_generate():
    global my_img
    my_qr = pyqrcode.create(link) 
    my_qr.png("temp_qrcode.png", scale=10)
    my_img=ImageTk.PhotoImage(Image.open("temp_qrcode.png").resize((250,250), Image.Resampling.LANCZOS))
    qrcode_label.config(image=my_img)
    host_name.config(text=hostname)
    host_url.config(text=link)   

def serve_forever():
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    httpd.serve_forever()

if __name__ == '__main__':
    my_w.mainloop()
    server_thread = threading.Thread(target=serve_forever)
    server_thread.start()


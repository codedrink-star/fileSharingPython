import socket
import os, png
import pyqrcode
import http.server
import socketserver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-P", help="Directory Path", required=True)
parser.add_argument("-p", help="Port Number", default=443)
args = vars(parser.parse_args())

os.chdir(args["P"])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipAddress = s.getsockname()[0]
s.close()

url = "http://" + ipAddress + ":" + str(args["p"])
qrCode = pyqrcode.create(url)
qrCode.png("qr.png", scale=6)

httpRequestHandler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", args["p"]), httpRequestHandler) as httpd:
    print("Target URL:", url)
    httpd.serve_forever()
import time
import utils
import socket
import os, signal
import subprocess
import tkinter as tk
from tkinter import filedialog

process_id = 0
labelFive = ""
imgLabel = ""
mainFrame = tk.Tk()
directoryPath = tk.StringVar(mainFrame)
mainFrame.configure(background="#070f4e")
mainFrame.geometry("700x420")
mainFrame.resizable(False, False)
mainFrame.title("CodeDrink File Share")
mainFrame.columnconfigure(0, weight=3)
mainFrame.columnconfigure(1, weight=1)

obj = utils.createLabel("Select Folder Location")
labelOne = tk.Label(
    mainFrame,
    text="{0}".format(obj.text),
    background=obj.background,
    foreground=obj.foreground,
    font=("verdana", 12, "bold"),
)
labelOne.grid(column=0, row=0, sticky=tk.NW, padx=25, pady=15)

obj = utils.createLabel("Which folder to be shared?")
labelTwo = tk.Label(
    mainFrame,
    text="{0}".format(obj.text),
    background=obj.background,
    foreground=obj.foreground,
    font=("verdana", 10),
)
labelTwo.grid(column=0, row=0, sticky=tk.NW, padx=45, pady=36)

obj = utils.createLabel("Program will share all files present in selected folder.")
labelThree = tk.Label(
    mainFrame,
    text="{0}".format(obj.text),
    background=obj.background,
    foreground=obj.foreground,
    font=("verdana", 10),
)
labelThree.grid(column=0, row=0, sticky=tk.NW, padx=45, pady=80)

obj = utils.createLabel("To select a location, click Browse.")
labelFour = tk.Label(
    mainFrame,
    text="{0}".format(obj.text),
    background=obj.background,
    foreground=obj.foreground,
    font=("verdana", 10, "bold"),
)
labelFour.grid(column=0, row=0, sticky=tk.NW, padx=45, pady=100)

textBox = tk.Entry(mainFrame, width=85, textvariable=directoryPath)
textBox.grid(column=0, row=0, sticky=tk.NW, padx=45, pady=135, ipady=3)


def browseButton():
    path = filedialog.askdirectory()
    directoryPath.set(path)


buttonOne = tk.Button(mainFrame, text="Browse", width=10, command=browseButton)
buttonOne.grid(column=0, row=0, sticky=tk.NE, padx=30, pady=135)


def shareButton():
    path = directoryPath.get()
    process = subprocess.Popen(["python", "share.py", "-P", path])
    print("Process forked with ID: ", process.pid)
    global process_id
    process_id = process.pid
    waitForQr()
    showTextMsg()


buttonTwo = tk.Button(mainFrame, text="Share", width=10, command=shareButton)
buttonTwo.grid(column=0, row=0, sticky=tk.NE, padx=116, pady=330)


def stopButton():
    try:
        print("Terminating Process with ID: ", process_id)
        os.kill(process_id, signal.SIGTERM)
        print("Terminated..!!")
        os.remove(str(directoryPath.get() + "/qr.png"))
    except OSError as err:
        print("Error occurred..", err)


buttonThree = tk.Button(mainFrame, text="Stop", width=10, command=stopButton)
buttonThree.grid(column=0, row=0, sticky=tk.NE, padx=30, pady=330)


def waitForQr():
    qrPath = str(directoryPath.get() + "/qr.png")
    while not os.path.exists(qrPath):
        time.sleep(1)
    global imgLabel
    imgLabel = tk.PhotoImage(file=qrPath)
    global labelFive
    labelFive = tk.Label(mainFrame)
    labelFive.config(image=imgLabel)
    labelFive.grid(column=0, row=0, sticky=tk.NW, padx=45, pady=177)
    labelFive.config(image=imgLabel)


def showTextMsg():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    obj = utils.createLabel(
        "Scan QR Code or Open link http://{0}:443 in Browser".format(s.getsockname()[0])
    )
    labelSix = tk.Label(
        mainFrame,
        text="{0}".format(obj.text),
        background=obj.background,
        foreground=obj.foreground,
        font=("verdana", 10),
        wraplength=250,
    )
    labelSix.grid(column=0, row=0, sticky=tk.NE, padx=30, pady=177)


mainFrame.mainloop()
import tkinter
from tkinter import *
from tkinter import messagebox
import time
import serial.tools.list_ports
import warnings

global ser
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Arduino' in p.description
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduino found - using the first')

ports = serial.tools.list_ports.comports()
print(arduino_ports[0])
time.sleep(1)


def connect():
    global ser

    try:
        ser = serial.Serial(arduino_ports[0])
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        connect_button.config(state=tkinter.DISABLED)
        disconnect_button.config(state=tkinter.NORMAL)
        time.sleep(0.5)
    except serial.SerialException:
        messagebox.showerror("Error", "Cannot connect, please restart")


def disconnect():
    global ser
    if ser is not None and ser.is_open:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.close()
        connect_button.config(state=tkinter.NORMAL)
        disconnect_button.config(state=tkinter.DISABLED)


def burstgenerator():
    global ser
    try:
        pulsecount = int(ib.get())
        if pulsecount == int(ib.get()):
            selection = 'P ' + str(pulsecount) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection.encode('utf-8'))
            print(selection)
    except ValueError:
        messagebox.showerror("Error", "Please enter an integer from 1 to 65,535")
    except (serial.SerialException, NameError):
        messagebox.showerror("Error", "Connect to an Arduino")
    # except NameError:
    #    messagebox.showerror("Error", "Connect to an Arduino")


def poweron():
    try:
        selection = 'POWERON\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        b5.config(state=tkinter.DISABLED)
        b6.config(state=tkinter.NORMAL)
        print(selection)
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def poweroff():
    try:
        selection = 'POWEROFF\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        b6.config(state=tkinter.DISABLED)
        b5.config(state=tkinter.NORMAL)
        print(selection)
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def latch():
    try:
        selection = 'LATCH\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        print(selection)
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def start():
    try:
        starting = 'START\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(starting.encode('utf-8'))
        print(starting)
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def resetting():
    try:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.close()
        time.sleep(1)
        ser.open()
        b6.config(state=tkinter.DISABLED)
        b5.config(state=tkinter.NORMAL)
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


root = Tk()
root.geometry()
root.title("Thesis Interface V0.1")
l1 = Label(root, text="OSL Interface v0.1", font="bold")
l2 = Label(root, text="Enter Pulse Count", font="bold")
b1 = Button(root, text='Send Number', command=burstgenerator, height=2, width=15, bg='white', activebackground='green')
b2 = Button(root, text="Latch", command=latch, height=2, width=15, bg='white', activebackground='blue')
b3 = Button(root, text="Start Countdown", command=start, height=2, width=15, bg='white', activebackground='red')
b4 = Button(root, text="Reset", command=resetting, height=2, width=15, bg='white', activebackground='black')
l3 = Label(root, text=arduino_ports[0])
# l4 = Label(root, text=str(ser))
ib = Entry(justify=LEFT)
connect_button = Button(root, text="Connect", command=connect)
disconnect_button = Button(root, text="Disconnect", command=disconnect)
b5 = Button(root, text="Power On", command=poweron, height=2, width=15)
b6 = Button(root, text="Power Off", command=poweroff, height=2, width=15)
l1.grid(row=0, column=1)
l2.grid(row=1, column=1)
ib.grid(row=2, column=1)
b1.grid(row=3, column=1)
b2.grid(row=4, column=1)
b3.grid(row=5, column=1)
b4.grid(row=6, column=1)
l3.grid(row=7, column=1)
# l4.grid(row=8, column=1)
connect_button.grid(row=9, column=1)
disconnect_button.grid(row=10, column=1)
b5.grid(row=1, column=0)
b6.grid(row=2, column=0)
root.mainloop()

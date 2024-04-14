from tkinter import *
import time
import serial.tools.list_ports
import warnings

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Arduino' in p.description
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

ser = serial.Serial(arduino_ports[0], 9600)
ports = serial.tools.list_ports.comports()
print(ports[0])
print(ser)
time.sleep(1)


def burstgenerator():
    pulsecount = int(ib.get())
    selection = 'P ' + str(pulsecount) + '\n\r'
    ser.write(selection.encode('utf-8'))
    print(selection)


def latch():
    selection = 'LATCH\n\r'
    ser.write(selection.encode('utf-8'))
    print(selection)


def start():
    starting = 'START\n\r'
    ser.write(starting.encode('utf-8'))
    print(starting)


def resetting():
    ser.close()
    ser.open()


root = Tk()
root.geometry()
root.title("Thesis Interface V0.1")
l1 = Label(root, text="OSL Interface v0.1", font= "bold")
l2 = Label(root, text="Enter Pulse Count",font= "bold")
b1 = Button(text='Send Number', command=burstgenerator, height=2, width=15,bg='white',activebackground='green')
b2 = Button(root, text="Latch", command=latch, height=2, width=15,bg='white',activebackground='blue')
b3 = Button(root, text="Start Countdown", command=start, height=2, width=15,bg='white',activebackground='red')
b4 = Button(root, text="Reset", command=resetting, height=2, width=15,bg='white',activebackground='black')
l3 = Label(root, text=ports[0])
l4= Label(root, text= str(ser))
ib = Entry(justify=LEFT)

l1.grid(row=0, column=1)
l2.grid(row=1, column=1)
ib.grid(row=2, column=1)
b1.grid(row=3, column=1)
b2.grid(row=4, column=1)
b3.grid(row=5, column=1)
b4.grid(row=6, column=1)
l3.grid(row=7, column=1)
l4.grid(row=8, column=1)


root.mainloop()

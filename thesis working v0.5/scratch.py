import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import time
import serial.tools.list_ports
import warnings
import os
from tkinter import filedialog as fd

frequency = 0
illuminate = 0
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
        b15.config(state=tkinter.DISABLED)
        b16.config(state=tkinter.NORMAL)
        time.sleep(0.5)
    except serial.SerialException:
        messagebox.showerror("Error", "Cannot connect, please restart")


def run():
    try:
        os.startfile(file_path)
    except NameError:
        messagebox.showerror("Error", "Please select the file path from the menu bar")
    except Exception:
        messagebox.showerror('Error', "System Cannot Find the File Specified")


def disconnect():
    global ser
    if ser is not None and ser.is_open:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.close()
        b15.config(state=tkinter.NORMAL)
        b16.config(state=tkinter.DISABLED)


def resetstate():
    pb.config(state=tkinter.NORMAL)
    db.config(state=tkinter.NORMAL)


def poweron():
    try:
        selection = 'POWERON\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        b5.config(state=tkinter.DISABLED)
        b6.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
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
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def latch():
    try:
        selection = 'LATCH\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def start():
    try:
        starting = 'START\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(starting.encode('utf-8'))
        print(starting)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
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
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def frequencyselection():
    try:
        db.config(state="disabled")
        pb.config(state=tkinter.NORMAL)
        global seconds
        selection = freqcombo.get()
        freq = float(pb.get())
        if selection == "kHz":
            value = 1000
            frequency = int(value * freq)
            seconds = frequency
            selection5 = 'F ' + str(seconds) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection5.encode('utf-8'))
            print("selection5")
            print(selection5)
        elif selection == "MHz":
            value = 1000000
            frequency = int(value * freq)
            seconds = frequency
            selection5 = 'F ' + str(seconds) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection5.encode('utf-8'))
            print("selection5")
            print(selection5)
    except ValueError:
        messagebox.showerror("Error", "Please enter a number")
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")


def dwellselection():
    try:
        pb.config(state="disabled")
        db.config(state=tkinter.NORMAL)
        global seconds
        selection3 = dwellcombo.get()
        dwell = float(db.get())
        if selection3 == "ns":
            value = 0.000000001
            frequencydwell = 1/(dwell * value)
            frequencydwell = round(frequencydwell, 6)
            frequencydwell = int(frequencydwell)
            seconds = frequencydwell
            selection4 = 'F ' + str(seconds) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection4.encode('utf-8'))
            print("selection4")
            print(selection4)
        elif selection3 == "us":
            value = 0.000001
            frequencydwell = 1 / (dwell * value)
            frequencydwell = round(frequencydwell, 6)
            frequencydwell = int(frequencydwell)
            seconds = frequencydwell
            selection4 = 'F ' + str(seconds) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection4.encode('utf-8'))
            print("selection4")
            print(selection4)
        elif selection3 == "ms":
            value = 0.001
            frequencydwell = 1 / (dwell * value)
            frequencydwell = round(frequencydwell, 6)
            frequencydwell = int(frequencydwell)
            seconds = frequencydwell
            selection4 = 'F ' + str(seconds) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection4.encode('utf-8'))
            print("selection4")
            print(selection4)
        elif selection3 == "s":
            value = 1
            frequencydwell = 1 / (dwell * value)
            frequencydwell = round(frequencydwell, 6)
            frequencydwell = int(frequencydwell)
            seconds = frequencydwell
            selection4 = 'F ' + str(seconds) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection4.encode('utf-8'))
            print("selection4")
            print(selection4)
    except ValueError:
        messagebox.showerror("Error", "Please enter a number")
    except (serial.SerialException, NameError):
        messagebox.showerror("Error", "Connect to an Arduino")


def timeselection():
    try:
        global illuminate
        global multiplier
        selection2 = lightcombo.get()
        time = float(tb.get())
        if selection2 == "ns":
            multiplier = 1 / seconds
            time = time * 0.000000001
            multiplier = float(multiplier)
            illuminate = time / multiplier
            illuminate = round(illuminate)
            selected = str(illuminate)
            l5.config(text=selected)
            selection3 = 'P ' + str(selected) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection3.encode('utf-8'))
            print("selection3")
            print(selection3)
        elif selection2 == "us":
            multiplier = 1 / seconds
            time = time * 0.000001
            multiplier = float(multiplier)
            illuminate = time / multiplier
            illuminate = round(illuminate)
            print(illuminate)
            selected = str(illuminate)
            print("selection")
            print(illuminate)
            l5.config(text=selected)
            selection3 = 'P ' + str(selected) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection3.encode('utf-8'))
            print("selection3")
            print(selection3)
        elif selection2 == "ms":
            multiplier = 1 / seconds
            time = time * 0.001
            multiplier = float(multiplier)
            illuminate = time / multiplier
            illuminate = round(illuminate)
            print(illuminate)
            selected = str(illuminate)
            print("selection")
            print(illuminate)
            l5.config(text=selected)
            selection3 = 'P ' + str(selected) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection3.encode('utf-8'))
            print("selection3")
            print(selection3)
        elif selection2 == "s":
            multiplier = 1 / seconds
            time = time * 1
            multiplier = float(multiplier)
            illuminate = time / multiplier
            illuminate = round(illuminate)
            print(illuminate)
            selected = str(illuminate)
            print("selection")
            print(illuminate)
            l5.config(text=selected)
            selection3 = 'P ' + str(selected) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection3.encode('utf-8'))
            print("selection3")
            print(selection3)
    except ValueError:
        messagebox.showerror("Error", "Please enter a number")
    except (serial.SerialException, NameError):
        messagebox.showerror("Error", "Connect to an Arduino")


def devoptions():
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

    def frequencygenerator():
        global ser
        try:
            frequency = int(fb.get())
            if frequency == int(fb.get()):
                selection = 'F ' + str(frequency) + '\n\r'
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(selection.encode('utf-8'))
                print(selection)
        except ValueError:
            messagebox.showerror("Error", "Please enter an integer from 8000 to 4000000")
        except (serial.SerialException, NameError):
            messagebox.showerror("Error", "Connect to an Arduino")
        # except NameError:
        #    messagebox.showerror("Error", "Connect to an Arduino")

    devwindow = Toplevel()
    devwindow.title("Developer Options")
    devwindow.geometry()
    ib = Entry(devwindow, justify=LEFT)
    fb = Entry(devwindow, justify=LEFT)
    b1 = Button(devwindow, text='Send Number', command=burstgenerator, height=2, width=15)
    b9 = Button(devwindow, text='Send Number', command=frequencygenerator, height=2, width=15)
    b17 = Button(devwindow, text="Exit Dev Options", command=devwindow.destroy, height=2, width=15)
    l6 = Label(devwindow, text="Frequency")
    l7 = Label(devwindow, text="Pulses")
    b17.grid(row=5, column=5)
    l6.grid(row=0, column=0)
    fb.grid(row=1, column=0)
    b9.grid(row=2, column=0)
    l7.grid(row=0, column=1)
    ib.grid(row=1, column=1)
    b1.grid(row=2, column=1)


def mcs32location():
    global file_path
    file_path = fd.askopenfilename()
    print(file_path)


root = Tk()
root.geometry()
root.title("Thesis Interface V0.2")
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="MCS-32 Location", command=mcs32location)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

b5 = Button(root, text="Power On", command=poweron, height=2, width=15)
b6 = Button(root, text="Power Off", command=poweroff, height=2, width=15)
b7 = Button(root, text='MCS-32', command=run, height=2, width=15)

l1 = Label(root, text="OSL Interface v0.2", font="bold")
b2 = Button(root, text="Latch", command=latch, height=2, width=15)
b3 = Button(root, text="Start Countdown", command=start, height=2, width=15)
b4 = Button(root, text="Reset", command=resetting, height=2, width=15)
l3 = Label(root, text=arduino_ports[0])
b15 = Button(root, text="Connect", command=connect)
b16 = Button(root, text="Disconnect", command=disconnect)


pb = Entry(justify=LEFT)
freqcombo = ttk.Combobox(state="readonly", values=["kHz", "MHz"])
freqcombo.current(0)
b10 = Button(root, text="Frequency selection", command=frequencyselection, height=2, width=15)

tb = Entry(justify=LEFT)
lightcombo = ttk.Combobox(state="readonly", values=["ns", "us", "ms", "s"])
lightcombo.current(0)
b11 = Button(root, text="Time selection", command=timeselection, height=2, width=15)
l4 = Label(root, text="Your rounded pulse count is")
l5 = Label(root, text=illuminate)

db = Entry(justify=LEFT)
dwellcombo = ttk.Combobox(state="readonly", values=["ns", "us", "ms", "s"])
dwellcombo.current(0)
b12 = Button(root, text="Dwell selection", command=dwellselection, height=2, width=15)

b13 = Button(root, text="Reset Entry States", command=resetstate, height=2, width=15)
b14 = Button(root, text="Dev Options", command=devoptions, height=2, width=15)

b5.grid(row=2, column=0)
b6.grid(row=3, column=0)
b7.grid(row=4, column=0)

l1.grid(row=0, column=1, columnspan=2)
b2.grid(row=2, column=1)
b3.grid(row=3, column=1)
b4.grid(row=4, column=1)
l3.grid(row=14, column=1)
b15.grid(row=15, column=1)
b16.grid(row=16, column=1)


pb.grid(row=2, column=2)
freqcombo.grid(row=3, column=2)
b10.grid(row=4, column=2)

db.grid(row=5, column=2)
dwellcombo.grid(row=6, column=2)
b12.grid(row=7, column=2)

tb.grid(row=8, column=2)
lightcombo.grid(row=9, column=2)
b11.grid(row=10, column=2)
l4.grid(row=11, column=2)
l5.grid(row=12, column=2)

b13.grid(row=15, column=2)
b14.grid(row=15, column=3)
root.config(menu=menubar)
root.mainloop()

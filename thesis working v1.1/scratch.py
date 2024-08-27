#importing required packages
import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import time
import serial.tools.list_ports
import os
from tkinter import filedialog as fd
import math

#initializing and setting global variables
frequency = 0
illuminate = 0
binNumber = 0
dwelltime = 0
totaltime = 0
pos = ""
powerstatus = ""
global ser

#automatic connect function for Arduino. Finds and connects to an original Arduino plugged into the USB
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Arduino' in p.description
]
if not arduino_ports:
    messagebox.showerror("Error", "No Arduino Found")
    #raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    messagebox.showwarning("Warning", "Multiple Arduino found - using the first")
    #warnings.warn('Multiple Arduino found - using the first')

ports = serial.tools.list_ports.comports()
print(arduino_ports[0])
time.sleep(1)


def run():
    #function to define the file path of MCS-32.exe
    try:
        os.startfile(file_path)
    except NameError:
        messagebox.showerror("Error", "Please select the file path from the menu bar")
    except Exception:
        messagebox.showerror('Error', "System Cannot Find the File Specified")


def connect():
    #this function connects to Arduino and sets clickable buttons
    global ser
    try:
        ser = serial.Serial(arduino_ports[0])
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        lport.config(fg="green", font=("Arial", 12, "bold"))
        b3.config(state=tkinter.DISABLED)
        b10.config(state=tkinter.NORMAL)
        db.config(state=tkinter.NORMAL)
        b4.config(state=tkinter.NORMAL)
        b6.config(state=tkinter.NORMAL)
        b7.config(state=tkinter.NORMAL)
        bl8.config(state=tkinter.NORMAL)
        bl9.config(state=tkinter.NORMAL)
        pmtb.config(state=tkinter.NORMAL)
        pmtb2.config(state=tkinter.NORMAL)
        dwellcombo.config(state=tkinter.NORMAL)
        mb1.config(state=tkinter.NORMAL)
        mb2.config(state=tkinter.NORMAL)
        mb3.config(state=tkinter.NORMAL)
        mb4.config(state=tkinter.NORMAL)
        mb5.config(state=tkinter.NORMAL)
        mb6.config(state=tkinter.NORMAL)
        mb7.config(state=tkinter.NORMAL)
        mb8.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.NORMAL)
        mb10.config(state=tkinter.NORMAL)
        mb11.config(state=tkinter.NORMAL)
        IRpower.config(text="IR Power", fg="black", font=("Arial", 12, "bold"))
        BLpower.config(text="Blue Power", fg="black", font=("Arial", 12, "bold"))
        time.sleep(0.5)
       # started = ser.readline()
       # if started:
       #     connectindicator.config(fg="green", font=("Arial", 12, "bold"))
    except serial.SerialException:
        messagebox.showerror("Error", "Cannot connect, please restart")


def disconnect():
    #this function first resets, then disconnects the Arduino
    #and sets buttons as not clickable
    global ser
    try:
        if ser is not None and ser.is_open:
            resetting()
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.close()
            lport.config(fg="red", font=("Arial", 12, "bold"))
            b3.config(state=tkinter.NORMAL)
            b4.config(state=tkinter.DISABLED)
            b6.config(state=tkinter.DISABLED)
            b7.config(state=tkinter.DISABLED)
            plb.config(state=tkinter.DISABLED)
            b8.config(state=tkinter.DISABLED)
            bl8.config(state=tkinter.DISABLED)
            bl9.config(state=tkinter.DISABLED)
            delayb.config(state=tkinter.DISABLED)
            b9.config(state=tkinter.DISABLED)
            b10.config(state=tkinter.DISABLED)
            db.config(state=tkinter.DISABLED)
            dwellcombo.config(state=tkinter.DISABLED)
            tb.config(state=tkinter.DISABLED)
            lightcombo.config(state=tkinter.DISABLED)
            b11.config(state=tkinter.DISABLED)
            pmtb.config(state=tkinter.DISABLED)
            pmtb2.config(state=tkinter.DISABLED)
            mb1.config(state=tkinter.DISABLED)
            mb2.config(state=tkinter.DISABLED)
            mb3.config(state=tkinter.DISABLED)
            mb4.config(state=tkinter.DISABLED)
            mb5.config(state=tkinter.DISABLED)
            mb6.config(state=tkinter.DISABLED)
            mb7.config(state=tkinter.DISABLED)
            mb8.config(state=tkinter.DISABLED)
            mb9.config(state=tkinter.DISABLED)
            mb10.config(state=tkinter.DISABLED)
            mb11.config(state=tkinter.DISABLED)
            poslabel2.config(text="")
            IRpower.config(text="IR Power", fg="black", font=("Arial", 12, "bold"))
            BLpower.config(text="Blue Power", fg="black", font=("Arial", 12, "bold"))
            pmtpower.config(text="PMT Power", fg="black", font=("Arial", 12, "bold"))
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def poweron():
    #function to power the IR LED on. Enables IR pulses
    try:
        selection = 'IRPOWER\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        IRpower.config(text="IR Power On", fg="green", font=("Arial", 12, "bold"))
        b6.config(state=tkinter.DISABLED)
        b7.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def poweroff():
    # function to power the IR LED off. Disables IR pulses
    try:
        selection = 'IRPOWERO\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        IRpower.config(text="IR Power Off", fg="red", font=("Arial", 12, "bold"))
        b7.config(state=tkinter.DISABLED)
        b6.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def pmtenable():
    # function to enable the gate of the PMT
    try:
        selection = 'PMTEN\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        print(selection)
        time.sleep(2)
        pmtpower.config(text="PMT Enabled", fg="green", font=("Arial", 12, "bold"))
        pmtb.config(state=tkinter.DISABLED)
        pmtb2.config(state=tkinter.NORMAL)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def pmtdisable():
    #function to disable the gate of the PMT
    try:
        selection = 'PMTDIS\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pmtpower.config(text="PMT Disabled", fg="red", font=("Arial", 12, "bold"))
        pmtb2.config(state=tkinter.DISABLED)
        pmtb.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def bluepoweron():
    # function to power the Blue LED on. Enables Blue pulses
    try:
        selection = 'BLPOWER\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        BLpower.config(text="BL Power On", fg="green", font=("Arial", 12, "bold"))
        bl8.config(state=tkinter.DISABLED)
        bl9.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def bluepoweroff():
    # function to power the Blue LED off. Disables Blue pulses
    try:
        selection = 'BLPOWERO\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        BLpower.config(text="BL Power Off", fg="red", font=("Arial", 12, "bold"))
        bl9.config(state=tkinter.DISABLED)
        bl8.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def latch():
    #takes set variables and sends  them to the Arduino to arm 74f525 for counting
    try:
        global passlength
        global delaytime
        passlength = int(plb.get())
        delaytime = float(delayb.get())
        selection3 = dwellcombo.get()
        if illuminate != 0:
            selection = 'L ' + '\n\r'
            if selection3 == "ns":
                exptime = (((dwelltime * 1000000 / 250) + delaytime * 1000000) * passlength)
                exptime = int(exptime)
            if selection3 == "µs":
                exptime = (((dwelltime * 1000) + delaytime * 1000000) * passlength)
                exptime = int(exptime)
            print(exptime)
            nstous = exptime / 1000
            ustoms = nstous / 1000
            mstos = ustoms / 1000
            stomin = mstos / 60
            mintohour = stomin / 60
            stomin = float(stomin)
            mintohour = float(mintohour)
            #expnumber = str(exptime) + "ms, " + str(mstos) + "s, " + str(stomin) + "min, " + str(mintohour) + " hour"
            if 1 < exptime < 1000:
                expnumber = str(exptime) + "ms"
                lexperimentnumber.config(text=expnumber)
            if 1 < mstos < 119:
                mstos = format(mstos, '.2f')
                expnumber = str(mstos) + "s"
                lexperimentnumber.config(text=expnumber)
            if 1 < stomin < 119:
                stomin = format(stomin, '.2f')
                expnumber = str(stomin) + "min"
                lexperimentnumber.config(text=expnumber)
            if 1 < mintohour:
                mintohour = format(mintohour, '.2f')
                expnumber = str(mintohour) + " hour"
                lexperimentnumber.config(text=expnumber)
                #lexperimentnumber.config(text=expnumber)
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection.encode('utf-8'))
            print(selection)
        else:
            messagebox.showerror("Error", "No number to latch")
    except ValueError:
        messagebox.showerror("Error", "Enter both variables")
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def start():
    # sends a command to initiate the start experiment function of Arduino
    # also sets the delay time between acquisitions automatically
    passlength = int(plb.get())
    delaytime = int(delayb.get())
    try:
        if delaytime > 0.99:
            selection6 = 'START ' + str(passlength) + " " + str(delaytime) + '\n\r'
            print("passlength")
            print(passlength)
            print(str(passlength))
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection6.encode('utf-8'))
            print("selection6")
            print(selection6)
        else:
            messagebox.showerror("Error", "Minimum Delay is 1ms")
    except ValueError:
        messagebox.showerror("Error", "Please enter an integer number")
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def resetting():
    # resets the power status of LED's and PMT, stops experiment, resets arduino
    try:
        IRpower.config(text="IR Power", fg="black", font=("Arial", 12, "bold"))
        BLpower.config(text="Blue Power", fg="black", font=("Arial", 12, "bold"))
        pmtpower.config(text="PMT Power", fg="black", font=("Arial", 12, "bold"))
        poslabel2.config(text="")
        b7.config(state=tkinter.NORMAL)
        b6.config(state=tkinter.NORMAL)
        bl8.config(state=tkinter.NORMAL)
        bl9.config(state=tkinter.NORMAL)
        pmtb.config(state=tkinter.NORMAL)
        pmtb2.config(state=tkinter.NORMAL)
        mb1.config(state=tkinter.NORMAL)
        mb2.config(state=tkinter.NORMAL)
        mb3.config(state=tkinter.NORMAL)
        mb4.config(state=tkinter.NORMAL)
        mb5.config(state=tkinter.NORMAL)
        mb6.config(state=tkinter.NORMAL)
        mb7.config(state=tkinter.NORMAL)
        mb8.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.NORMAL)
        mb10.config(state=tkinter.NORMAL)
        mb11.config(state=tkinter.NORMAL)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.close()
        time.sleep(1)
        ser.open()
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def frequencyselection():
    # sets the dwelltime as the integer multiple of LED illumination pulses
    # sends this information to Arduino
    try:
        tb.config(state=tkinter.NORMAL)
        lightcombo.config(state=tkinter.NORMAL)
        b11.config(state=tkinter.NORMAL)
        global dwelltime
        dwelltime = float(db.get())
        selection3 = dwellcombo.get()
        if selection3 == "ns":
            if 124 < dwelltime < 125001:
                value = 0.000000001
                frequencydwell = 1 / (dwelltime * value)
                frequencydwell = round(frequencydwell, 6)
                frequencydwell = int(frequencydwell)
                seconds = frequencydwell
                selection4 = 'F ' + str(seconds) + '\n\r'
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(selection4.encode('utf-8'))
                print("selection4")
                print(selection4)
            else:
                messagebox.showerror("Error", "Dwell time should be between 125ns and 125µs")
        elif selection3 == "µs":
            if 0.249 < dwelltime < 126:
                value = 0.000001
                frequencydwell = 1 / (dwelltime * value)
                frequencydwell = round(frequencydwell, 6)
                frequencydwell = int(frequencydwell)
                seconds = frequencydwell
                selection4 = 'F ' + str(seconds) + '\n\r'
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(selection4.encode('utf-8'))
                print("selection4")
                print(selection4)
            else:
                messagebox.showerror("Error", "Dwell time should be between 250ns and 125µs")
    except ValueError:
        messagebox.showerror("Error", "Please enter a number")
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")


def timeselection():
    # calculates the amount of pulses 74f525 will count down from
    # using the dwell time and selection boxes
    try:
        plb.config(state=tkinter.NORMAL)
        b8.config(state=tkinter.NORMAL)
        b9.config(state=tkinter.NORMAL)
        delayb.config(state=tkinter.NORMAL)
        global illuminate
        global multiplier
        global selected
        global bins
        selection2 = lightcombo.get()
        time = float(tb.get())
        binmultiplier = float(db.get())
        if selection2 == "ns":
            if time < 1000:
                multiplier = 1 / 4000000
                time = time * 0.000000001
                multiplier = float(multiplier)
                illuminate = time / multiplier
                illuminate = round(illuminate)
                selected = str(illuminate)
                binmultiplier = binmultiplier / 250
                bins = illuminate * 10 / binmultiplier
                bins = math.ceil(bins)
                l9.config(text=bins)
                print("bins")
                print(bins)
                l6.config(text=selected)
                selection3 = 'P ' + str(selected) + '\n\r'
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(selection3.encode('utf-8'))
                print("selection3")
                print(selection3)
            else:
                messagebox.showwarning("Warning", "Please choose µs")
        elif selection2 == "µs":
            if time < 1000:
                multiplier = 1 / 4000000
                time = time * 0.000001
                multiplier = float(multiplier)
                illuminate = time / multiplier
                illuminate = round(illuminate)
                selected = str(illuminate)
                bins = illuminate * 10 / binmultiplier
                bins = math.ceil(bins)
                l9.config(text=bins)
                l6.config(text=selected)
                selection3 = 'P ' + str(selected) + '\n\r'
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(selection3.encode('utf-8'))
                print(selection3)
            else:
                messagebox.showwarning("Warning", "Please choose ms")
        elif selection2 == "ms":
            if time < 8.193:
                multiplier = 1 / 4000000
                time = time * 0.001
                multiplier = float(multiplier)
                illuminate = time / multiplier
                illuminate = round(illuminate)
                print(illuminate)
                selected = str(illuminate)
                bins = illuminate * 10 / binmultiplier
                bins = math.ceil(bins)
                l9.config(text=bins)
                print("selection")
                print(illuminate)
                l6.config(text=selected)
                selection3 = 'P ' + str(selected) + '\n\r'
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(selection3.encode('utf-8'))
                print("selection3")
                print(selection3)
            else:
                messagebox.showwarning("Warning", "Cannot provide more than 32768 pulses")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")
    except NameError:
        messagebox.showerror("Error", "Please enter a number in Frequency or Dwell")
    except ValueError:
        messagebox.showerror("Error", "Please enter a number")


def devoptions():
    #developer options, allows for sending raw numbers of pulses and frequency
    #allows for resetting the entry boxes
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

    def resetstate():
        db.config(state=tkinter.NORMAL)
        db.delete(0, END)
        tb.delete(0, END)
        fb.delete(0, END)
        ib.delete(0, END)
        plb.delete(0, END)

    ##tkinter's main dropdown menu selections and developer options window
    devwindow = Toplevel()
    devwindow.iconbitmap("myIcon.ico")
    devwindow.title("Developer Options")
    devwindow.geometry()
    ib = Entry(devwindow, justify=LEFT)
    fb = Entry(devwindow, justify=LEFT)
    b1 = Button(devwindow, text='Send Burst Number', command=burstgenerator, width=17)
    b9 = Button(devwindow, text='Send Frequency', command=frequencygenerator, width=17)
    b17 = Button(devwindow, text="Exit Dev Options", command=devwindow.destroy, width=17)
    l6 = Label(devwindow, text="Frequency")
    l7 = Label(devwindow, text="Pulses")
    b13 = Button(devwindow, text="Reset Entry States", command=resetstate, width=17)
    l6.grid(row=0, column=2)
    fb.grid(row=1, column=2)
    b9.grid(row=2, column=2)
    b13.grid(row=3, column=2)
    l7.grid(row=0, column=3)
    ib.grid(row=1, column=3)
    b1.grid(row=2, column=3)
    b17.grid(row=3, column=3)

    Label(devwindow, text="Tips", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
    guidelines = [
        "Send frequency directly sends it to Arduino without limitations",
        "Send Burst Number directly sends the number of light pulses",
        'Reset Entry States resets all the boxes in the interface',
    ]
    for i, guideline in enumerate(guidelines, start=1):
        Label(devwindow, text=f"{i}. {guideline}", font=("Arial", 9), justify="left").grid(row=i, column=0, padx=10, sticky="w")


def mcs32location():
    #file path function for the file dropdown menu
    global file_path
    file_path = fd.askopenfilename()
    print(file_path)


def aboutmenu():
    #an about part of the software, accessible from help->about
    aboutwindow = Toplevel()
    aboutwindow.iconbitmap("myIcon.ico")
    aboutwindow.title("Developer Options")
    aboutwindow.geometry()
    authorlabel = Label(aboutwindow, text="Author")
    namelabel = Label(aboutwindow, text="Deniz Boztemur")
    datelabel = Label(aboutwindow, text="2024")
    maillabel = Label(aboutwindow, text="dboz@metu.edu.tr")
    infolabel = Label(aboutwindow, text="Thesis work in TOSL Lab")
    infolabel2 = Label(aboutwindow, text="Supervised by Enver Bulur")
    authorlabel.grid(row=0, column=0)
    namelabel.grid(row=1, column=0)
    datelabel.grid(row=2, column=0)
    maillabel.grid(row=3, column=0)
    infolabel.grid(row=4, column=0)
    infolabel2.grid(row=5, column=0)


def rotaryhome():
    #homes the rotary stage
    #sets all positions available
    try:
        mb1.config(state=tkinter.NORMAL)
        mb2.config(state=tkinter.NORMAL)
        mb3.config(state=tkinter.NORMAL)
        mb4.config(state=tkinter.NORMAL)
        mb5.config(state=tkinter.NORMAL)
        mb6.config(state=tkinter.NORMAL)
        mb7.config(state=tkinter.NORMAL)
        mb8.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.DISABLED)
        selection = 'HOME\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Rotary Home"
        poslabel2.config(text=pos)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def sampleone():
    #sets the rotary stage to sample one
    #sample one button is disabled
    try:
        mb1.config(state=tkinter.DISABLED)
        mb2.config(state=tkinter.NORMAL)
        mb3.config(state=tkinter.NORMAL)
        mb4.config(state=tkinter.NORMAL)
        mb5.config(state=tkinter.NORMAL)
        mb6.config(state=tkinter.NORMAL)
        mb7.config(state=tkinter.NORMAL)
        mb8.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.NORMAL)
        selection = 'ONE\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Sample One"
        poslabel2.config(text=pos)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def sampletwo():
    # sets the rotary stage to sample two
    # sample two button is disabled
    try:
        mb2.config(state=tkinter.DISABLED)
        mb1.config(state=tkinter.NORMAL)
        mb3.config(state=tkinter.NORMAL)
        mb4.config(state=tkinter.NORMAL)
        mb5.config(state=tkinter.NORMAL)
        mb6.config(state=tkinter.NORMAL)
        mb7.config(state=tkinter.NORMAL)
        mb8.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.NORMAL)
        selection = 'TWO\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Sample Two"
        poslabel2.config(text=pos)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def samplethree():
    # sets the rotary stage to sample three
    # sample three button is disabled
    try:
        mb3.config(state=tkinter.DISABLED)
        mb1.config(state=tkinter.NORMAL)
        mb2.config(state=tkinter.NORMAL)
        mb4.config(state=tkinter.NORMAL)
        mb5.config(state=tkinter.NORMAL)
        mb6.config(state=tkinter.NORMAL)
        mb7.config(state=tkinter.NORMAL)
        mb8.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.NORMAL)
        selection = 'THREE\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Sample Three"
        poslabel2.config(text=pos)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def samplefour():
    # sets the rotary stage to sample four
    # sample four button is disabled
    try:
        mb4.config(state=tkinter.DISABLED)
        mb1.config(state=tkinter.NORMAL)
        mb2.config(state=tkinter.NORMAL)
        mb3.config(state=tkinter.NORMAL)
        mb5.config(state=tkinter.NORMAL)
        mb6.config(state=tkinter.NORMAL)
        mb7.config(state=tkinter.NORMAL)
        mb8.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.NORMAL)
        selection = 'FOUR\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Sample Four"
        poslabel2.config(text=pos)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def samplefive():
    # sets the rotary stage to sample five
    # sample five button is disabled
    try:
        mb5.config(state=tkinter.DISABLED)
        mb1.config(state=tkinter.NORMAL)
        mb2.config(state=tkinter.NORMAL)
        mb3.config(state=tkinter.NORMAL)
        mb4.config(state=tkinter.NORMAL)
        mb6.config(state=tkinter.NORMAL)
        mb7.config(state=tkinter.NORMAL)
        mb8.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.NORMAL)
        selection = 'FIVE\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Sample Five"
        poslabel2.config(text=pos)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def samplesix():
    # sets the rotary stage to sample six
    # sample six button is disabled
    try:
        mb6.config(state=tkinter.DISABLED)
        mb1.config(state=tkinter.NORMAL)
        mb2.config(state=tkinter.NORMAL)
        mb3.config(state=tkinter.NORMAL)
        mb4.config(state=tkinter.NORMAL)
        mb5.config(state=tkinter.NORMAL)
        mb7.config(state=tkinter.NORMAL)
        mb8.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.NORMAL)
        selection = 'SIX\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Sample Six"
        poslabel2.config(text=pos)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def sampleseven():
    # sets the rotary stage to sample seven
    # sample seven button is disabled
    try:
        mb7.config(state=tkinter.DISABLED)
        mb1.config(state=tkinter.NORMAL)
        mb2.config(state=tkinter.NORMAL)
        mb3.config(state=tkinter.NORMAL)
        mb4.config(state=tkinter.NORMAL)
        mb5.config(state=tkinter.NORMAL)
        mb6.config(state=tkinter.NORMAL)
        mb8.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.NORMAL)
        selection = 'SEVEN\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Sample Seven"
        poslabel2.config(text=pos)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def sampleeight():
    # sets the rotary stage to sample eight
    # sample eight button is disabled
    try:
        mb8.config(state=tkinter.DISABLED)
        mb1.config(state=tkinter.NORMAL)
        mb2.config(state=tkinter.NORMAL)
        mb3.config(state=tkinter.NORMAL)
        mb4.config(state=tkinter.NORMAL)
        mb5.config(state=tkinter.NORMAL)
        mb6.config(state=tkinter.NORMAL)
        mb7.config(state=tkinter.NORMAL)
        mb9.config(state=tkinter.NORMAL)
        selection = 'EIGHT\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Sample Eight"
        poslabel2.config(text=pos)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def linearhome():
    # sets the linear stage to its home position
    # disables the home button
    try:
        selection = 'LHOME\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Linear Home"
        poslabel2.config(text=pos)
        print(selection)
        mb11.config(state=tkinter.DISABLED)
        mb10.config(state=tkinter.NORMAL)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def lineareject():
    #ejects the linear tray for sample loading
    #disables the eject button
    try:
        selection = 'EJECT\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pos = "Tray Ejected"
        poslabel2.config(text=pos)
        mb10.config(state=tkinter.DISABLED)
        mb11.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


#from now on, tkinter
#creates menu bar, menus, several frames, creates buttons, entryboxes and drop-down menus
#then places them accordingly into the frames
#creates two tabs, places frames into one and guidelines into the other
root = Tk()
root.iconbitmap("myIcon.ico")
root.geometry()
root.title("TR-OSL Interface v1.0.1")
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Guidelines')
tabControl.add(tab2, text='Control')
tabControl.grid(row=0, column=0)

defaultbg = root.cget('bg')
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
helpmenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="MCS-32 Location", command=mcs32location)
filemenu.add_separator()
filemenu.add_command(label="Developer Options", command=devoptions)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
helpmenu.add_command(label="About", command=aboutmenu)
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Help", menu=helpmenu)

infoframe = Frame(tab1, borderwidth=5, relief="sunken")
softwareframe = LabelFrame(tab2, text="MCS-32 Software", font=("Arial", 9, "bold"))
connection_frame = LabelFrame(tab2, text="Arduino Connection", font=("Arial", 9, "bold"))
ledframe = LabelFrame(tab2, text="Light Source Driver", font=("Arial", 9, "bold"))
dataframe = LabelFrame(tab2, text="Experiment Start", font=("Arial", 9, "bold"))
selectionframe = LabelFrame(tab2, text="Parameter Selection", font=("Arial", 9, "bold"))
movementframe = LabelFrame(tab2, text="Movement Control", font=("Arial", 9, "bold"))

infoframe.grid(row=1, column=0, rowspan=10, padx=10, pady=10, sticky="nsew")
softwareframe.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
connection_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
ledframe.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
dataframe.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")
selectionframe.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")
movementframe.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

mb1 = Button(movementframe, text="One", command=sampleone, height=2, width=5, font="Arial")
mb2 = Button(movementframe, text="Two", command=sampletwo, height=2, width=5, font="Arial")
mb3 = Button(movementframe, text="Three", command=samplethree, height=2, width=5, font="Arial")
mb4 = Button(movementframe, text="Four", command=samplefour, height=2, width=5, font="Arial")
mb5 = Button(movementframe, text="Five", command=samplefive, height=2, width=5, font="Arial")
mb6 = Button(movementframe, text="Six", command=samplesix, height=2, width=5, font="Arial")
mb7 = Button(movementframe, text="Seven", command=sampleseven, height=2, width=5, font="Arial")
mb8 = Button(movementframe, text="Eight", command=sampleeight, height=2, width=5, font="Arial")
mb9 = Button(movementframe, text="Home", command=rotaryhome, height=2, width=5, font="Arial")
mb10 = Button(movementframe, text="Eject Tray", command=lineareject, height=2, width=15, font="Arial")
mb11 = Button(movementframe, text="Load Tray", command=linearhome, height=2, width=15, font="Arial")
poslabel = Label(movementframe, text="Tray Position", font=("Arial", 12, "bold"))
poslabel2 = Label(movementframe, text=pos, font=("Arial", 12, "bold"))
mb1.grid(row=0, column=0)
mb2.grid(row=0, column=1)
mb3.grid(row=0, column=2)
mb4.grid(row=1, column=0)
mb5.grid(row=1, column=1)
mb6.grid(row=1, column=2)
mb7.grid(row=2, column=0)
mb8.grid(row=2, column=1)
mb9.grid(row=2, column=2)
mb10.grid(row=0, column=3)
mb11.grid(row=1, column=3)
poslabel.grid(row=2, column=3)
poslabel2.grid(row=3, column=3)
mb1.config(state=tkinter.DISABLED)
mb2.config(state=tkinter.DISABLED)
mb3.config(state=tkinter.DISABLED)
mb4.config(state=tkinter.DISABLED)
mb5.config(state=tkinter.DISABLED)
mb6.config(state=tkinter.DISABLED)
mb7.config(state=tkinter.DISABLED)
mb8.config(state=tkinter.DISABLED)
mb9.config(state=tkinter.DISABLED)
mb10.config(state=tkinter.DISABLED)
mb11.config(state=tkinter.DISABLED)

b1 = Button(softwareframe, text='Run MCS-32', command=run, height=2, width=15, font="Arial")
b1.grid(row=0, column=0, sticky="NEWS")

lport = Label(connection_frame, text=arduino_ports[0], font=("Arial", 12, "bold"))
b3 = Button(connection_frame, text="Connect", command=connect, height=2, width=15, font="Arial")
b4 = Button(connection_frame, text="Disconnect", command=disconnect, height=2, width=15, font="Arial")
b5 = Button(connection_frame, text="Reset Arduino", command=resetting, height=2, width=15, font="Arial")
lport.grid(row=0, column=0)
b3.grid(row=1, column=0)
b4.grid(row=2, column=0)
b5.grid(row=3, column=0)

IRpower = Label(ledframe, text="IR Power", font=("Arial", 12, "bold"))
BLpower = Label(ledframe, text="Blue Power", font=("Arial", 12, "bold"))
b6 = Button(ledframe, text="Power On", command=poweron, height=2, width=15, font="Arial")
b7 = Button(ledframe, text="Power Off", command=poweroff, height=2, width=15, font="Arial")
bl8 = Button(ledframe, text="Power On", command=bluepoweron, height=2, width=15, font="Arial")
bl9 = Button(ledframe, text="Power Off", command=bluepoweroff, height=2, width=15, font="Arial")
pmtb = Button(ledframe, text="PMT Enable", command=pmtenable, height=2, width=15, font="Arial")
pmtb2 = Button(ledframe, text="PMT Disable", command=pmtdisable, height=2, width=15, font="Arial")
pmtpower = Label(ledframe, text="PMT", font=("Arial", 12, "bold"))
IRpower.grid(row=0, column=0)
BLpower.grid(row=0, column=1)
b6.grid(row=1, column=0)
b7.grid(row=2, column=0)
bl8.grid(row=1, column=1)
bl9.grid(row=2, column=1)
pmtpower.grid(row=0, column=2)
pmtb.grid(row=1, column=2)
pmtb2.grid(row=2, column=2)
pmtb.config(state=tkinter.DISABLED)
pmtb2.config(state=tkinter.DISABLED)
b6.config(state=tkinter.DISABLED)
b7.config(state=tkinter.DISABLED)
bl8.config(state=tkinter.DISABLED)
bl9.config(state=tkinter.DISABLED)

l3 = Label(dataframe, text="Acquisition Count", font=("Arial", 12, "bold"))
ldelay = Label(dataframe, text="Single Acquisition Time (ms)", font=("Arial", 12, "bold"))
b8 = Button(dataframe, text="Arm Experiment", command=latch, height=2, width=15, font=("Arial", 12, "bold"))
plb = Entry(dataframe, justify=LEFT, width=23)
delayb = Entry(dataframe, justify=LEFT, width=23)
b9 = Button(dataframe, text="Start Experiment", command=start, height=2, width=15, font=("Arial", 12, "bold"))
image = PhotoImage(file="tosl.png")
label = Label(dataframe, image=image)
l3.grid(row=0, column=0)
plb.grid(row=1, column=0)
ldelay.grid(row=2, column=0)
delayb.grid(row=3, column=0)
b8.grid(row=4, column=0)
b9.grid(row=5, column=0)
label.grid(row=0, column=1, rowspan=4)
delayb.config(state=tkinter.DISABLED)
plb.config(state=tkinter.DISABLED)
b8.config(state=tkinter.DISABLED)
b9.config(state=tkinter.DISABLED)

l3 = Label(selectionframe, text="Dwell Time", font=("Arial", 12, "bold"))
db = Entry(selectionframe, justify=LEFT, width=33)
dwellcombo = ttk.Combobox(selectionframe, state="readonly", values=["ns", "µs"], font=("Arial", 12, "bold"))
dwellcombo.current(0)
b10 = Button(selectionframe, text="Confirm Dwell Time", command=frequencyselection, height=1, width=22, font=("Arial", 12, "bold"))
l4 = Label(selectionframe, text="Illumination Duration", font=("Arial", 12, "bold"))
tb = Entry(selectionframe, justify=LEFT, width=33)
lightcombo = ttk.Combobox(selectionframe, state="readonly", values=["ns", "µs", "ms"], font=("Arial", 12, "bold"))
lightcombo.current(0)
b11 = Button(selectionframe, text="Confirm Illumination Duration", command=timeselection, height=1, width=22, font=("Arial", 12, "bold"))

l8 = Label(selectionframe, text="Suggested Data Points", font=("Arial", 12, "bold"))
l9 = Label(selectionframe, text=binNumber, font=("Arial", 12, "bold"))
l5 = Label(selectionframe, text="Light Pulse Count", font=("Arial", 12, "bold"))
l6 = Label(selectionframe, text=illuminate, font=("Arial", 12, "bold"))
lexperiment = Label(selectionframe, text="Total Approximate Experiment Time", font=("Arial", 12, "bold"))
lexperimentnumber = Label(selectionframe, text=totaltime, font=("Arial", 12, "bold"))
l3.grid(row=0, column=0)
db.grid(row=1, column=0)
dwellcombo.grid(row=2, column=0)
b10.grid(row=3, column=0)
l4.grid(row=4, column=0)
tb.grid(row=5, column=0)
lightcombo.grid(row=6, column=0)
b11.grid(row=7, column=0)

l8.grid(row=1, column=1)
l9.grid(row=2, column=1)
lexperiment.grid(row=5, column=1)
lexperimentnumber.grid(row=6, column=1)

l5.grid(row=3, column=1)
l6.grid(row=4, column=1)
b10.config(state=tkinter.DISABLED)
db.config(state=tkinter.DISABLED)
dwellcombo.config(state=tkinter.DISABLED)
tb.config(state=tkinter.DISABLED)
lightcombo.config(state=tkinter.DISABLED)
b11.config(state=tkinter.DISABLED)

Label(infoframe, text="Guidelines", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
guidelines = [
    "Make sure both MCS-32 and Arduino are both installed and connected.",
    "From the File drop down menu, choose the location of MCS-32.exe.",
    'Click on "Run MCS-32" Button to start the software.',
    'From the MCS-32 software file menu go to Acquire->Input Control and select 50ohm',
    'Click "Connect" in the Arduino Connection frame to connect to Arduino.',
    'Click "Power On" to enable the illumination driver, according to the LED you will be using',
    'Enable the PMT using the "PMT Enable" button.',
    'Write the desired dwell time for the DAQ',
    'Choose appropriate order of magnitude from the drop-down menu',
    'Dwell Time values are limited between 125ns and 125µs',
    'Confirm Dwell Time',
    'Enter the amount of time desired for light pulses.',
    'Choose appropriate order of magnitude from the drop-down menu',
    'Illumination Duration is limited between 250ns and 8.192ms',
    'Confirm Illumination Duration',
    'From the list at the right-hand side, confirm the suggested data points and light pulse count',
    'From the MCS-32 software, it is suggested you set the "Pass Length" parameter to the suggested value',
    'Enter how many times the experiment will be repeated in "Acquisition Count".',
    'Enter the duration of a single run in total.',
    'For example, for a 1ms illumination, a minimum of 10ms is required',
]

guidelines2 = [
    'Click Arm Experiment to arm the experiment.',
    'From the list at the right-hand side, confirm the duration the experiment will take',
    'Make sure you click on the "Start" Radiobutton in the software to Arm MCS-32',
    'Clicking "Experiment" will begin the experiment.'
]
for i, guideline in enumerate(guidelines, start=1):
    Label(infoframe, text=f"{i}. {guideline}", font=("Arial", 9), justify="left").grid(row=i, column=0, padx=10, sticky="w")
for i, guideline in enumerate(guidelines2, start=21):
    Label(infoframe, text=f"{i}. {guideline}", font=("Arial", 9), justify="left").grid(row=i - 20, column=1, padx=10, sticky="w")
#main loop for the interface
root.config(menu=menubar)
root.mainloop()

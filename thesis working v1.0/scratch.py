import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import time
import serial.tools.list_ports
import warnings
import os
from tkinter import filedialog as fd
import math

frequency = 0
illuminate = 0
dwelltimeshow = 0
binNumber = 0
totaltime = 0
powerstatus = ""
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


def run():
    #function to define the file path of MCS-32.exe
    #
    try:
        os.startfile(file_path)
    except NameError:
        messagebox.showerror("Error", "Please select the file path from the menu bar")
    except Exception:
        messagebox.showerror('Error', "System Cannot Find the File Specified")


def connect():
    #this function connects to Arduino and allows buttons to be clicked
    #
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
    except serial.SerialException:
        messagebox.showerror("Error", "Cannot connect, please restart")


def disconnect():
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
            b9.config(state=tkinter.DISABLED)
            b10.config(state=tkinter.DISABLED)
            db.config(state=tkinter.DISABLED)
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
            IRpower.config(text="IR Power", fg="black", font=("Arial", 12, "bold"))
            BLpower.config(text="Blue Power", fg="black", font=("Arial", 12, "bold"))
            pmtpower.config(text="PMT Power", fg="black", font=("Arial", 12, "bold"))
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def poweron():
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
    try:
        global passlength
        global delaytime
        passlength = int(plb.get())
        delaytime = bins * illuminate
        if illuminate != 0:
            selection = 'L ' + '\n\r'
            print("dwelltimeshow")
            print(dwelltimeshow)
            print("illuminate")
            print(illuminate)
            print("delaytime")
            print(delaytime)
            print("passlength")
            print(passlength)
            exptime = ((dwelltimeshow * illuminate) + delaytime) * passlength / 200
            exptime = int(exptime)
            mstos = exptime / 1000
            stomin = mstos / 60
            mintohour = stomin / 60
            stomin = int(stomin)
            mintohour = int(mintohour)
            expnumber = str(exptime) + "ms, " + str(mstos) + "s, " + str(stomin) + "min, " + str(mintohour) + " hour"
            lexperimentnumber.config(text=expnumber)
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection.encode('utf-8'))
            print(selection)
        else:
            messagebox.showerror("Error", "No number to latch")
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def start():
    try:
        global delaytime
        if delaytime < 999:
            delaytime = 1000
            selection6 = 'START ' + str(passlength) + " " + str(delaytime) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection6.encode('utf-8'))
            print("selection6")
            print(selection6)
        elif delaytime > 3000:
            delaytime = 1000
            selection6 = 'START ' + str(passlength) + " " + str(delaytime) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection6.encode('utf-8'))
            print("selection6")
            print(selection6)
        else:
            selection6 = 'START ' + str(passlength) + " " + str(delaytime) + '\n\r'
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(selection6.encode('utf-8'))
            print("selection6")
            print(selection6)
    except ValueError:
        messagebox.showerror("Error", "Please enter an integer number")
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def resetting():
    try:
        IRpower.config(text="IR Power", fg="black", font=("Arial", 12, "bold"))
        BLpower.config(text="Blue Power", fg="black", font=("Arial", 12, "bold"))
        pmtpower.config(text="PMT Power", fg="black", font=("Arial", 12, "bold"))
        b7.config(state=tkinter.NORMAL)
        b6.config(state=tkinter.NORMAL)
        bl8.config(state=tkinter.NORMAL)
        bl9.config(state=tkinter.NORMAL)
        pmtb.config(state=tkinter.NORMAL)
        pmtb2.config(state=tkinter.NORMAL)
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
    try:
        tb.config(state=tkinter.NORMAL)
        lightcombo.config(state=tkinter.NORMAL)
        b11.config(state=tkinter.NORMAL)
        global dwelltime
        global dwelltimeshow
        multiple = 1 / float(db.get())
        print(multiple)
        dwelltimeshow = 250 / multiple
        dwelltimeshow = int(dwelltimeshow)
        selected = (str(dwelltimeshow) + "ns")
        l7.config(text=selected)
        dwelltime = multiple * 4000000
        dwelltime = int(dwelltime)
        selection4 = 'F ' + str(dwelltime) + '\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection4.encode('utf-8'))
        print("selection4")
        print(selection4)
    except ValueError:
        messagebox.showerror("Error", "Please enter a number")
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")


def timeselection():
    try:
        plb.config(state=tkinter.NORMAL)
        b8.config(state=tkinter.NORMAL)
        b9.config(state=tkinter.NORMAL)
        global illuminate
        global multiplier
        global selected
        global bins
        selection2 = lightcombo.get()
        time = float(tb.get())
        binmultiplier = float(db.get())
        if selection2 == "ns":
            if time < 999:
                multiplier = 1 / 4000000
                time = time * 0.000000001
                multiplier = float(multiplier)
                illuminate = time / multiplier
                illuminate = round(illuminate)
                selected = str(illuminate)
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
            if time < 999:
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
            if time < 999:
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
                messagebox.showwarning("Warning", "Please choose s")
        elif selection2 == "s":
            multiplier = 1 / 4000000
            time = time * 1
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
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")
    except NameError:
        messagebox.showerror("Error", "Please enter a number in Frequency or Dwell")
    except ValueError:
        messagebox.showerror("Error", "Please enter a number")


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

    def resetstate():
        db.config(state=tkinter.NORMAL)
        db.delete(0, END)
        tb.delete(0, END)
        fb.delete(0, END)
        ib.delete(0, END)
        plb.delete(0, END)

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
    global file_path
    file_path = fd.askopenfilename()
    print(file_path)


def aboutmenu():
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
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def sampleone():
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
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def sampletwo():
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
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def samplethree():
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
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def samplefour():
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
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def samplefive():
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
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def samplesix():
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
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def sampleseven():
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
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def sampleeight():
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
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def linearhome():
    try:
        selection = 'LHOME\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        print(selection)
        mb11.config(state=tkinter.DISABLED)
        mb10.config(state=tkinter.NORMAL)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def lineareject():
    try:
        selection = 'EJECT\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        mb10.config(state=tkinter.DISABLED)
        mb11.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


root = Tk()
root.iconbitmap("myIcon.ico")
root.geometry()
root.title("TR-OSL Interface v0.8")
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

l3 = Label(dataframe, text="Acquisition Count", font="Arial")
b8 = Button(dataframe, text="Arm Experiment", command=latch, height=2, width=15, font="Arial")
plb = Entry(dataframe, justify=LEFT, width=23)
b9 = Button(dataframe, text="Start Experiment", command=start, height=2, width=15, font="Arial")
image = PhotoImage(file="tosl.png")
label = Label(dataframe, image=image)
l3.grid(row=0, column=0)
plb.grid(row=1, column=0)
b8.grid(row=2, column=0)
b9.grid(row=3, column=0)
label.grid(row=0, column=1, rowspan=4)
plb.config(state=tkinter.DISABLED)
b8.config(state=tkinter.DISABLED)
b9.config(state=tkinter.DISABLED)

l3 = Label(selectionframe, text="Dwell Time", font="Arial")
db = Entry(selectionframe, justify=LEFT, width=33)
b10 = Button(selectionframe, text="Confirm Dwell Time", command=frequencyselection, height=1, width=22, font="Arial")
l4 = Label(selectionframe, text="Illumination Duration", font="Arial")
tb = Entry(selectionframe, justify=LEFT, width=33)
lightcombo = ttk.Combobox(selectionframe, state="readonly", values=["ns", "µs", "ms", "s"], font="Arial")
lightcombo.current(0)
b11 = Button(selectionframe, text="Confirm Illumination Duration", command=timeselection, height=1, width=22, font="Arial")

l2 = Label(selectionframe, text="MCS-32 Dwell Time", font=("Arial", 12, "bold"))
l7 = Label(selectionframe, text=dwelltimeshow, font=("Arial", 12, "bold"))
l8 = Label(selectionframe, text="Pass Length", font=("Arial", 12, "bold"))
l9 = Label(selectionframe, text=binNumber, font=("Arial", 12, "bold"))
l5 = Label(selectionframe, text="Light Pulse Count", font=("Arial", 12, "bold"))
l6 = Label(selectionframe, text=illuminate, font=("Arial", 12, "bold"))
lexperiment = Label(selectionframe, text="Total Approximate Experiment Time", font=("Arial", 12, "bold"))
lexperimentnumber = Label(selectionframe, text=totaltime, font=("Arial", 12, "bold"))
l3.grid(row=0, column=0)
db.grid(row=1, column=0)
b10.grid(row=2, column=0)
l4.grid(row=3, column=0)
tb.grid(row=4, column=0)
lightcombo.grid(row=5, column=0)
b11.grid(row=6, column=0)

l2.grid(row=0, column=1)
l7.grid(row=1, column=1)
l8.grid(row=2, column=1)
l9.grid(row=3, column=1)
lexperiment.grid(row=6, column=1)
lexperimentnumber.grid(row=7, column=1)

l5.grid(row=4, column=1)
l6.grid(row=5, column=1)
b10.config(state=tkinter.DISABLED)
db.config(state=tkinter.DISABLED)

tb.config(state=tkinter.DISABLED)
lightcombo.config(state=tkinter.DISABLED)
b11.config(state=tkinter.DISABLED)

Label(infoframe, text="Guidelines", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
guidelines = [
    "Make sure both MCS-32 and Arduino are both installed and connected.",
    "From the File drop down menu, choose the location of MCS-32.exe.",
    'Click on "Run MCS-32" Button to start the software.',
    'Make sure you click on the "Start" Radiobutton in the software to Arm MCS-32',
    'Click "Connect" in the Arduino Connection frame to connect to Arduino.',
    'Click "Power On" to power up the light source driver.',
    'Enter either desired frequency or desired bin width to the boxes in "Parameter Selection".',
    'Choose appropriate order of magnitude from drop down menus under the boxes.',
    'Either click "Frequency Selection" or "Dwell Selection" to set up the system.',
    'Enter the amount of time desired for light pulses. Choose appropriate order of magnitude.',
    'Click "Time Selection" to set the system. This will show you the number of pulses at the right of the button.',
    'Enter how many times the experiment will be repeated in "Pass Count".',
    'Click Latch to arm the experiment.',
    'Clicking "Start Countdown" will begin the experiment.'
]
for i, guideline in enumerate(guidelines, start=1):
    Label(infoframe, text=f"{i}. {guideline}", font=("Arial", 9), justify="left").grid(row=i, column=0, padx=10, sticky="w")

root.config(menu=menubar)
root.mainloop()

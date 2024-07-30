import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import time
import serial.tools.list_ports
import warnings
import os
from tkinter import filedialog as fd

frequency = 0
illuminate = 0
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
    try:
        os.startfile(file_path)
    except NameError:
        messagebox.showerror("Error", "Please select the file path from the menu bar")
    except Exception:
        messagebox.showerror('Error', "System Cannot Find the File Specified")


def connect():
    global ser
    try:
        ser = serial.Serial(arduino_ports[0])
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        lport.config(fg="green", font=("Arial", 12, "bold"))
        b3.config(state=tkinter.NORMAL)
        pb.config(state=tkinter.NORMAL)
        freqcombo.config(state=tkinter.NORMAL)
        b10.config(state=tkinter.NORMAL)
        db.config(state=tkinter.NORMAL)
        dwellcombo.config(state=tkinter.NORMAL)
        b12.config(state=tkinter.NORMAL)
        b4.config(state=tkinter.NORMAL)
        b6.config(state=tkinter.NORMAL)
        b7.config(state=tkinter.NORMAL)
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
        time.sleep(0.5)
    except serial.SerialException:
        messagebox.showerror("Error", "Cannot connect, please restart")


def disconnect():
    global ser
    try:
        if ser is not None and ser.is_open:
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
            b9.config(state=tkinter.DISABLED)
            pb.config(state=tkinter.DISABLED)
            freqcombo.config(state=tkinter.DISABLED)
            b10.config(state=tkinter.DISABLED)
            db.config(state=tkinter.DISABLED)
            dwellcombo.config(state=tkinter.DISABLED)
            b12.config(state=tkinter.DISABLED)
            tb.config(state=tkinter.DISABLED)
            lightcombo.config(state=tkinter.DISABLED)
            b11.config(state=tkinter.DISABLED)
            lpower.config(text="Power", fg="black", font=("Arial", 12, "bold"))
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def poweron():
    try:
        selection = 'POWERON\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        lpower.config(text="Power On", fg="green", font=("Arial", 12, "bold"))
        b6.config(state=tkinter.DISABLED)
        b7.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def pmtpoweron():
    try:
        selection = 'PPOWERON\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pmtpower.config(text="PMT Power On", fg="green", font=("Arial", 12, "bold"))
        pmtb.config(state=tkinter.DISABLED)
        pmtb2.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def pmtpoweroff():
    try:
        selection = 'PPOWEROF\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        pmtpower.config(text="PMT Power Off", fg="red", font=("Arial", 12, "bold"))
        pmtb2.config(state=tkinter.DISABLED)
        pmtb.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def poweroff():
    try:
        selection = 'POWEROFF\n\r'
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(selection.encode('utf-8'))
        lpower.config(text="Power Off", fg="red", font=("Arial", 12, "bold"))
        b7.config(state=tkinter.DISABLED)
        b6.config(state=tkinter.NORMAL)
        print(selection)
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")
    except serial.SerialException:
        messagebox.showerror("Error", "Connect to an Arduino")


def latch():
    try:
        if illuminate != 0:
            selection = 'LATCH\n\r'
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
        passlength = int(plb.get())
        delaytime = round(9.5 * 1000000 * illuminate / seconds)
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
        b7.config(state=tkinter.NORMAL, bg=defaultbg)
        b6.config(state=tkinter.NORMAL, bg=defaultbg)
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
        db.delete(0, END)
        db.config(state="disabled")
        pb.config(state=tkinter.NORMAL)
        global seconds
        selection = freqcombo.get()
        freq = float(pb.get())
        if selection == "kHz":
            if 7.9 < freq < 4001:
                value = 1000
                frequency = int(value * freq)
                seconds = frequency
                selection5 = 'F ' + str(seconds) + '\n\r'
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(selection5.encode('utf-8'))
                print("selection5")
                print(selection5)
            else:
                messagebox.showerror("Error", "Please choose a frequency between 8kHz and 4MHz")
        elif selection == "MHz":
            if 0.0079 < freq < 4.000001:
                value = 1000000
                frequency = int(value * freq)
                seconds = frequency
                selection5 = 'F ' + str(seconds) + '\n\r'
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(selection5.encode('utf-8'))
                print("selection5")
                print(selection5)
            else:
                messagebox.showerror("Error", "Please choose a frequency between 8kHz and 4MHz")
    except ValueError:
        messagebox.showerror("Error", "Please enter a number")
    except NameError:
        messagebox.showerror("Error", "Connect to an Arduino")


def dwellselection():
    try:
        tb.config(state=tkinter.NORMAL)
        lightcombo.config(state=tkinter.NORMAL)
        b11.config(state=tkinter.NORMAL)
        pb.delete(0, END)
        pb.config(state="disabled")
        db.config(state=tkinter.NORMAL)
        global seconds
        selection3 = dwellcombo.get()
        dwell = float(db.get())
        if selection3 == "ns":
            if 249 < dwell < 125001:
                value = 0.000000001
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
            else:
                messagebox.showerror("Error", "Dwell time should be between 250ns and 125µs")
        elif selection3 == "µs":
            if 0.249 < dwell < 126:
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
            else:
                messagebox.showerror("Error", "Dwell time should be between 250ns and 125µs")
    except ValueError:
        messagebox.showerror("Error", "Please enter a number")
    except (serial.SerialException, NameError):
        messagebox.showerror("Error", "Connect to an Arduino")


def timeselection():
    try:
        plb.config(state=tkinter.NORMAL)
        b8.config(state=tkinter.NORMAL)
        b9.config(state=tkinter.NORMAL)
        global illuminate
        global multiplier
        global selected
        selection2 = lightcombo.get()
        time = float(tb.get())
        if selection2 == "ns":
            if time < 999:
                multiplier = 1 / seconds
                time = time * 0.000000001
                multiplier = float(multiplier)
                illuminate = time / multiplier
                illuminate = round(illuminate)
                selected = str(illuminate)
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
                multiplier = 1 / seconds
                time = time * 0.000001
                multiplier = float(multiplier)
                illuminate = time / multiplier
                illuminate = round(illuminate)
                print(illuminate)
                selected = str(illuminate)
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
                messagebox.showwarning("Warning", "Please choose ms")
        elif selection2 == "ms":
            if time < 999:
                multiplier = 1 / seconds
                time = time * 0.001
                multiplier = float(multiplier)
                illuminate = time / multiplier
                illuminate = round(illuminate)
                print(illuminate)
                selected = str(illuminate)
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
            multiplier = 1 / seconds
            time = time * 1
            multiplier = float(multiplier)
            illuminate = time / multiplier
            illuminate = round(illuminate)
            print(illuminate)
            selected = str(illuminate)
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
        pb.config(state=tkinter.NORMAL)
        db.config(state=tkinter.NORMAL)
        pb.delete(0, END)
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
root.title("TR-OSL Interface v0.3")

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

infoframe = Frame(root, borderwidth=5, relief="sunken")
softwareframe = LabelFrame(root, text="MCS-32 Software", font=("Arial", 9, "bold"))
connection_frame = LabelFrame(root, text="Arduino Connection", font=("Arial", 9, "bold"))
ledframe = LabelFrame(root, text="Light Source Driver", font=("Arial", 9, "bold"))
dataframe = LabelFrame(root, text="Experiment Start", font=("Arial", 9, "bold"))
selectionframe = LabelFrame(root, text="Parameter Selection", font=("Arial", 9, "bold"))
movementframe = LabelFrame(root, text="Movement Control", font=("Arial", 9, "bold"))

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

lpower = Label(ledframe, text="Power", font=("Arial", 12, "bold"))
b6 = Button(ledframe, text="Power On", command=poweron, height=2, width=15, font="Arial")
b7 = Button(ledframe, text="Power Off", command=poweroff, height=2, width=15, font="Arial")
pmtb = Button(ledframe, text="PMT Power On", command=pmtpoweron, height=2, width=15, font="Arial")
pmtb2 = Button(ledframe, text="PMT Power On", command=pmtpoweroff, height=2, width=15, font="Arial")
pmtpower = Label(ledframe, text="PMT Power", font=("Arial", 12, "bold"))
lpower.grid(row=0, column=0)
b6.grid(row=1, column=0)
b7.grid(row=2, column=0)
pmtpower.grid(row=0, column=1)
pmtb.grid(row=1, column=1)
pmtb2.grid(row=2, column=1)
pmtb.config(state=tkinter.DISABLED)
pmtb2.config(state=tkinter.DISABLED)
b6.config(state=tkinter.DISABLED)
b7.config(state=tkinter.DISABLED)

l3 = Label(dataframe, text="Enter Pass Count", font="Arial")
b8 = Button(dataframe, text="Latch", command=latch, height=2, width=15, font="Arial")
plb = Entry(dataframe, justify=LEFT, width=23)
b9 = Button(dataframe, text="Start Countdown", command=start, height=2, width=15, font="Arial")
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

l2 = Label(selectionframe, text="Enter Frequency", font="Arial")
pb = Entry(selectionframe, justify=LEFT, width=33)
freqcombo = ttk.Combobox(selectionframe, state="readonly", values=["kHz", "MHz"], font="Arial")
freqcombo.current(0)
b10 = Button(selectionframe, text="Frequency selection", command=frequencyselection, height=1, width=22, font="Arial")
l3 = Label(selectionframe, text="Enter Dwell Time", font="Arial")
db = Entry(selectionframe, justify=LEFT, width=33)
dwellcombo = ttk.Combobox(selectionframe, state="readonly", values=["ns", "µs"], font="Arial")
dwellcombo.current(0)
b12 = Button(selectionframe, text="Dwell selection", command=dwellselection, height=1, width=22, font="Arial")

tb = Entry(selectionframe, justify=LEFT, width=33)
l4 = Label(selectionframe, text="Enter Illumination Time", font="Arial")
lightcombo = ttk.Combobox(selectionframe, state="readonly", values=["ns", "µs", "ms", "s"], font="Arial")
lightcombo.current(0)
b11 = Button(selectionframe, text="Time selection", command=timeselection, height=1, width=22, font="Arial")
l5 = Label(selectionframe, text="Your rounded pulse count is", font="Arial")
l6 = Label(selectionframe, text=illuminate, font=("Arial", 12, "bold"))
l2.grid(row=0, column=0)
pb.grid(row=1, column=0)
freqcombo.grid(row=2, column=0)
b10.grid(row=3, column=0)
l3.grid(row=0, column=1)
db.grid(row=1, column=1)
dwellcombo.grid(row=2, column=1)
b12.grid(row=3, column=1)
l4.grid(row=4, column=0)
tb.grid(row=5, column=0)
lightcombo.grid(row=6, column=0)
b11.grid(row=7, column=0)
l5.grid(row=6, column=1)
l6.grid(row=7, column=1)
pb.config(state=tkinter.DISABLED)
freqcombo.config(state=tkinter.DISABLED)
b10.config(state=tkinter.DISABLED)
db.config(state=tkinter.DISABLED)
dwellcombo.config(state=tkinter.DISABLED)
b12.config(state=tkinter.DISABLED)

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

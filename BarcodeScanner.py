import threading
import time

import os

import pyautogui
import d3dshot
from pyzbar.pyzbar import decode

from pynput import mouse

from playsound import playsound
import pyperclip
from plyer import notification

# Daniel Shaw
# Github: https://github.com/Daniel-Shaw-MT
# Development time ~1 Week
# Any questions? Contact me at danshawmt@hotmail.com, +356 99331049

# This algorithm contains all the logic for the program. From selection of monitor to detection and parsing.
def detectionAl():

    # Global decleration of what to copy to clipboard (Not used)
    global fin
    fin = ""

    print(
    "\n ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______  "
    +"\n|______|______|______|______|______|______|______|______|______|______|______| "
    +"\n _____  _                             _     _ _                                "
    +"\n|  __ \| |                           | |   (_) |                               "
    +"\n| |__) | | __ _ _   _ _ __ ___   ___ | |__  _| |                               "
    +"\n|  ___/| |/ _` | | | | '_ ` _ \ / _ \| '_ \| | |                               "
    +"\n| |    | | (_| | |_| | | | | | | (_) | |_) | | |                               "
    +"\n|_|    |_|\__,_|\__, |_| |_| |_|\___/|_.__/|_|_|                               "
    +"\n ____            __/ |         _         _____                                 "
    +"\n|  _ \          |___/         | |       / ____|                                "
    +"\n| |_) | __ _ _ __ ___ ___   __| | ___  | (___   ___ __ _ _ __  _ __   ___ _ __ "
    +"\n|  _ < / _` | '__/ __/ _ \ / _` |/ _ \  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|"
    +"\n| |_) | (_| | | | (_| (_) | (_| |  __/  ____) | (_| (_| | | | | | | |  __/ |   "
    +"\n|____/ \__,_|_|  \___\___/ \__,_|\___| |_____/ \___\__,_|_| |_|_| |_|\___|_|   "
    +"\n ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______  "
    +"\n|______|______|______|______|______|______|______|______|______|______|______| "
    "\n \nPlease select a monitor from the list:")

    # Creates screen capture instance using D3D
    d = d3dshot.create(capture_output="numpy", frame_buffer_size=1)

    # Choose display
    for i, display in enumerate(d.displays):
        current_display = display
        print(str(i + 1) + ') ' + display.name + '\n')

    # Set display
    current_display.i = int(input("Select display by number: ")) - 1
    d.display = d.displays[current_display.i]
    print('\n You\'ve selected [' + str(current_display.i+1) + '] ' + current_display.name)

    # Lets user know the program has started in the log
    print(" Capture Started! Now just hover over any barcode and the program will automatically\n"
          "scan it and copy it to the clipboard, just hit paste in any program of your choice (Right click -> Paste "
          "OR CTRL+V)\n "
          "and the barcode that you scanned will be pasted!\n To stop scanning for barcodes just close the program "
          "with the X button on the top right!")
    # Start capturing
    d.capture(target_fps=10)

    # Notifies the user of the program starting.
    notification.notify(
        # title of the notification,
        title="Barcode Scanner Started",
        # the body of the notification
        message="Just hover over any barcode to scan.",
        # creating icon for the notification
        # we need to download a icon of ico file format
        app_icon="icon.ico",
        # the notification stays for 10sec
        timeout=10
    )
    time.sleep(0.1)
    count=0
    while True:
        # Captures latest frame from screen cap
        img = d.get_latest_frame()

        # Decodes whole frame places results in array format for further parsing later.
        decoded = decode(img)

        # Captures mouse pos.
        pos = pyautogui.position()

        # If nothing was detected on the screen for 5 minutes (FPS Based)
        if count>5000:
            print("nothing detected for too long")
            notification.notify(
                # title of the notification,
                title="Barcode Scanner shutting down due to inactivity",
                # the body of the notification
                message="Shutting down due to 5 minutes of inactivity.",
                # creating icon for the notification
                # we need to download a icon of ico file format
                app_icon="icon.ico",
                # the notification stays for 10sec
                timeout=10
            )
            break

        # If nothing was detected for 4 minutes (FPS BASED)
        if count==4000:
            notification.notify(
                # title of the notification,
                title="No barcodes have been detected for 4 Minutes",
                # the body of the notification
                message="Barcode scanner will automatically close in 1 minute, if you are still using it please scan a "
                        "barcode to reset the timer.",
                # creating icon for the notification
                # we need to download a icon of ico file format
                app_icon="icon.ico",
                # the notification stays for 10sec
                timeout=10
            )

        # Counts number of frames where a barcode is not present anywhere on screen
        # Used to count number of frames where idle, if count == 5000 means that 5 min has passed
        # about 10fps rate of increment.
        if len(decoded) < 1:
            count+=1

        # If decoded contains anything the idle frame count is set to 0. Resets idle timer.
        elif decoded:
            count = 0

            # Will loop through decoded array, calculate bounding box per detected entity.
            for barcode in decoded:
                # Logic for calculating bounding box.

                # Math functions to determine extremes of each barcode.
                rect = barcode.rect
                WLeft = rect.width+rect.left
                WH = rect.top+rect.height

                # Determines if mouse is over barcode or not.
                if pos[0] <= WLeft and pos[0]>= rect.left and pos[1]<WH and pos[1]>rect.top:
                    # If it is:
                    # Copies data from barcode to clipboard
                    data = str(barcode.data)
                    noB = data.replace('b', '')
                    fin = noB.replace("'", '')
                    # Calls beep function to play a barcode beep sound
                    beep()
                    # Copies data to clipboard
                    pyperclip.copy(fin)


# Plays barcode beep sound when called
def beep():
    # Dynamic directory detection
    cwd = os.getcwd()
    playsound(cwd+'/beep.mp3')

# Experimental click detection (NOT USED)
def on_click(x, y, button, pressed):
    print()
    # threading.Thread.start(beep())

# Starts detection Al and initializes mouse click listener
def click_listener():
    listener = mouse.Listener(
        on_click=on_click)
    listener.start()
    threading.Thread.start(detectionAl())
    exit(0)

# Main function, initializes threads
def main():
    threading.Thread.start(click_listener())

# Calling main functions
main()
exit(0)

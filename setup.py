import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os", "threading", "numpy", "time", "pyautogui", "d3dshot", "pyzbar", "pynput", "playsound", "pyperclip", "plyer", "sys"], 'include_files': ['beep.mp3', 'icon.ico'], 'include_msvcr': True, "excludes": []}

# base="Win32GUI" should be used only for Windows GUI app
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(
    name = "BarcodeScanner",
    version = "1.0.0",
    description = "Playmobil Barcode Scanner!",
    options = {"build_exe": build_exe_options},
    executables = [Executable("BarcodeScanner.py",icon="icon.ico", base=base)]
)
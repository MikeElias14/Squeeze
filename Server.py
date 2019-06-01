import serial
import time
import ctypes
import socket
import sys

# For simulating keystrokes

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

# Don't need mouse or hardware input, but need the classes for the input union
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))

class KEYBOARDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBOARDINPUT),
                ('hi', HARDWAREINPUT))

class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))

def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)

INPUT_KEYBOARD = 1

def Input(structure):
    if isinstance(structure, KEYBOARDINPUT):
        return INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure))
    raise TypeError('Cannot create INPUT structure!')

KEY_A = 0x41
KEY_B = 0x42
KEY_C = 0x43
KEY_D = 0x44
KEY_E = 0x45
KEY_F = 0x46
KEY_G = 0x47
KEY_H = 0x48
KEY_I = 0x49
KEY_J = 0x4A
KEY_K = 0x4B
KEY_L = 0x4C
KEY_M = 0x4D
KEY_N = 0x4E
KEY_O = 0x4F
KEY_P = 0x50
KEY_Q = 0x51
KEY_R = 0x52
KEY_S = 0x53
KEY_T = 0x54
KEY_U = 0x55
KEY_V = 0x56
KEY_W = 0x57
KEY_X = 0x58
KEY_Y = 0x59
KEY_Z = 0x5A

def KeyboardInput(code, flags):
    return KEYBOARDINPUT(code, code, flags, 0, None)

def Keyboard(code, flags=0):
    return Input(KeyboardInput(code, flags))


# Main
def main():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('10.10.100.254', 8899)
    print(f'connecting to {server_address}')
    sock.connect(server_address)

    # For wired testing
    # ard = serial.Serial('COM3', 9600, timeout=5)
    # sock = ard

    running = True
    while running:

        # Serial read section
        # msg = sock.read(sock.inWaiting()) # read everything in the input buffer
        # valves = str(msg)[2:5]

        # Socket read section
        received = 0
        expected = 3
        
        while received < expected:
            data = sock.recv(16)
            received += len(data)
            valves = str(data)[2:5]
            print(f'Recieved: {valves}')


        # This is the note the player is playing, and the keypress needed to make it happen on the musical typing keyboard,
        # Centered where keyboard input 'G' plays the note 'G'.
        note = ''
        if valves == '000':
            # Reset keystokes when nothing is played
            SendInput(Keyboard(KEY_G, KEYEVENTF_KEYUP))
            SendInput(Keyboard(KEY_H, KEYEVENTF_KEYUP))
            SendInput(Keyboard(KEY_J, KEYEVENTF_KEYUP))

        elif valves =='111':
            # End connection when all buttons pressed
            print('closing socket')
            sock.close()
            exit()

        elif valves == '101':
            note = 'G'
            SendInput(Keyboard(KEY_G))

        elif valves == '110':
            note = 'A'
            SendInput(Keyboard(KEY_H))

        elif valves == '010':
            note = 'B'
            SendInput(Keyboard(KEY_J))

        print(f'Valves: {valves} : {note}')
        time.sleep(0.1)

if __name__ == "__main__":
    main()
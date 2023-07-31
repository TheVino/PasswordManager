# motivação: https://github.com/betinn/GDSB-WPF
import random
from PySimpleGUI import PySimpleGUI as sg

def generate_password():
    length = 16
    amount = 1
    uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase_letters = uppercase_letters.lower()
    digits = "0123456789"
    symbols = "!@#$%^&*()_+-=[]{};:,.<>/?"

    upper, lower, nums, syms = True, True, True, True

    all =""
    if upper:
        all += uppercase_letters
    if lower:
        all += lowercase_letters
    if nums:
        all += digits
    if syms:
        all += symbols

    for x in range(amount):
        password = "".join(random.sample(all, length))
        print(password) 
        return password

def window_home():
    sg.theme('Dark Blue 3')
    layout = [
        [sg.VPush()],
        [sg.Text('Password Generator')],
        [sg.Image(r'C:\Users\vini_\Desktop\Script\passMngr\Photos\DALL-E-password.png')],
        [sg.Button('Generate')],
        # [sg.Button('Compare'),sg.Input()],
        [sg.Button('Exit')],
        [sg.VPush()],
    ]
    return sg.Window('Home', layout=layout , finalize=True)

def window_generate():
    sg.theme('Dark Blue 3')
    layout  = [
        [sg.VPush()],
        [sg.Text('Your password generated:')],
        [sg.Text(key)],
        [sg.Button('Home')],
        [sg.Button('Generate Another')],
        [sg.Button('Use it')],        
        [sg.VPush()],
    ]
    return sg.Window('Generate', layout=layout, finalize=True)


#%% Main run  
if __name__ == "__main__":
    print("--==RUNNING PASSWORD GENERATOR==--")

    #var declarations
    key =""

    # Create the starting windows var declarations
    window1 = window_home()
    windowcompare, windowgenerate  = None, None

    # create a loop to continuous read the windows
    while True:
        window, event, values = sg.read_all_windows()
        # event1: window closed
        if event in(sg.WIN_CLOSED,'Exit'):
            break
        
        if window == window1 and event == 'Generate':
            key = generate_password()
            windowgenerate = window_generate()
            window1.hide

        if window == windowgenerate and event == 'Generate Another':
            windowgenerate.close()
            key = generate_password()
            windowgenerate = window_generate()
            window1.hide

        if window == windowgenerate and event == 'Use it':
            print('using password: ' + key)
            window1.hide
                  
        if window == windowgenerate and event == 'Home':
            windowgenerate.close()
            window1.un_hide    
            
    window.close()
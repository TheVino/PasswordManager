# motivation: https://github.com/betinn/GDSB-WPF
# https://www.tutorialspoint.com/pysimplegui/pysimplegui_spin_element.htm
# https://www.youtube.com/watch?v=DLn3jOsNRVE
# Table of Elements in Tkinter Port -> https://www.pysimplegui.org/en/latest/#building-custom-windows
# make an API to check the programs version, to send the updates whenever the customers open the app

# to add a master password to check and decrypt, please read and search as the link below:
# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet

import random, os, io, base64, sys, ctypes, PIL.Image, time
from random import randint
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from PySimpleGUI import PySimpleGUI as sg
from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def get_display_size(): # just to check display size
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    Width = user32.GetSystemMetrics(0)
    Height = user32.GetSystemMetrics(1)
    return Width, Height

def resize_background(resize=None): # check display resolution and resize image to 50% max display resolution
    sizes = get_display_size()
    resize = (round(int(resize[0])/2),round(int(resize[1])/2))
    rnd = randint(0,1)
    if rnd == 1:
        image = 'C:\\Users\\vini_\\Desktop\\Script\\passMngr\\Photos\\DALL-E-password.png'
    else:
        image = 'C:\\Users\\vini_\\Desktop\\Script\\passMngr\\Photos\\DALL·E-chibi.png'
    if isinstance(image, str):
        img = PIL.Image.open(image)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(image)))
        except Exception as e:
            data_bytes_io = io.BytesIO(image)
            img = PIL.Image.open(data_bytes_io)
    cur_width, cur_height = img.size
    if resize:
        new_width, new_height    = resize
        scale   = min(new_height/cur_height, new_width/cur_width)
        img     = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.LANCZOS)
    bio     = BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def check_main_password(master_password): # actually main password is 'senha'
    check = ""
    cyhper_master_password = fer.encrypt(master_password.encode()).decode()
    decryp_master_password = fer.decrypt(cyhper_master_password.encode()).decode()
    stored_cypher_password = "gAAAAABlk7unFmYOQd43Q2THULwQ2GnTiNxWDjvEIzI3fzfbTsx95gahWLn6yqzg4rZb7zX0WFLNO7Nwr91BNk2JJ0B8C3nXUA=="
    decryp_stored_password = fer.decrypt(stored_cypher_password.encode()).decode()
    if decryp_master_password == decryp_stored_password:
        check = True
        pass
    else:
        wps=window_wrong_password()
        wps
        time.sleep(3)
        check = False
        sys.exit()
    # sys.exit() 
    return check

def write_key(): # This function is only written once, to generate the main key (private key)
    private_key = Fernet.generate_key()
    with open("private_key.key", "wb") as key_file:
        key_file.write(private_key)

def load_key(): # Load private key to decrypt password
    file    = open("private_key.key", "rb")
    read_file     = file.read()
    file.close()
    return read_file

def generate_password(keycount): # Generate password, as it is
    # length = values['-chars-']
    length = keycount
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
        return str(password)

def add(login, key, notes): # Store password, login and notes on a file
    with open('passwords.txt', 'a') as password_file:
        password_file.write(login + "|" + fer.encrypt(key.encode()).decode() + "|" + notes + "\n")
    return

#TODO need to modify this to view the passwords on GUI
def view(): # Display the passwords
    with open('passwords.txt', 'r') as password_file:
        for line in password_file.readlines():
            data = line.rstrip()
            user, passw, note = data.split("|")
            print("Login:", user, "| Password:", fer.decrypt(passw.encode()).decode(), "| Notes:", note)
    pass

def window_check_password(): # window to type main password to initialize the program
    sg.theme('Dark Blue 3')
    layout = [
        [sg.VPush()],
        [sg.Text('Please enter your password to open the program: ')],
        [sg.Input(key='-masterKeyInput-')],
        [sg.Button('Enter', key='-Enter-',bind_return_key=True)], # bind_return_key=True triggers this action when "enter" is pressed
        [sg.Button('Exit')],
        [sg.VPush()],
    ]
    return sg.Window('Welcome to Password Manager', layout=layout , finalize=True, return_keyboard_events=True)

def window_wrong_password(): # Just display a msg that the user typed the wrong password
    sg.theme('Dark Blue 3')
    layout = [
        [sg.VPush()],
        [sg.Text('Wrong password entered, please type the correct password next time.. Bye :)')],
        [sg.VPush()],
    ]
    return sg.Window('Wrong password', layout=layout , finalize=True)

def window_home(): # main window, with most buttons an calls
    image = resize_background(resize=get_display_size())
    sg.theme('Dark Blue 3')
    chars= [i for i in range(8, 25)]
    image_re = [[sg.VPush()],
        [sg.Text('Password Generator')],
        [sg.Image(image)],
        [sg.Button('View Passwords')],
        [sg.Button('Generate')],
        [sg.Text('How many characters you want?')],
        [sg.Spin(chars,initial_value=16,size=3,auto_size_text=True, enable_events=True, key= '-chars-')],
        [sg.Button('Exit')],
        [sg.VPush()],]

    layout = [
        [sg.Column(image_re,expand_x=True, expand_y=True)]
    ]
    return sg.Window('Home', layout=layout , location=(300, 150), resizable=True, finalize=True)

def window_generate(): # window after password is generated
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

def window_add_password(key): # window that displays password generated ans has boxes to add login and password
    login = "asdas"
    sg.theme('Dark Blue 3')
    layout  = [
        [sg.VPush()],
        [sg.Text('Insert your Login to store:')],
        [sg.Input(login)],
        [sg.Text('Your password generated: ' + str(key))],
        [sg.Text('Notes (optional):')],
        [sg.Input(tooltip= "Website, School, Bank Account...")],
        [sg.Button('Save')],
        [sg.Button('Home')],        
        [sg.VPush()],
    ]
    return sg.Window('Save Password', layout=layout, finalize=True)

#TODO need to add an edit/ modify login and a delete one, with security password to delete
#%% Main run  
if __name__ == "__main__":
    print("--==RUNNING PASSWORD GENERATOR==--")
    
    #var declarations
    key = load_key()
    fer = Fernet(key)

    # Here is the Hazmat lib to handle password encryption
    # salt = os.urandom(16)
    # kdf = PBKDF2HMAC(
    #     algorithm=hashes.SHA256(),
    #     length=32,
    #     salt=salt,
    #     iterations=480000,
    #     backend=default_backend()
    # )
    # print(kdf)
    # kdf_key = base64.urlsafe_b64encode(kdf.derive(b_master_password))
    # print(kdf_key)
    # f = Fernet(kdf_key)
    # token = f.encrypt(b'message')
    # print(token)
    # print (f.decrypt(token))
    
    # Create the starting windows var declarations
    window1 = window_check_password()
    windowhome, windowcompare, windowgenerate, windowaddpassword, windowwrongpassword  = None, None, None, None, None

    # create a loop to continuous read the windows
    while True:
        window, event, values = sg.read_all_windows()
        # event1: window closed
        if event in(sg.WIN_CLOSED,'Exit'):
            break
        
        if window == window1 and event == '-Enter-':
            mainPasswordInput = check_main_password(values['-masterKeyInput-'])
            windowhome = window_home()
            window1.close()
            
        if window == windowhome and event == 'View Passwords':
            view()

        if window == windowhome and event == 'Generate':
            keycount = values['-chars-']
            key = generate_password(keycount)
            windowgenerate = window_generate()
            windowhome.hide

        if window == windowgenerate and event == 'Generate Another':
            windowgenerate.close()
            key = generate_password(keycount)
            windowgenerate = window_generate()
            windowhome.hide

        if window == windowgenerate and event == 'Use it':
            windowgenerate.close()
            windowaddpassword = window_add_password(key)
            saved_password = print('using password: ' + str(key))
            windowhome.hide
                  
        if window == windowgenerate and event == 'Home':
            windowgenerate.close()
             
        if window == windowaddpassword and event == 'Save':
            login           = str(values[0])
            notes           = str(values[1])
            saved_message   = print('using login: '     + login)
            saved_password  = print('using password: '  + key  )
            saved_notes     = print('using notes: '     + notes)
            add(login, key, notes)
            windowaddpassword.close()


        if window == windowaddpassword and event == 'Home':
            windowaddpassword.close()
            windowhome.hide

    window.close()
# %%

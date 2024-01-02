# motivação: https://github.com/betinn/GDSB-WPF
# https://www.tutorialspoint.com/pysimplegui/pysimplegui_spin_element.htm
# https://www.youtube.com/watch?v=DLn3jOsNRVE
# Table of Elements in Tkinter Port -> https://www.pysimplegui.org/en/latest/#building-custom-windows
# make an API to check the programs version, to send the updates whenever the customers open the app

# to add a master password to check and decrypt, please read and serach as the link below:
# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet

from random import randint
import random, os, base64, sys
from PySimpleGUI import PySimpleGUI as sg
from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def check_main_password(master_password): # actually main password is 'senha'
    cyhper_master_password = fer.encrypt(master_password.encode()).decode()
    decryp_master_password = fer.decrypt(cyhper_master_password.encode()).decode()
    stored_cypher_password = "gAAAAABlk7unFmYOQd43Q2THULwQ2GnTiNxWDjvEIzI3fzfbTsx95gahWLn6yqzg4rZb7zX0WFLNO7Nwr91BNk2JJ0B8C3nXUA=="
    decryp_stored_password = fer.decrypt(stored_cypher_password.encode()).decode()
    if decryp_master_password == decryp_stored_password:
        pass
    else:
        sys.exit() 
    return

# This function is only written once, to generate the main key (private key)
def write_key():
    private_key = Fernet.generate_key()
    with open("private_key.key", "wb") as key_file:
        key_file.write(private_key)

def load_key():
    file    = open("private_key.key", "rb")
    read_file     = file.read()
    file.close()
    return read_file

def generate_password(keycount):
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

# need to modify this to actually store the login and password to a file
def add(login, key, notes):
    with open('passwords.txt', 'a') as password_file:
        password_file.write(login + "|" + fer.encrypt(key.encode()).decode() + "|" + notes + "\n")
    return

# need to modify this to view the passwords
def view():
    with open('passwords.txt', 'r') as password_file:
        for line in password_file.readlines():
            data = line.rstrip()
            user, passw, note = data.split("|")
            print("Login:", user, "| Password:", fer.decrypt(passw.encode()).decode(), "| Notes:", note)
    pass

def window_check_password():
    sg.theme('Dark Blue 3')
    layout = [
        [sg.VPush()],
        [sg.Text('Please enter your password to open the program: ')],
        [sg.Input()],
        [sg.Button('Enter')],
        [sg.Button('Exit')],
        [sg.VPush()],
    ]
    return sg.Window('Welcome to Password Manager', layout=layout , finalize=True)

def window_home():
    rnd = randint(0,1)
    if rnd == 1:
        image = 'C:\\Users\\vini_\\Desktop\\Script\\passMngr\\Photos\\DALL-E-password.png'
    else:
        image = 'C:\\Users\\vini_\\Desktop\\Script\\passMngr\\Photos\\DALL·E-chibi.png'
    sg.theme('Dark Blue 3')
    chars= [i for i in range(8, 25)]
    layout = [
        [sg.VPush()],
        [sg.Text('Password Generator')],
        [sg.Image(image)],
        [sg.Button('View Passwords')],
        [sg.Button('Generate')],
        [sg.Text('How many characters you want?')],
        [sg.Spin(chars,initial_value=16,size=3,auto_size_text=True, enable_events=True, key= '-chars-')],
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

# need to modify this to accept boxes to store login and notes
def window_add_password(key):
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
    windowhome, windowcompare, windowgenerate, windowaddpassword, windowcheckpassword  = None, None, None, None, None

    # create a loop to continuous read the windows
    while True:
        window, event, values = sg.read_all_windows()
        # event1: window closed
        if event in(sg.WIN_CLOSED,'Exit'):
            break
        
        if window == window1 and event == 'Enter':
            check_main_password(str(values[0]))
            windowhome = window_home()
            window1.hide()
        
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

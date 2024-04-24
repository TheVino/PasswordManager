
# Password Manager 🔐

Hi! This program can generate passwords, storage, manage and view them. All passwords are encrypted to increase the protection, and are only decrypted when you pass the main password check.

# What libs do I need? 
<!---
```
 pip install PySimpleGUI
 pip install cryptography
 pip install pillow
 ```
--->
<img src="https://imgur.com/oMCL4sP.png" alt="drawing" width="400"/>


## Main code has these main functions


- View Passwords
- Generate Password (with # characters   selection)
- Save Password and Login
- Master Password to Start the program



## Testing the program! 👨‍💻
<!---
```
def  check_main_password(master_password): # actually main password is 'senha'
```
--->
![](https://imgur.com/CPASsyP.png)
**Returns**: <br>
![](https://i.imgur.com/y2FGR1g.png)
-------------
Once you pass the Main Password verification, we are in the main screen:
![](https://i.imgur.com/0FSV6Kf.png)
```
View Passwords
```
**Returns**: <br>
![enter image description here](https://i.imgur.com/B5r70DP.png)
```
Generate Password
```
**Returns**: <br>
![](https://i.imgur.com/9VqWtkJ.png)
```
Use it
```
Will copy the password generated (the example has different passwords, but you get the idea)
**Returns**:
![enter image description here](https://i.imgur.com/pDwX55o.png)

Once you click on **Save**, it will return to main screen. If we click on **View Passwords** again, we can see the last password generated is there:
![](https://i.imgur.com/cAuY4bw.png)

For safety, if you check the file where the passwords are stored, they are encrypted:
![](https://i.imgur.com/1LR8Vux.png)

Future Features:
- MFA to increase security on login
- Better UI *(Not that easy to build good UI with PySimpleGUI)*
- View saved passwords on GUI ~~not terminal~~
- Add an edit/ modify login and a delete one, with security password to delete
- Add Update OTA (Over-the-air) to keeps the app updated

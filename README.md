# College Management System
This project is a GUI-based College Management System designed to streamline the management of college data. It utilizes an SQLite database to store information about students, library, courses, and more.

## Technologies\Modules Used
1. __customtkinter (v5.2.2):__ A modern and customizable Python UI library based on Tkinter, used for creating the project's graphical user interface.
2. __sqlite3:__ SQLite is a python embeded database. This module is used to connect to SQLite database.
3. __os:__ For operating system related tasks.
4. __PIL:__ For loading all the Images and Icons.
5. __sys:__ Using sys.exit() to make sure proper exiting of `.exe` file.
6. __re:__ For checking that email is proper and other string patterns.
7. __datetime:__ For Date and Time related tasks.
8. __pandas, numpy:__ For Excel related tasks.
9. __tkinter.filedialog:__ askdirectory and askopenfilename functions.
10. __random:__ For generating OTP.
11. __smtplib, email:__ For sending email of OTP.

## Features
### 1. Signin Form, Create Account Form, Forget Password
- Allows users to sign in with existing credentials or create a new account.
- Provides a mechanism to reset forgotten passwords.

![Screenshot 2024-03-04 153428](https://github.com/Harshit1234G/College-Management-System/assets/119939567/d9558993-daca-4f3c-93fe-dfd239dabdd5)

### 2. Menu
- There are 4 options in the menu:
    - Accounts: It has all the student and fee related options. 
    - Library: It has all the library related tasks.
    - Courses: It has all the Courses related tasks.
    - Excel: Importing data from Excel file to Database, Exporting data from Database to Excel file.

All these options contains various functionalities with icons and names as shown in the below screenshots.
  
![Screenshot 2024-03-04 154411](https://github.com/Harshit1234G/College-Management-System/assets/119939567/8f738897-07d6-4765-8fd7-971e481746d5)
![Screenshot 2024-03-04 154421](https://github.com/Harshit1234G/College-Management-System/assets/119939567/d92ae950-f562-4b85-8841-db37de008ef3)
![Screenshot 2024-03-04 154435](https://github.com/Harshit1234G/College-Management-System/assets/119939567/fb2be2c5-836e-4d0f-b83e-772598490ec1)
![Screenshot 2024-03-04 154446](https://github.com/Harshit1234G/College-Management-System/assets/119939567/d461a072-2b1a-4724-b2b0-1a07e189545d)

### 3. Tables
- Data is presented in clear tables throughout the application, as shown in the screenshot below. These tables offer automatic cell resizing, dynamically adjusting height and width to accommodate the content within each cell.

![Screenshot 2024-03-04 160304](https://github.com/Harshit1234G/College-Management-System/assets/119939567/bc81dec9-bae4-4285-bb5d-e0b460cef7eb)

### 4. Settings and Shortcuts
- User can change the theme from dark to light.
- User Can set default tab on startup.
- Some special settings are only accessible by Admin.
- There are various different shortcuts, like for switching tabs, etc.

![Screenshot 2024-03-04 161337](https://github.com/Harshit1234G/College-Management-System/assets/119939567/c6cc7b3d-dc84-4155-8b5a-b09c688145aa)

## Future Enhancements
These are some of the features that I would I like to add in future:
1. Adding a proper feature for creating Admin account.
2. Enhancing GUI, making it more attractive.

## Setup
I'll add the link to download the setup file of my software.

## Usage
### Account creation:
For normal account just provide the credentials, but for Admin account it is a little weird (I'll implement it properly later), follow the steps to create Admin account.
1. Click on `Forgot password?`
2. The software will prompt you to create Admin account, if the Admin doesn't exsits.
3. The Admin creation window will open, aside from email it will also require SMTP key or app password to send OTP via your email.

### Steps to get the SMTP key:
1. Open any Browser.
2. Go to your account settings or Manage your Google Account.
3. Search for App passwords.
4. Enter your email password there to verify its you.
5. The app passwords will appear, create a new app-specific password.
6. You will get a 16-bit key, enter that in SMTP key field.

If these steps won't work for you, try googling about it. I recommend using Chrome Browser.

### After that:
You are good to go to use the software, you can create as many account you want. Everything should work fine after doing this.

## Project Status: 
Project is: _complete_

## Note: 
- This project is licensed under the MIT License. See the LICENSE file (https://github.com/Harshit1234G/College-Management-System/blob/master/license.txt) for details.
- If you want more detailed information about each function or class then look over the respective docstring.

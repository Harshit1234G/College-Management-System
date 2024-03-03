import customtkinter as ctk
from database_connector import DatabaseConnector
from messagebox import ShowError, ShowInfo
import re
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import ImageTk, Image
import os
import sys


class SigninForm(ctk.CTk):
    """
    Creates the basic GUI of sigin form, create account form and forget password form.
    """
    access_granted = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #basic attributes
        self.title('College Management System')
        self.resizable(False, False)

        # changing icon
        self.imagepath = ImageTk.PhotoImage(file=os.path.join('icons', 'app.png'))
        self.wm_iconbitmap()
        self.iconphoto(False, self.imagepath)

        # theme
        ctk.set_appearance_mode('light')

        self.sign_in_gui()


    def __content_remover(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()

    def sign_in_gui(self) -> None:
        """
        Sign in form GUI.
        """
        self.geometry('600x430')
        self.__content_remover()

        #stringvars
        self.user_name = ctk.StringVar()
        self.password = ctk.StringVar()

        #basic gui
        self.header_label = ctk.CTkLabel(
            master= self,
            text= 'Sign in',
            font= ('arial', 28, 'bold')
        )
        self.header_label.grid(
            row= 0, 
            column= 1, 
            padx= 20,
            pady= (45, 10),
            sticky= 'w', 
            columnspan= 2
        )

        #entry widgets
        #username
        ctk.CTkLabel(
            master= self,
            text= 'Username'
        ).grid(row= 1, column= 1, sticky= 'w', padx= 22)

        self.user_name_widget = ctk.CTkEntry(
            master= self,
            textvariable= self.user_name,
            width= 260,
            border_color= '#72d2ff',
            border_width= 3
        )

        self.user_name_widget.grid(
            row= 2, 
            column= 1,
            padx= 20,
            columnspan= 2,
            sticky= 'w'
        )

        #password 
        ctk.CTkLabel(
            master= self,
            text= 'Password'
        ).grid(row= 3, column= 1, sticky= 'w', padx= (22, 0), pady= (10, 0))

        self.password_widget = ctk.CTkEntry(
            master= self,
            textvariable= self.password,
            width= 260,
            show= '*', 
            border_color= '#72d2ff',
            border_width= 3
        )

        self.password_widget.grid(
            row= 4, 
            column= 1,
            padx= (20, 0),
            sticky= 'w',
            columnspan= 2
        )

        self.show_or_hide_button = ctk.CTkButton(
            master= self,
            text= 'Show',
            command= self.__show_or_hide,
            width= 50,
            fg_color= "#ceefff",
            border_color= "#72d2ff",
            border_width= 3, 
            hover_color= '#72d2ff',
            text_color= '#000000'
        )

        self.show_or_hide_button.grid(
            row= 4,
            column= 2,
            sticky= 'e',
            padx= (0, 20)
        )

        # forgot passowrd
        self.forgot_password = ctk.CTkButton(
            master= self, 
            text= "Forgot password?", 
            text_color= '#2873ed',
            fg_color= '#ceefff',
            hover_color= '#ceefff',
            width= 10, 
            command= self.forget_password_gui
        )

        self.forgot_password.grid(
            row= 5, 
            column= 1, 
            pady= 5,
            padx= (15, 0),
            sticky= 'w'
        )

        #sign in button
        self.submit_button = ctk.CTkButton(
            master= self, 
            text= 'Sign in',
            corner_radius= 30,
            width= 260,
            height= 32, 
            command= self.__sign_in
        )

        self.submit_button.grid(
            row= 7, 
            column= 1,
            columnspan= 2,
            padx= 20,
            pady= (20, 5)
        )

        #create account
        self.create_account = ctk.CTkButton(
            master= self, 
            text= "Don't have an account? Create one.", 
            text_color= '#2873ed',
            fg_color= '#ceefff',
            hover_color= '#ceefff',
            width= 10, 
            command= self.create_account_gui
        )

        self.create_account.grid(
            row= 8, 
            column= 1, 
            padx= (15, 0),
            sticky= 'w'
        )

        #adding image
        image = ctk.CTkImage(
            Image.open(os.path.join('icons', 'sigin_form_img.jpg')), 
            size= (300, 600)
        )

        self.decorative_image = ctk.CTkLabel(
            master= self,
            text= '',
            image= image
        )

        self.decorative_image.grid(
            row= 0,
            column= 0,
            sticky= 'w',
            rowspan= 80
        )

    def create_account_gui(self) -> None:
        """
        Create account GUI.
        """
        self.geometry('600x430')
        self.email = ctk.StringVar()

        self.header_label.configure(text= 'Create Account')
        self.forgot_password.destroy()

        #email
        self.email_label = ctk.CTkLabel(
            master= self,
            text= 'Email'
        )

        self.email_label.grid(
            row= 5, 
            column= 1, 
            sticky= 'w', 
            padx= 20, 
            pady= (10, 0)
        )

        self.email_widget = ctk.CTkEntry(
            master= self,
            textvariable= self.email,
            width= 260,
            border_color= '#72d2ff',
            border_width= 3
        )

        self.email_widget.grid(
            row= 6, 
            column= 1,
            padx= 20,
            columnspan= 2,
            sticky= 'w'
        )

        #changing sigin to create account
        self.submit_button.configure(text= 'Create Account', command= self.__create_account)
        self.create_account.configure(text= 'Have an account! Sign in.', command= self.sign_in_gui)

    def __show_or_hide(self) -> None:
        """
        Show or Hide button implementation, if the button displays Show that means the current password field has hidden the content and displays '*' in place of letters. If the button displays Hide that means the current password field will display all the characters. It is opposite to read here but makes sense when you see the GUI.
        """
        button_text = self.show_or_hide_button.cget('text')
        if button_text == 'Show':
            self.show_or_hide_button.configure(text= 'Hide')
            self.password_widget.configure(show= '')

        else:
            self.show_or_hide_button.configure(text= 'Show')
            self.password_widget.configure(show= '*')

    def __sign_in(self) -> None:
        """
        This function first takes the username and password from the stringvars. Then it will retrieve the respective user's password from the database and checks if the username and password are correct. If they are correct it will grant the access.
        """
        username = self.user_name.get()
        password = self.password.get()

        error_msg = ''

        #retrieving user data
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                SELECT password
                FROM user
                WHERE username = ?;
                ''',
                [username]
            )

            user_data = connector.cursor.fetchall()
        
        #if user exists then check password
        if user_data:
            if password != user_data[0][0]:
                error_msg = 'Wrong Password! Access Denied.'
        
        else:
            error_msg = f"'{username}' user doesn't exist."

        if error_msg:
            ShowError(error_msg= error_msg)
            return None
        
        #granting Access and deleting form
        ShowInfo('Access Granted', f'Welcome! {username}. Loading data...')
        self.access_granted = True
        self.after(1000, self.destroy)

    def __create_account(self) -> None:
        """
        Gets the details from the stringvars and checks constraints. If all the constraints passes then the user data will be inserted to the database.
        """
        username = self.user_name.get()
        password = self.password.get()
        email = self.email.get()

        error_msg = ''

        if not username.rstrip():
            error_msg = 'Please enter username.'

        elif not password.rstrip():
            error_msg = 'Please enter password.'

        elif not email.rstrip():
            error_msg = 'Please enter email.'

        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            error_msg = 'Please enter a proper mail ID.'

        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                SELECT username
                FROM user;
                '''
            )

            existing_users = connector.cursor.fetchall()
        
        if (username,) in existing_users:
            error_msg = f'Username "{username}" is not available.'

        if error_msg:
            ShowError(error_msg= error_msg)
            return None
        
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                INSERT INTO user(username, password, email)
                VALUES (?, ?, ?);
                ''',
                [username, password, email]
            )

            connector.db.commit()

        ShowInfo('Account Created', 'Sign in with the new account.')
        self.after(1000, self.sign_in_gui)

    #all funcs below are for forget password
    def forget_password_gui(self) -> None:
        """
        Creates the GUI for forget password.
        """
        #check user existence and send mail
        if not self.__check_user_existence_and_send_otp():
            return None

        #removing all previous widgets
        self.__content_remover()

        self.geometry('600x430')

        #adding image
        image = ctk.CTkImage(
            Image.open(os.path.join('icons', 'sigin_form_img.jpg')), 
            size= (300, 600)
        )

        self.decorative_image = ctk.CTkLabel(
            master= self,
            text= '',
            image= image
        )

        self.decorative_image.grid(
            row= 0,
            column= 0,
            sticky= 'w',
            rowspan= 80
        )

        #gui of forget password
        self.header_label = ctk.CTkLabel(
            master= self,
            text= 'Forget Password',
            font= ('arial', 28, 'bold')
        )
        self.header_label.grid(
            row= 0, 
            column= 1, 
            padx= 20,
            pady= (45, 10),
            sticky= 'w'
        )

        ctk.CTkLabel(
            master= self,
            text= "We've send an OTP to this user's registered email. Enter OTP to verify.",
            wraplength= 260,
            justify= 'left'
        ).grid(row= 1, column= 1, padx= 20, sticky= 'w', pady= (0, 10))

        #otp field
        self.user_entered_otp = ctk.StringVar()

        ctk.CTkLabel(
            master= self,
            text= 'OTP'
        ).grid(row= 2, column= 1, sticky= 'w', padx= 20)

        self.otp_widget = ctk.CTkEntry(
            master= self,
            textvariable= self.user_entered_otp,
            width= 260,
            border_color= '#72d2ff',
            border_width= 3
        )

        self.otp_widget.grid(
            row= 3, 
            column= 1,
            padx= 20,
            columnspan= 2,
            sticky= 'w'
        )

        #resend otp
        self.resend_otp = ctk.CTkButton(
            master= self, 
            text= "Didn't get the OTP? Resend it.", 
            text_color= '#2873ed',
            fg_color= '#ceefff',
            hover_color= '#ceefff',
            width= 10, 
            command= lambda: self.__check_user_existence_and_send_otp(resend= True)
        )

        self.resend_otp.grid(
            row= 4, 
            column= 1, 
            pady= 5,
            padx= (15, 0),
            sticky= 'w'
        )

        #verify button
        self.verify_button = ctk.CTkButton(
            master= self, 
            text= 'Verify',
            corner_radius= 30,
            width= 260,
            height= 32, 
            command= self.__verify_otp
        )

        self.verify_button.grid(
            row= 5, 
            column= 1,
            columnspan= 2,
            padx= 20,
            pady= (20, 5)
        )

    def __check_user_existence_and_send_otp(self, resend: bool = False) -> bool:
        """
        Generates an otp via __generate_otp and send it to the user's email after checking user existence.
        """
        #getting user email
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                SELECT email
                FROM user
                WHERE username = ?;
                ''',
                [username := self.user_name.get()]
            )

            data = connector.cursor.fetchall()

        if data:
            email = data[0][0]

        else:
            ShowError(error_msg= "This user doesn't exists.")
            return False
        
        if not resend:
            self.forgot_password.configure(text= 'Please Wait...', state= 'disabled')
            self.update()

        else:
            self.resend_otp.configure(text= 'Resending...', state= 'disabled')
            self.update()
        
        #getting otp and sending mail to user
        self.otp = self.__generate_otp()
        self.__send_email(username, email)

        if resend:
            self.resend_otp.configure(text= "Didn't get the OTP? Resend it.", state= 'enabled')
            self.update()

        return True
        
    @staticmethod
    def __generate_otp() -> str:
        otp = ''.join(random.sample([str(i) for i in range(1, 10)], 6))
        return otp
    
    def __send_email(
        self, 
        username: str, 
        receiver_email: str
    ) -> None:
        """
        Used to send email.
        """
        #body of email
        email_body = f"""
Dear {username},

We received a request to reset the password associated with your College Management System account. To proceed, please use the following One-Time Password (OTP):

OTP: {self.otp}

If you did not request a password reset, please ignore this email. Your account security is important to us.

Please do not share this OTP with anyone for security reasons. If you encounter any issues or did not request this password reset, contact our support team immediately at harshitnibm1@gmail.com.

Thank you for using College Management System.

Best regards,
Harshit Kumawat
"""

        #get admin's email
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                SELECT email
                FROM user
                WHERE username = "Admin";
                '''
            )

            smtp_email = connector.cursor.fetchall()[0][0]

        #email configuration
        message = MIMEMultipart()
        message["From"] = smtp_email
        message['To'] = receiver_email
        message['Subject'] = 'College Management System Password Reset'
        message.attach(MIMEText(email_body))
        
        #smtp configuration
        smtp_server = "smtp.gmail.com"      #SMTP server
        smtp_port = 587                     #SMTP with TLS(transport layer security) has this port number
        smtp_username = smtp_email
        smtp_16_bit_key = 'use your key here'

        try:
            #initialize SMTP (simple mail transfer protocol)
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                #use TLS security
                server.starttls()
                #login admin account
                server.login(smtp_username, smtp_16_bit_key)
                #sendmail
                server.sendmail(smtp_email, receiver_email, message.as_string())

        except Exception as e:
            ShowError(Exception, e)

    def __verify_otp(self) -> None:
        user_entered_otp = self.user_entered_otp.get()

        if user_entered_otp == self.otp:
            self.__content_remover()
            self.geometry('600x430')

            #adding image
            image = ctk.CTkImage(
                Image.open(os.path.join('icons', 'sigin_form_img.jpg')), 
                size= (300, 600)
            )

            self.decorative_image = ctk.CTkLabel(
                master= self,
                text= '',
                image= image
            )

            self.decorative_image.grid(
                row= 0,
                column= 0,
                sticky= 'w',
                rowspan= 80
            )

            self.header_label = ctk.CTkLabel(
                master= self,
                text= 'Change Password',
                font= ('arial', 28, 'bold')
            )
            self.header_label.grid(
                row= 0, 
                column= 1, 
                padx= 20,
                pady= (45, 10),
                sticky= 'w',
                columnspan= 2
            )

            #password
            ctk.CTkLabel(
                master= self,
                text= 'Password'
            ).grid(row= 1, column= 1, sticky= 'w', padx= (22, 0), pady= (10, 0))

            self.password_widget = ctk.CTkEntry(
                master= self,
                textvariable= self.password,
                width= 260,
                show= '*', 
                border_color= '#72d2ff',
                border_width= 3
            )

            self.password_widget.grid(
                row= 2, 
                column= 1,
                padx= (20, 0),
                sticky= 'w',
                columnspan= 2
            )

            self.show_or_hide_button = ctk.CTkButton(
                master= self,
                text= 'Show',
                command= self.__show_or_hide,
                width= 50,
                fg_color= "#ceefff",
                border_color= "#72d2ff",
                border_width= 3, 
                hover_color= '#72d2ff',
                text_color= '#000000'
            )

            self.show_or_hide_button.grid(
                row= 2,
                column= 2,
                sticky= 'e',
                padx= (0, 20)
            )

            #change_password button
            self.change_password_button = ctk.CTkButton(
                master= self,
                text= 'Change Password',
                corner_radius= 30,
                width= 260,
                height= 32, 
                command= self.__change_password_of_user_in_db
            )

            self.change_password_button.grid(
                row= 3, 
                column= 1,
                columnspan= 2,
                padx= 20,
                pady= (20, 5)
            )

        else:
            ShowError('Wrong OTP', 'The OTP you entered is wrong, access denied.')
            self.after(3000, sys.exit)

    def __change_password_of_user_in_db(self) -> None:
        password = self.password.get()
        username = self.user_name.get()

        if not len(password): 
            ShowError('Invalid Password', 'Please enter password.')
            return None

        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                UPDATE user
                SET password = ?
                WHERE username = ?;
                ''',
                [password, username]
            )
            connector.db.commit()

        ShowInfo('Password', 'Successfully changed the password.')
        self.sign_in_gui()

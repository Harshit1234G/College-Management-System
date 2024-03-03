#Achievement Unlocked: 5000+ lines of code in this project.
import customtkinter as ctk
import os
from PIL import ImageTk, Image
from menu import Menu
from content_frame import ContentFrame
from database_connector import DatabaseConnector
from pre_req_test import PreReqTester
from signin_form import SigninForm
import sys 

#running pre-requisite test
error = PreReqTester()
if len(error):
    app = ctk.CTk()
    app.geometry("300x100")
    app.title('College Management System')

    ctk.CTkLabel(
        master= app,
        text= f"! {error}",
        text_color= 'red'
    ).pack(pady= 10)

    app.mainloop()
    sys.exit()


class MainWindow(ctk.CTk):
    """
    Main window class for the College Management System GUI.

    This class represents the main window of the College Management System graphical user interface (GUI).
    It includes essential attributes, such as window size, title, icon, content frame, menu, and settings button.

    Attributes:
        - user (str): The user of the program. 
        - geometry: The size of the main window in the format 'widthxheight'.
        - minsize: The minimum size constraints for the main window.
        - title: The title displayed on the main window.
        - imagepath: The path to the icon image file.
        - content: An instance of ContentFrame, the main content frame of the GUI.
        - menu: An instance of Menu, providing menu options for various functionalities.
        - settings_image: An instance of CTkImage representing the settings icon.
        - setting_button: A button for accessing application settings.

    Example:
    ```
    main_window = MainWindow()
    main_window.mainloop()
    ```

    Note:
    Ensure that the 'icons' directory contains the necessary image files for the window icon and settings button.
    """

    def __init__(self, user: str) -> None:
        super().__init__()
        
        self.user = user
        self.__version__ = "1.1"

        # basic attributes
        self.geometry('900x550')
        self.minsize(900, 550)
        self.title('College Management System')

        # changing icon
        self.imagepath = ImageTk.PhotoImage(
            file=os.path.join('icons', 'app.png'))
        self.wm_iconbitmap()
        self.iconphoto(False, self.imagepath)

        # content
        self.content = ContentFrame(
            master=self,
            user= self.user,
            corner_radius= 0
        )
        self.content.pack(
            fill='both',
            expand=True,
            padx=5,
            pady=(10, 5),
            anchor='s',
            side='right'
        )

        # menu
        self.menu = Menu(
            master=self,
            content_frame=self.content,
            width=200,
            corner_radius= 0,
            fg_color= '#1F6AA5',
            segmented_button_selected_color= '#1F6AA5'
        )
        self.menu.pack(
            expand=True,
            anchor='w'
        )

        # settings
        img_path = os.path.join('icons', 'settings.png')

        self.settings_image = ctk.CTkImage(
            Image.open(img_path),
            size= (40, 40)
        )
        self.setting_button = ctk.CTkButton(
            master=self,
            image=self.settings_image,
            text='Settings',
            command=self.content.settings_gui,
            font= ('arial', 14),
            anchor= 'w',
            corner_radius= 0,
            fg_color= '#1F6AA5'
        )
        self.setting_button.pack(ipadx= 36, padx=(1, 0))

        # shortcut binding
        # for changing tabs
        self.bind('<Control-Key-1>', lambda _: self.menu.set('Accounts'))
        self.bind('<Control-Key-2>', lambda _: self.menu.set('Library'))
        self.bind('<Control-Key-3>', lambda _: self.menu.set('Courses'))
        self.bind('<Control-Key-4>', lambda _: self.menu.set('Excel'))

        # for different funcs of accounts
        self.bind('<Control-Shift-N>', self.content.new_admission_gui)
        self.bind('<Control-f>', self.content.fetch_student_data)
        self.bind('<Control-u>', self.content.update_student_gui)
        self.bind('<Control-d>', self.content.deposit_fee)
        self.bind('<Control-Delete>', self.content.remove_student_gui)

        # for library
        self.bind('<Control-l>', self.content.lend_book)
        self.bind('<Control-r>', self.content.return_book)
        self.bind('<Control-b>', self.content.show_books)
        self.bind('<Control-Shift-A>', self.content.add_book_gui)
        self.bind('<Control-Shift-R>', self.content.remove_book_gui)
        self.bind('<Control-Shift-U>', self.content.update_stock_gui)

        # for courses
        self.bind('<Control-Alt-c>', self.content.add_course_gui)
        self.bind('<Control-Alt-r>', self.content.remove_course_gui)
        self.bind('<Control-Alt-u>', self.content.update_course_gui)
        self.bind('<Control-Alt-s>', self.content.show_all_courses)

        # for excel
        self.bind('<Control-Shift-X>', self.menu.export_data_to_excel)
        self.bind('<Control-Insert>', self.menu.import_data_from_excel)

        # for settings
        self.bind('<Control-`>', self.content.settings_gui)


if __name__ == '__main__':
    sign_in_form = SigninForm(fg_color= '#ceefff')
    sign_in_form.mainloop()

    user_name = sign_in_form.user_name.get()

    if not sign_in_form.access_granted:
        sys.exit()


    app = MainWindow(user= user_name)
    with DatabaseConnector() as connector:
        connector.cursor.execute(
            '''
            SELECT value
            FROM settings
            WHERE setting = "theme";
            '''
        )
        theme = connector.cursor.fetchall()[0][0]

    ctk.set_appearance_mode(theme)
    app.mainloop()

import customtkinter as ctk
import re
from datetime import datetime
from database_connector import DatabaseConnector
from messagebox import ShowError, ShowInfo, ShowWarning

type CTkWindow = ctk.CTk
type stringvar = ctk.StringVar
type StrOrNone = str | None
type ctkButton = ctk.CTkButton
type BookData = tuple[int, str]
type ctkFrame = ctk.CTkFrame


class ContentFrame(ctk.CTkScrollableFrame):
    """
    A customtkinter ScrollableFrame that serves as the main GUI frame for displaying various functionalities. This class contains all the functions related to Accounts, Library and Courses.

    Usage: 

    The following functions should be called from the Menu class:
        - `new_admission_gui()`
        - `fetch_student_data()`
        - `update_student_gui()`
        - `remove_student_gui()`
        - `deposit_fee()`
        - `add_course_gui()`
        - `remove_course_gui()`
        - `update_course_gui()`
        - `show_all_courses()`
        - `add_book_gui()`
        - `remove_book_gui()`
        - `show_books()`
        - `lend_book()`
        - `return_book()`
        - `update_stock_gui()`

    All other functions are either implicitly called by the above functions or triggered by an event (like button clicked).

    Parameters:
        - master (CTkWindow): The master widget (customtkinter window).

    Attributes:
        - All attributes are explained in their respective functions.

    Note:
        - master attribute must be a customtkinter window.
        - Randomly calling any function may result in inappropriate behaviour and errors.
        - These functions are designed to be called via Menu class, and will execute in a specific order.
    """

    def __init__(self, master: CTkWindow, user: str, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.user = user

    # helper funcs
    def content_remover(self) -> None:
        """
        It uses customtkinter's winfo_children() to get all widgets currently present in the frame, and destroy them one-by-one. This is widely used in various functions of this class.

        Parameters:
            - None

        Returns:
            - None
        """
        for widget in self.winfo_children():
            widget.destroy()

    def __create_label_and_entry(
            self,
            text: str,
            text_variable: stringvar,
            row: int,
            padx: int = 50,
            pady: int = 5,
            columnspan: int = 3,
            sticky: str = 'w',
            width: int = 360
    ) -> None:
        """
        It is used to create both label and entry widget.

        Parameters:
            - text (str): text to display in label
            - text_variable (stringvar): ctk.StringVar() for storing entry widget value
            - row (int): row value to grid in GUI
            - padx (int): padding at x-axis
            - pady (int): padding at y-axis
            - columnspan (int): number of columns to be occupied by the entry widgets
            - sticky (str): side of label
            - width (int): width of entry widget (in pixels)

        Returns:
            - None
        """

        label = ctk.CTkLabel(
            master=self,
            text=text
        )
        label.grid(
            row=row,
            column=0,
            padx=padx,
            pady=pady,
            sticky=sticky
        )

        entry = ctk.CTkEntry(
            master=self,
            textvariable=text_variable,
            width=width
        )
        entry.grid(
            row=row,
            column=1,
            columnspan=columnspan
        )

    def __get_course_info(self, choice: StrOrNone = None) -> None:
        """
        This function is used to update the course_info label which displays the information related to the course onto the label.

        Parameters:
            - choice (str): The value selected in the combobox is passed to it via `ctk.ctkComboBox()`

        Returns:
            - None
        """
        with DatabaseConnector() as connector:
            # finding all the integers
            course_id = re.findall(r'\d+', self.course_var.get())
            connector.cursor.execute(
                'SELECT * FROM courses WHERE course_id = ?',
                course_id
            )

            result = connector.cursor.fetchall()[0]

        self.course_info.configure(
            text=f'{"Course ID": <10}: {result[0]}\n{"Name": <10}: {result[1]}\n{"Fee": <10}: {result[2]}\n{"Year": <10}: {result[3]}')

    def __age_calc(self, date: str) -> int:
        """
        This method takes a date string, converts it to a datetime object, calculates the age based on the current date, and returns the result as an integer

        Parameters:
            - date (str): date string of form `YYYY-MM-DD`

        Returns:
            - int, age of person
        """

        birth_date = datetime.strptime(date, "%Y-%m-%d")
        current_date = datetime.now()

        # First calculates the difference in years between the current year and the birth year.Then a tuple comparison. It checks if the current month and day are earlier in the year than the birth month and day. If true, it means the birthday for the current year hasn't occurred yet, so we subtract 1 from the age.
        age = current_date.year - birth_date.year - \
            ((current_date.month, current_date.day)
             < (birth_date.month, birth_date.day))

        return age

    @staticmethod
    def __valueGetter(var: str) -> StrOrNone:
        """
        Private function used to check that the provided string is only whitespaces or a valid string.

        Parameters:
            - var (str): string variable

        Returns:
            - StrOrNone, if string is whitespaces then returns `None` else returns the string.
        """
        if var.rstrip() == "":
            return None

        else:
            return var

    def __get_info_from_widgets_for_accounts(self) -> tuple:
        """
        It is used to get values from the widgets present in the accounts window (mainly new_admission and update_student).

        Parameters:
            - None

        Returns:
            - tuple of name, f_name, year, month, day, address, phone_no, email, gender, pincode, course_id, class_10_per, class_12_per all these variables.
        """
        name = self.__valueGetter(self.name_var.get())
        f_name = self.__valueGetter(self.f_name_var.get())

        year = self.__valueGetter(self.year_var.get())
        month = self.__valueGetter(self.month_var.get())
        day = self.__valueGetter(self.day_var.get())

        address = self.__valueGetter(self.address_var.get())
        phone_no = self.__valueGetter(self.phone_no_var.get())
        email = self.__valueGetter(self.email_var.get())

        gender = self.gender_var.get()
        pincode = self.__valueGetter(self.pincode_var.get())

        course_id = re.findall(r'\d+', self.course_var.get())

        class_10_per = self.__valueGetter(self.per10_var.get())
        class_12_per = self.__valueGetter(self.per12_var.get())

        return name, f_name, year, month, day, address, phone_no, email, gender, pincode, course_id, class_10_per, class_12_per

    def __get_info_from_widgets_for_courses(self) -> tuple:
        """
        It is used to get values from the widgets present in the courses window (mainly add_course and update_course).

        Parameters:
            - None

        Returns:
            - tuple of course_id, course_name, fee, course_year all these variables.
        """
        course_id = self.__valueGetter(self.course_id.get())
        course_name = self.__valueGetter(self.course_name.get())
        fee = self.__valueGetter(self.fee.get())
        course_year = self.__valueGetter(self.course_year.get())

        return course_id, course_name, fee, course_year

    def __ask_enrollment(
        self,
        label_text: str,
        command: callable,
        button_text: str = 'Submit'
    ) -> None:
        """
        Creates a label, entry widget and a button

        Parameters:
            - label_text (str): text to be displayed in the label
            - command (callable): function to be called after clicking the button
            - button_text (str): text to be displayed on the button (default 'Submit')

        Returns:
            - None
        """
        self.content_remover()

        enrollment_frame = ctk.CTkFrame(
            master= self,
            fg_color= ("#f2f2f4", "#4a4a4a")
        )

        enrollment_frame.pack(pady= 5)

        header = ctk.CTkLabel(
            master=enrollment_frame,
            text=label_text,
            font=('arial', 28)
        )
        header.grid(
            row= 0, 
            column= 0,
            padx=10,
            pady=10,
            columnspan= 2
        )

        self.enrollment_no = ctk.StringVar()
        enroll_label = ctk.CTkLabel(
            master=enrollment_frame,
            text='Enrollment Number',
            justify='left'
        )
        enroll_label.grid(
            row= 1, 
            column= 0,
            padx= (50, 10), 
            pady=5
        )

        entry = ctk.CTkEntry(
            master=enrollment_frame,
            textvariable=self.enrollment_no,
            width=200
        )
        entry.grid(
            row= 1,
            column= 1,
            padx= (0, 50)
        )

        button = ctk.CTkButton(
            master=enrollment_frame,
            text=button_text,
            command=command,
            width= 200
        )

        button.grid(
            row= 2, 
            column= 1,
            pady=(5, 10),
            sticky= 'w'
        )

    def __create_checkbox_from_list(self, books: list[BookData]) -> int:
        """
        This is used to create checkboxes for books provided in the list.

        Parameters:
            - books (list of BookData): contains tuple of book_id and book name, usually read from a database.

        Attributes:
            - stringvars_for_checkbox (dict[int, stringvar]): dictionary of book_id and stringvar.
            - all_of_the_above (stringvar): stringvar for all of the above checkbox.

        Returns:
            - int, index of row griding.
        """

        # creating books_dict with key=book_id and value=bookname, for easyness sake
        books_dict = {
            book_data[0]: (book_data[1], book_data[2]) for book_data in books
        }

        self.stringvars_for_checkbox: dict[int, stringvar] = {
            book_id: ctk.StringVar() for book_id in books_dict
        }

        for index, book_id in enumerate(books_dict):
            ctk.CTkCheckBox(
                master=self,
                text= f"{books_dict[book_id][0]}, By {books_dict[book_id][1]}",
                variable=self.stringvars_for_checkbox[book_id],
                command=lambda: self.all_of_the_above.set('off'),
                onvalue='on',
                offvalue='off'
            ).grid(row=index+1, column=1, pady=5, sticky='w')

        self.all_of_the_above = ctk.StringVar()

        ctk.CTkCheckBox(
            master=self,
            text='All of the above',
            variable=self.all_of_the_above,
            command=self.__clicked_all_of_the_above,
            onvalue='on',
            offvalue='off'
        ).grid(row=index+2, column=1, pady=5, sticky='w')

        return index

    def __clicked_all_of_the_above(self) -> None:
        """
        Selects all the options after clicking all of the above.
        """
        if self.all_of_the_above.get() == 'on':
            value_to_set = 'on'

        else:
            value_to_set = 'off'

        for stringvar in self.stringvars_for_checkbox.values():
            stringvar.set(value_to_set)

    def __create_table(
        self, 
        master: ctkFrame,
        header: str,
        row: int, 
        col: int, 
        data: list[tuple[str]],
        word_wrap_length: int = 400
    ) -> None:
        """
        Creates a table of rowxcol dimensions and assigns a value to it according to data.

        Parameters:
            - master (ctkFrame): a customtkinter frame object.
            - row (int): Number of rows in the table.
            - col (int): Number of columns in the table.
            - data (list[tuple[str]]): `list` of `tuples` containing strings. `row` must be equal to the number of strings in tuple, `col` must be equal to number of tuples. 
        """
        #header
        ctk.CTkLabel(
            master=master,
            text= header,
            font=('arial', 28)
        ).pack(pady= 5, padx= 5)

        # Create a container frame to hold the table
        container_frame = ctk.CTkFrame(
            master= master,
            fg_color= ('#f2f2f4', '#4a4a4a')
        )
        container_frame.pack()

        frame = ctk.CTkFrame(
            master=container_frame,
            fg_color=('#f2f2f4', '#4a4a4a')
        )
        frame.pack(
            pady=5,
            padx=5
        )

        # Set weights for rows and columns
        for i in range(row):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(col):
            frame.grid_columnconfigure(i, weight=1, minsize= 100)

        for x in range(row):
            for y in range(col):
                if x == 0 or y == 0:
                    fg = ('#7983ad', '#40486d')
                else:
                    fg = ('#DBDBDB', '#2B2B2B')

                frame_grid = ctk.CTkFrame(
                    master= frame,
                    border_width= 2,
                    corner_radius= 0,
                    border_color= ('#000000', '#ffffff'),
                    fg_color= fg
                )
                frame_grid.grid(
                    row= x, 
                    column= y,
                    sticky= 'nsew'
                )
                labelGrid = ctk.CTkLabel(
                    master= frame_grid, 
                    text= data[x][y],
                    wraplength= word_wrap_length
                )
                labelGrid.pack(
                    padx=5, 
                    pady=5
                )


    # new admission funcs
    def new_admission_gui(
        self,
        event: any = None,
        update: bool = False
    ) -> None:
        """
        Main GUI function for new admission

        Parameters:
            - update (bool): this gui is used for both new admission and update student, if update is True then it will not create the submit and clear button.

        Attributes:
            - self.name_var (stringvar): stringvar to store value of name
            - self.f_name_var (stringvar): stringvar to store value of father name
            - self.year_var (stringvar): stringvar to store value of year
            - self.month_var (stringvar): stringvar to store value of month
            - self.day_var (stringvar): stringvar to store value of day
            - self.phone_no_var (stringvar): stringvar to store value of phone number 
            - self.email_var (stringvar): stringvar to store value of email
            - self.pincode_var (stringvar): stringvar to store value of pincode
            - self.address_var (stringvar): stringvar to store value of address
            - self.gender_var (stringvar): stringvar to store value of gender
            - self.per10_var (stringvar): stringvar to store value of 10th percentage
            - self.per12_var (stringvar): stringvar to store value of 12th percentage
            - self.course_var (stringvar): stringvar to store value of course_id and name

        Returns: 
            - None
        """

        self.content_remover()

        self.name_var = ctk.StringVar()
        self.f_name_var = ctk.StringVar()
        self.year_var = ctk.StringVar(value= '-Year-')
        self.month_var = ctk.StringVar(value= '-Month-')
        self.day_var = ctk.StringVar(value= '-Day-')
        self.phone_no_var = ctk.StringVar()
        self.email_var = ctk.StringVar()
        self.pincode_var = ctk.StringVar()
        self.address_var = ctk.StringVar()
        self.gender_var = ctk.StringVar()
        self.per10_var = ctk.StringVar()
        self.per12_var = ctk.StringVar()
        self.course_var = ctk.StringVar(value= '-Select-')

        # student details
        ctk.CTkLabel(
            master=self,
            text='Student Details',
            font=('arial', 28)
        ).grid(row=0, column=0, padx=10, pady=10)

        self.name = self.__create_label_and_entry("Name", self.name_var, 1)
        self.f_name = self.__create_label_and_entry(
            "Father Name", self.f_name_var, 2)

        # Date fo birth
        ctk.CTkLabel(
            master=self,
            text='Date of Birth'
        ).grid(
            row=3,
            column=0,
            padx=50,
            pady=5,
            sticky='w'
        )
        self.year = ctk.CTkComboBox(
            master=self,
            values=[str(i) for i in range(1980, datetime.now().year - 15)],
            variable=self.year_var,
            width=110
        )
        self.year.grid(
            row=3,
            column=1
        )

        self.month = ctk.CTkComboBox(
            master=self,
            values=[str(i) for i in range(1, 13)],
            variable=self.month_var,
            width=110
        )
        self.month.grid(
            row=3,
            column=2
        )

        self.day = ctk.CTkComboBox(
            master=self,
            width=110,
            values=[str(i) for i in range(1, 32)],
            variable=self.day_var
        )
        self.day.grid(
            row=3,
            column=3
        )

        self.address = self.__create_label_and_entry(
            "Address", self.address_var, 4)

        self.phone_no = self.__create_label_and_entry(
            "Phone Number", self.phone_no_var, 5)

        self.email = self.__create_label_and_entry(
            "Email (if any)", self.email_var, 6)

        # gender
        ctk.CTkLabel(
            master=self,
            text='Gender'
        ).grid(
            row=7,
            column=0,
            padx=50,
            pady=5,
            sticky='w'
        )
        ctk.CTkRadioButton(
            master=self,
            text='Male',
            variable=self.gender_var,
            value='M'
        ).grid(
            row=7,
            column=1
        )
        ctk.CTkRadioButton(
            master=self,
            text='Female',
            variable=self.gender_var,
            value='F'
        ).grid(
            row=7,
            column=2
        )
        ctk.CTkRadioButton(
            master=self,
            text='Other',
            variable=self.gender_var,
            value='O'
        ).grid(
            row=7,
            column=3
        )

        self.pincode = self.__create_label_and_entry(
            "Pincode", self.pincode_var, 8, width=110, columnspan=1)

        # percent
        self.per10 = self.__create_label_and_entry(
            "10th Percentage", self.per10_var, 9, width=110, columnspan=1)
        self.per12 = self.__create_label_and_entry(
            "12th Percentage", self.per12_var, 10, width=110, columnspan=1)

        ctk.CTkLabel(
            master=self,
            text='%'
        ).grid(row=9, column=2, sticky='w')

        ctk.CTkLabel(
            master=self,
            text='%'
        ).grid(row=10, column=2, sticky='w')

        # course
        with DatabaseConnector() as connector:
            connector.cursor.execute("SELECT course_id, name FROM courses")
            course_data = connector.cursor.fetchall()

        courses = ctk.CTkComboBox(
            master=self,
            values=[f"{i[0]}({i[1]})" for i in course_data],
            variable=self.course_var,
            width=110,
            command=self.__get_course_info
        )
        ctk.CTkLabel(
            master=self,
            text='Course'
        ).grid(
            row=11,
            column=0,
            padx=50,
            pady=5,
            sticky='w'
        )
        courses.grid(
            row=11,
            column=1
        )

        self.frame = ctk.CTkFrame(
            master=self,
            fg_color=("#f2f2f4", "#4a4a4a"),
            corner_radius=7
        )
        self.frame.grid(
            row=12,
            column=1,
            columnspan=3,
            pady=5
        )
        self.course_info = ctk.CTkLabel(
            master=self.frame,
            text="Please select course to get its info...",
            width=340,
            height=70,
            font= ('consolas', 14),
            justify= 'left'
        )
        self.course_info.grid(row=0, column=0, padx=10, pady=10)

        if not update:
            # submit button
            self.submit_button = ctk.CTkButton(
                master=self,
                text='Submit',
                width=120,
                command=self.__new_admission_submit
            )
            self.submit_button.grid(
                row=13,
                column=3,
                pady=50
            )

            # clearbutton
            clear_button = ctk.CTkButton(
                master=self,
                text='Clear',
                width=120,
                command=self.new_admission_gui
            )
            clear_button.grid(
                row=13,
                column=1
            )

    def __new_admission_constraints(
        self,
        name: StrOrNone,
        f_name: StrOrNone,
        year: StrOrNone,
        month: StrOrNone,
        day: StrOrNone,
        address: StrOrNone,
        phone_no: StrOrNone,
        email: StrOrNone,
        gender: StrOrNone,
        pincode: StrOrNone,
        course_id: StrOrNone,
        class_10_per: StrOrNone,
        class_12_per: StrOrNone
    ) -> StrOrNone:
        """
        It checks all the values passed to it, to validate them. It is called via `__new_admission_submit()`

        Parameters:
            - Each parameter has value as there name suggests.

        Returns:
            - if any of the following conditions met then it will return the respective error message, else returns None
        """

        name_pattern = r'^[a-zA-Z ]+$'

        if not name:
            return "Please enter Name."

        if not re.match(name_pattern, name):
            return "Invalid Name, please enter a proper name."

        if f_name and not re.match(name_pattern, f_name):
            return "Invalid Father Name, please enter a proper name."

        if year == 'Year':
            return "Please select Year."

        if month == 'Month':
            return "Please select Month."

        if day == 'Day':
            return "Please select Day."

        if not (year.isnumeric() and month.isnumeric() and day.isnumeric()):
            return "Invalid Date, please enter a proper date."

        if not address:
            return "Please enter Address."

        if not phone_no:
            return "Please enter Phone Number."

        if not phone_no.isnumeric() or len(phone_no) != 10:
            return "Invalid Phone Number, please enter a proper number"

        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return "Invalid Email, please enter a proper email."

        if not gender:
            return "Please select Gender."

        if not pincode:
            return "Please enter Pincode."

        if not pincode.isnumeric() or len(pincode) != 6:
            return "Invalid Pincode, please enter a proper pincode."

        if not class_10_per or not class_12_per:
            return "Please enter percentage."

        if not class_10_per.replace('.', '').isnumeric() or not class_12_per.replace('.', '').isnumeric():
            return "Invalid Percentage, please enter a decimal or numeric value."

        if not course_id:
            return "Please select Course."

        with DatabaseConnector() as connector:
            connector.cursor.execute("SELECT course_id FROM courses;")
            courses = connector.cursor.fetchall()

        if int(course_id[0]) not in [i[0] for i in courses]:
            return "Please select correct course from the list."

        return None

    def __new_admission_submit(self) -> None:
        """
        It is the submission function for new admission. Takes all the values from the widgets via `self.__get_info_from_widgets_for_accounts()`. Checks them using `self.__new_admission_constraints()` and shows any error message that is occured. Then insert the values into the database.
        """
        # getting values from widgets
        name, f_name, year, month, day, address, phone_no, email, gender, pincode, course_id, class_10_per, class_12_per = self.__get_info_from_widgets_for_accounts()

        # checking constraints
        if error_msg := self.__new_admission_constraints(name, f_name, year, month, day, address, phone_no, email, gender, pincode, course_id, class_10_per, class_12_per):
            ShowError("New Admission", error_msg)
            return None

        # caluculating dob, age and year of admission
        try:
            dob = f"{year}-{month}-{day}"
            year_of_ad = datetime.now().year
            age = self.__age_calc(dob)

        except ValueError:
            ShowError("New Admission", "Invalid date.")

        # writing data to db
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                'INSERT INTO student(name, dob, address, phone_no, email, year_of_ad, age, gender, pincode, course_id, f_name, class_10_per, class_12_per) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                [name, dob, address, phone_no, email, year_of_ad, age, gender,
                    pincode, course_id[0], f_name, class_10_per, class_12_per]
            )
            connector.db.commit()

            connector.cursor.execute('SELECT last_insert_rowid()')
            enrollment_no = connector.cursor.fetchall()[0][0]

        ShowInfo("New Admission", f"You have successfully submitted the data. Enrollment number: {enrollment_no}")

    # fetch data funcs
    def fetch_student_data(self, event: any = None) -> None:
        'Simply calls __ask_enrollment.'
        self.__ask_enrollment(
            label_text='Fetch Student Data',
            command=self.__fetch_student_submit
        )

    def __fetch_student_submit(self) -> None:
        """
        Submission function for fetch_student_data(), retrives the data of the student (whose enrollment number is provided) from database. If enrollment number is not found then prompt the user with an error message.
        """
        # retreiving student info from db
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                    SELECT * 
                    FROM student
                    INNER JOIN courses
                    ON student.course_id = courses.course_id
                    WHERE enrollment_no = ?
                ''',
                [self.enrollment_no.get()]
            )

            try:
                data = connector.cursor.fetchall()[0]
                self.content_remover()

                frame = ctk.CTkFrame(
                    master= self
                )

                frame.pack(
                    pady= (0, 5), 
                    padx= 5,
                    fill= 'both',
                    expand= True
                )

                # creating table
                data_of_student = [
                    ('Parameter', 'Detail'),
                    ('Enrollment Number', data[0]),
                    ('Name', data[1]),
                    ('Father Name', data[11]),
                    ('Date of Birth', data[2]),
                    ('Address', data[3]),
                    ('Phone Number', data[4]),
                    ('Email', data[5]),
                    ('Year of Admission', data[6]),
                    ('Age', data[7]),
                    ('Gender', data[8]),
                    ('Pincode', data[9]),
                    ('10th Percentage (%)', data[12]),
                    ('12th Percentage (%)', data[13]),
                    ('Course ID', data[10]),
                    ('Course Name', data[16]),
                    ('Course Fee', data[17]),
                    ('Course Year', data[18]),
                    ('Fee Deposited', data[14])
                ]
                self.__create_table(
                    master= frame,
                    header= 'Student Details',
                    row= 19,
                    col= 2,
                    data= data_of_student
                )

            # if data retrived is an empty tuple then prompting error message
            except IndexError:
                ShowError('Fetch Student Data', 'This enrollment number is not found.')

    # update data funcs
    def update_student_gui(self, event: any = None) -> None:
        self.__ask_enrollment(
            label_text='Update Student Data',
            command=self.__update_student_submit
        )

    def __update_student_submit(self) -> None:
        """
        Submission function for update_student_gui(), retrives data of student then calls the new_admission_gui() with update=True, and updates all the entry widgets by the data of student. 
        """
        # retrieving student data
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''SELECT * 
                    FROM student
                    WHERE enrollment_no = ?
                    ''',
                [self.enrollment_no.get()]
            )

            try:
                data = connector.cursor.fetchall()[0]
                self.content_remover()

                self.new_admission_gui(update=True)
                # assigning values to all the variables
                self.name_var.set(data[1])

                if not data[11]:
                    self.f_name_var.set('')
                else:
                    self.f_name_var.set(data[11])

                date = data[2].split('-')

                self.year_var.set(date[0])
                self.month_var.set(date[1])
                self.day_var.set(date[2])
                self.address_var.set(data[3])
                self.phone_no_var.set(data[4])

                if not data[5]:
                    self.email_var.set('')
                else:
                    self.email_var.set(data[5])

                self.gender_var.set(data[8])
                self.pincode_var.set(data[9])
                self.course_var.set(data[10])
                self.per10_var.set(data[12])
                self.per12_var.set(data[13])
                self.__get_course_info()

                update_button = ctk.CTkButton(
                    master=self,
                    text='Update',
                    width=120,
                    command=self.__update_student_data_in_db
                )
                update_button.grid(
                    row=13,
                    column=3,
                    pady=50
                )

            except IndexError:
                ShowError('Fetch Student Data',
                          'This enrollment number is not found.')

    def __update_student_data_in_db(self) -> None:
        """
         Updates the data of a student in the database.

        This method works similarly to the `__new_admission_submit()` method and is called via the `__update_student_submit()` function. It retrieves information from the GUI widgets, performs necessary validations, and updates the student's record in the database.

        """
        name, f_name, year, month, day, address, phone_no, email, gender, pincode, course_id, class_10_per, class_12_per = self.__get_info_from_widgets_for_accounts()

        if error_msg := self.__new_admission_constraints(name, f_name, year, month, day, address, phone_no, email, gender, pincode, course_id, class_10_per, class_12_per):
            ShowError("Update Student", error_msg)
            return None

        try:
            dob = f"{year}-{month}-{day}"
            year_of_ad = datetime.now().year
            age = self.__age_calc(dob)

        except ValueError:
            ShowError("Update Student", "Invalid date.")

        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''UPDATE student
                SET name=?, dob=?, address=?, phone_no=?, email=?, year_of_ad=?, age=?, gender=?, pincode=?, course_id=?, f_name=?, class_10_per=?, class_12_per=?
                WHERE enrollment_no = ?;
                ''',
                [name, dob, address, phone_no, email, year_of_ad, age, gender, pincode,
                    course_id[0], f_name, class_10_per, class_12_per, self.enrollment_no.get()]
            )
            connector.db.commit()
            ShowInfo("Update Student", "You have successfully updated the data.")

    # remove data funcs
    def remove_student_gui(self, event: any = None) -> None:
        self.__ask_enrollment(
            label_text='Remove Student',
            command=lambda: ShowWarning(
                'Remove Student',
                'Do you really want to delete this student, click OK to delete.',
                self.__remove_student_data_in_db
            )
        )

    def __remove_student_data_in_db(self) -> None:
        """
        Removes the data of a student from the database.

        This method is called via the `remove_student_gui()` function and is responsible for deleting the student's record from the database based on their enrollment number.
        """
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                'SELECT name FROM student WHERE enrollment_no = ?',
                [self.enrollment_no.get()]
            )
            result = connector.cursor.fetchall()
            if not result:
                ShowInfo('Remove Student',
                         'This enrollment number is not found.')
                return None

            connector.cursor.execute(
                'DELETE FROM student WHERE enrollment_no = ?',
                [self.enrollment_no.get()]
            )
            connector.db.commit()
            ShowInfo('Remove Student', 'Student is removed.')

    # fee deposit funcs
    def deposit_fee(self, event: any = None) -> None:
        self.__ask_enrollment(
            label_text='Deposit Fee',
            command=self.__get_fee_info
        )

    def __get_fee_info(
        self, 
        generate_receipt: bool = False, 
        current_transaction: int | None = None
    ) -> None:
        """
        Retrieves and displays fee information for a student based on their enrollment number.

        This method connects to the database, retrieves relevant information about the student's fee status and course details, and displays the information on the GUI.

        Parameters: 
            - generate_receipt (bool): If True it will generate the receipt and display to the user, default False
            - current_transaction (int or None): It should only be passed if generate_receipt is True, default None.

        Returns: 
            - None
        """
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''SELECT student.fee_deposited, courses.fee, student.name
                FROM student
                INNER JOIN courses
                ON student.course_id = courses.course_id
                WHERE student.enrollment_no = ?
                ''',
                [self.enrollment_no.get()]
            )
            data = connector.cursor.fetchall()

        try:
            fee_deposited, total_fee, name = data[0]
            remaining_fee = total_fee - fee_deposited

            self.content_remover()

            #left side frame for fee info and depositing
            info_frame = ctk.CTkFrame(
                master= self,
                fg_color= ('#f2f2f4', '#4a4a4a')
            )

            info_frame.pack(
                pady= 5, 
                padx= 5,
                fill= 'both',
                expand= True,
                side= 'left'
            )  

            #receipt frame
            receipt_frame = ctk.CTkFrame(
                master= self,
                fg_color= ('#f2f2f4', '#4a4a4a')
            )
            receipt_frame.pack(
                pady= 5,
                padx= (0, 5),
                fill= 'both',
                expand= True,
                side= 'right'
            )

            fee_info = [
                ('Parameter', 'Detail'),
                ('Name', name),
                ('Total Fee', total_fee),
                ('Fee Deposited', fee_deposited),
                ('Remaining Fee', remaining_fee)
            ]
            #creating table
            self.__create_table(
                master= info_frame,
                header= 'Student Details',
                row= 5,
                col= 2,
                data= fee_info
            )

            #deposit button
            ctk.CTkLabel(
                master= info_frame,
                text='Deposit Fee',
                font=('arial', 28)
            ).pack(padx=10, pady= (10, 5))

            ctk.CTkLabel(
                master= info_frame,
                text='Amount to deposit'
            ).pack(padx=50, pady=5)

            amount = ctk.StringVar()
            entyr = ctk.CTkEntry(
                master= info_frame,
                textvariable=amount,
                width=140
            )
            entyr.pack()

            button = ctk.CTkButton(
                master= info_frame,
                text= 'Deposit',
                command= lambda: self.__change_fee_in_db_and_generate_receipt(amount, fee_deposited, total_fee)
            )

            if remaining_fee == 0:
                button.configure(state= 'disabled')
                entyr.configure(state= 'disabled')

            button.pack(pady=20)

            if generate_receipt:
                ctk.CTkLabel(
                    master= receipt_frame,
                    text= 'Receipt',
                    font= ('arial', 16, 'underline')
                ).pack()

                ctk.CTkLabel(
                    master= receipt_frame,
                    text= 'College Management System',
                    font= ('arial', 28, 'bold')
                ).pack(pady= 5)

                with DatabaseConnector() as connector:
                    connector.cursor.execute(
                        '''
                        SELECT s.address, s.phone_no, c.name, c.year
                        FROM student s
                        INNER JOIN courses c
                        ON s.course_id = c.course_id
                        WHERE s.enrollment_no = ?
                        ''',
                        [self.enrollment_no.get()]
                    )
                    data = connector.cursor.fetchall()[0]

                date_time = datetime.now()
                today_date = date_time.strftime("%d/%m/%Y")

                details = f'''
{"Name of Student": <20}: {name}
{"Phone Number": <20}: {data[1]}
{"Address": <20}: {data[0]}

{"Course Name": <20}: {data[2]}
{"Course Year": <20}: {data[3]}
{"Date of Payment": <20}: {today_date}
'''
                ctk.CTkLabel(
                    master= receipt_frame,
                    text= details,
                    font= ('consolas', 14),
                    justify= 'left',
                    wraplength= 600
                ).pack(pady= (0, 10))

                table_data = [
                    ('Sr.No.', 'Particulars', 'Amount(₹)'),
                    (1, 'Total Fee', total_fee),
                    (2, 'Fee Deposited (current transaction)', current_transaction),
                    (3, 'Overall Fee Deposited', fee_deposited),
                    (4, 'Remaining Fee', remaining_fee)
                ]

                self.__create_table(
                    master= receipt_frame,
                    header= 'Fee Structure',
                    row= 5,
                    col= 3,
                    data= table_data
                )

                ctk.CTkLabel(
                    master= receipt_frame,
                    text= 'Signature of Student'
                ).pack(padx= (0, 170), pady= (100, 50) , side= 'right')

                ctk.CTkLabel(
                    master= receipt_frame,
                    text= 'Signature of Principal'
                ).pack(padx= (170, 0), pady= (100, 50) , side= 'left')

        except IndexError as e:
            ShowError('Deposit Fee', 'This enrollment number is not found.')


    def __change_fee_in_db_and_generate_receipt(
        self,
        amount: stringvar,
        fee_deposited: int,
        total_fee: int
    ) -> None:
        """
        Updates the fee deposited by a student in the database.

        This method is called when the user clicks the "Deposit" button after entering the deposit amount. It validates the input, checks if the deposit amount exceeds the remaining fee, and updates the database accordingly.

        Parameters:
            - amount (str): The deposit amount entered by the user.
            - fee_deposited (int): The current amount of fee deposited by the student.
            - total_fee (int): The total fee amount for the student's course.

        Returns:
            - None
        """
        try:
            fee = int(amount.get()) + fee_deposited

            if fee > total_fee:
                ShowError("Fee Deposit", "The amount is greater than remaining fee.")
                return None

        except ValueError:
            ShowError("Fee Deposit", "Add a valid amount.")

        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''UPDATE student
                SET fee_deposited = ?
                WHERE enrollment_no = ?;
                ''',
                [fee, self.enrollment_no.get()]
            )
            connector.db.commit()

        self.__get_fee_info(generate_receipt= True, current_transaction= int(amount.get()))

    # courses
    # add course funcs
    def add_course_gui(
        self,
        event: any = None,
        update: bool = False
    ) -> None:
        """
        Displays the GUI for adding a new course or updating an existing one.

        This method sets up the GUI elements, including labels, entry fields, and buttons, for adding a new course or updating an existing one.

        Parameters:
            - update (bool): If True, indicates that the GUI is for updating an existing course.

        Returns:
            - None
        """
        self.content_remover()
        self.course_id = ctk.StringVar()
        self.course_name = ctk.StringVar()
        self.fee = ctk.StringVar()
        self.course_year = ctk.StringVar(value= '-Select-')

        # add course label
        ctk.CTkLabel(
            master=self,
            text='Course Details',
            font=('arial', 28)
        ).grid(row=0, column=0, padx=10, pady=10)

        # course_id
        if not update:
            self.__create_label_and_entry(
                text='Course ID',
                text_variable=self.course_id,
                row=1
            )

        # course_name
        self.__create_label_and_entry(
            text='Course Name',
            text_variable=self.course_name,
            row=2
        )

        # fee
        self.__create_label_and_entry(
            text='Fee',
            text_variable=self.fee,
            row=3
        )

        # year
        ctk.CTkLabel(
            master=self,
            text='Year'
        ).grid(row=4, column=0, padx=50, pady=5, sticky='w')

        ctk.CTkComboBox(
            master=self,
            values=[str(i) for i in range(1, 5)],
            variable=self.course_year,
            width=120
        ).grid(row=4, column=1, sticky='w')

        if not update:
            # submit button
            self.submit_button = ctk.CTkButton(
                master=self,
                text='Submit',
                width=120,
                command=self.__add_course_submit
            )
            self.submit_button.grid(
                row=5,
                column=3,
                pady=50,
                sticky= 'e'
            )

            # clearbutton
            clear_button = ctk.CTkButton(
                master=self,
                text='Clear',
                width=120,
                command=self.add_course_gui
            )
            clear_button.grid(
                row=5,
                column=1,
                sticky= 'w'
            )
        self.update()

    def __add_course_constraints(
        self,
        course_id: str,
        course_name: str,
        fee: str,
        course_year: str,
        update: bool = False
    ) -> StrOrNone:
        """
        Performs constraints check for adding or updating a course.

        This method checks various constraints, such as the validity of course ID, uniqueness of course ID (for new courses), presence of course name, presence and validity of the fee, and selection of a course year.

        Parameters:
            - course_id (str): The course ID.
            - course_name (str): The course name.
            - fee (str): The course fee.
            - course_year (str): The course year.
            - update (bool): If True, indicates that the constraints check is for updating a course.

        Returns:
            - StrOrNone: If constraints are violated, returns an error message. Otherwise, returns None.
        """
        if not course_id:
            return 'Please enter course id.'

        if not course_id.isnumeric():
            return 'Invalid course id, ID must be a numeric value.'

        if not update:
            with DatabaseConnector() as connector:
                connector.cursor.execute('SELECT course_id FROM courses;')
                courses = connector.cursor.fetchall()

            if int(course_id) in [i[0] for i in courses]:
                return 'This course ID is already present.'

        if not course_name:
            return 'Please enter course name'

        if not fee:
            return 'Please enter fee.'

        if not fee.isnumeric():
            return 'Invalid fee, fee must be a numeric value.'

        if not course_year:
            return 'Please select course year.'

        if not course_year.isnumeric():
            return 'Invalid course year, it must be a numeric value.'

    def __add_course_submit(self) -> None:
        """
        Submits the information for adding a new course to the database.

        This method retrieves course information from the GUI, performs constraints check, and inserts the new course into the database.
        """
        course_id, course_name, fee, course_year = self.__get_info_from_widgets_for_courses()

        if error_msg := self.__add_course_constraints(course_id, course_name, fee, course_year):
            ShowError('Add Course', error_msg)
            return None

        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''INSERT INTO courses(course_id, name, fee, year)
                VALUES(?, ?, ?, ?);
                ''',
                [course_id, course_name, fee, course_year]
            )
            connector.db.commit()
            ShowInfo('Add Course', 'Successfully added the course.')

    def __ask_course_id(self, header_text: str) -> None:
        """
        Asks the user for course id from a combobox.

        Parameters: 
            - header_text (str): text to be displayed onto the header frame.

        Returns:
            - None 
        """

        self.content_remover()
        self.course_var = ctk.StringVar(value= '-Select-')

        if header_text == 'Remove Course':
            command = lambda: ShowWarning(
                title_of_box= 'Remove Course', 
                warning_msg= 'Do you really want to delete the course, the students associated with this course will also be removed, click OK to delete.', 
                command= lambda: self.__remove_course_data_in_db(course_data)
            )

        else:
            command= lambda: self.__get_course_info_for_update(self.course_var)

        id_frame = ctk.CTkFrame(
            master= self, 
            fg_color= ("#f2f2f4", "#4a4a4a")
        )

        id_frame.pack(pady= 5)

        header = ctk.CTkLabel(
            master=id_frame,
            text=header_text,
            font=('arial', 28)
        )

        header.grid(
            row= 0, 
            column= 0,
            padx=10, 
            pady=10,
            columnspan= 2
        )

        with DatabaseConnector() as connector:
            connector.cursor.execute("SELECT course_id, name FROM courses")
            course_data = connector.cursor.fetchall()

        if not course_data:
            ShowInfo(header_text, "No courses are available.")
            return None

        ctk.CTkLabel(
            master=id_frame,
            text='Course'
        ).grid(
            row= 1, 
            column= 0,
            padx=(50, 10), 
            pady=5
        )

        courses = ctk.CTkComboBox(
            master=id_frame,
            values=[f"{i[0]}({i[1]})" for i in course_data],
            variable=self.course_var,
            width=200
        )

        courses.grid(
            row= 1, 
            column= 1,
            padx= (0, 50)
        )

        submit_button = ctk.CTkButton(
            master=id_frame,
            text='Submit',
            command= command,
            width=200
        )
        submit_button.grid(
            row= 2, 
            column= 1,
            pady= (5, 10),
            sticky= 'w'
        )

    # remove course funcs
    def remove_course_gui(self, event: any = None) -> None:
        """
        Displays the GUI for removing a course.

        This method sets up the GUI elements, including labels, combo box for course selection, and a submit button for removing a course. It retrieves course data from the database.
        """
        
        self.__ask_course_id("Remove Course")

    def __remove_course_data_in_db(self, course_data: list) -> None:
        """
        Removes a course and associated students from the database.

        This method is called when the user confirms the removal of a course. It deletes the course and removes associated student records from the database.

        Parameters:
            - course_data (list): List of tuples containing course_id and name.

        Returns:
            - None
        """
        course_id = int(re.findall(r'\d+', self.course_var.get())[0])

        if course_id not in [i[0] for i in course_data]:
            ShowError("Remove Course", "Please select a course from the list.")
            return None

        with DatabaseConnector() as connector:
            connector.cursor.execute(
                'DELETE FROM courses WHERE course_id = ?',
                [course_id]
            )
            connector.db.commit()

            connector.cursor.execute(
                'SELECT enrollment_no FROM student WHERE course_id = ?',
                [course_id]
            )
            result = connector.cursor.fetchall()

            students = [i[0] for i in result]
            connector.cursor.executemany(
                'DELETE FROM student WHERE enrollment_no = ?',
                students
            )

            connector.db.commit()
            ShowInfo("Remove Course", "Successfully deleted the course.")
            self.remove_course_gui()

    # update course funcs
    def update_course_gui(self, event: any = None) -> None:
        """
        Displays the GUI for updating a course.

        This method sets up the GUI elements, including labels, combo box for course selection, and a submit button for updating a course. It retrieves course data from the database.
        """
        
        self.__ask_course_id('Update Course')

    def __get_course_info_for_update(self, course_var: stringvar) -> None:
        """
         Retrieves course information for updating a course and populates the GUI.

        This method is called when the user submits the update course form. It retrieves information for the selected course and populates the GUI fields for editing.

        Parameters:
            - course_var (str): The course variable containing the selected course.

        Returns:
            - None
        """
        with DatabaseConnector() as connector:
            try:
                course_id = int(re.findall(r'\d+', course_var.get())[0])
                connector.cursor.execute(
                    'Select * FROM courses WHERE course_id = ?', [course_id])
                course_data = connector.cursor.fetchall()[0]

            except IndexError:
                ShowError('Update course', 'This course ID is not present.')
                return None

        self.add_course_gui(update=True)
        self.course_id.set(course_data[0])
        self.course_name.set(course_data[1])
        self.fee.set(course_data[2])
        self.course_year.set(course_data[3])

        button = ctk.CTkButton(
            master=self,
            text='Update',
            command=self.__update_course_data_in_db
        )

        button.grid(
            row=5,
            column=3,
            pady=50
        )

    def __update_course_data_in_db(self) -> None:
        """
        Updates course information in the database.

        This method is called when the user clicks the "Update" button after editing course information. It validates the input, updates the course in the database, and displays a success message.
        """
        course_id, course_name, fee, course_year = self.__get_info_from_widgets_for_courses()

        if error_msg := self.__add_course_constraints(course_id, course_name, fee, course_year, update=True):
            ShowError('Add Course', error_msg)
            return None

        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''UPDATE courses 
                SET name = ?, fee = ?, year = ?
                WHERE course_id = ?;
                ''',
                [course_name, fee, course_year, course_id]
            )
            connector.db.commit()
            ShowInfo("Update Course", "Successfully updated the course.")

    # show courses
    def show_all_courses(self, event: any = None) -> None:
        """
        Displays information about all available courses. This method retrieves course data from the database and displays it on the GUI.
        """
        self.content_remover()

        with DatabaseConnector() as connector:
            connector.cursor.execute('SELECT * FROM courses;')
            course_data = connector.cursor.fetchall()

        if not course_data:
            ShowError('Show Courses', 'No courses available.')
            return None

        #create table
        course_data_to_display = [('ID', 'Name', 'Fee', 'Year')]
        course_data_to_display.extend(course_data)

        frame = ctk.CTkFrame(
            master= self
        )

        frame.pack(
            pady= (0, 5), 
            padx= 5,
            fill= 'both',
            expand= True
        )

        self.__create_table(
            master= frame,
            header= 'Course Details',
            row= len(course_data_to_display),
            col= 4,
            data= course_data_to_display
        )

    # library
    # add book
    def add_book_gui(self, event: any = None) -> None:
        """
        Displays the GUI for adding a new book.

        This method sets up the GUI elements, including labels, entry fields, and buttons, for adding a new book. It includes options for selecting the book name, quantity, and associated course.
        """
        self.content_remover()

        self.book_name = ctk.StringVar()
        self.quantity = ctk.StringVar()
        self.isbn = ctk.StringVar()
        self.publisher = ctk.StringVar()
        self.course_id = ctk.StringVar(value= '-Select-')

        ctk.CTkLabel(
            master=self,
            text='Book Details',
            font=('arial', 28)
        ).grid(row=0, column=0, padx=10, pady=10)

        self.__create_label_and_entry(
            text='Book Name',
            text_variable=self.book_name,
            row=1
        )

        self.__create_label_and_entry(
            text='Quantity',
            text_variable=self.quantity,
            row=2
        )

        self.__create_label_and_entry(
            text='ISBN',
            text_variable=self.isbn,
            row=3
        )

        self.__create_label_and_entry(
            text='Publisher',
            text_variable=self.publisher,
            row=4
        )

        with DatabaseConnector() as connector:
            connector.cursor.execute("SELECT course_id, name FROM courses")
            course_data = connector.cursor.fetchall()

        ctk.CTkLabel(
            master=self,
            text='Course'
        ).grid(row=5, column=0, padx=50, pady=5, sticky='w')

        courses = ctk.CTkComboBox(
            master=self,
            values=[f"{i[0]}({i[1]})" for i in course_data],
            variable=self.course_id,
            width=140
        )

        courses.grid(
            row=5,
            column=1,
            sticky='w'
        )

        submit_button = ctk.CTkButton(
            master=self,
            text='Submit',
            command=self.__add_book_submit
        )
        submit_button.grid(
            row=6,
            column=3,
            pady=50,
            sticky= 'e'
        )

        clear_button = ctk.CTkButton(
            master=self,
            text='Clear',
            command=self.add_book_gui
        )

        clear_button.grid(
            row=6,
            column=1,
            sticky= 'w'
        )

    def __add_book_constraints(
        self,
        book_name: StrOrNone,
        quantity: StrOrNone,
        course_id: StrOrNone,
        isbn: StrOrNone,
        publisher: StrOrNone
    ) -> StrOrNone:
        """
        Performs constraints check for adding a book.

        This method checks various constraints, such as the presence of book name, quantity, and a valid course ID.

        Parameters:
            book_name (StrOrNone): The name of the book.
            quantity (StrOrNone): The quantity of books.
            course_id (StrOrNone): The course ID associated with the book.
            isbn (StrOrNone): The ISBN number of the book.
            publisher (StrOnNone): The publisher of the book.

        Returns:
            StrOrNone: If constraints are violated, returns an error message. Otherwise, returns None.
        """
        if not book_name:
            return 'Please enter book name.'

        if not quantity:
            return 'Please enter quantity of books.'

        if not quantity.isnumeric():
            return 'Invalid quantity of books, it must be a numeric value.'

        if not course_id:
            return 'Please select the course ID.'
        
        if not isbn:
            return 'Please enter ISBN number.'
        
        if not isbn.isnumeric():
            return 'Inavlid ISBN, it must be a numeric value.'
        
        if len(isbn) != 13:
            return 'Invalid ISBN, it must contain 13 digits.'
        
        if not publisher:
            return 'Please enter name of Publisher.'
        

        with DatabaseConnector() as connector:
            connector.cursor.execute('SELECT course_id FROM courses;')
            courses = connector.cursor.fetchall()

        if int(course_id) not in [i[0] for i in courses]:
            return 'Please select a course ID from the list.'

    def __add_book_submit(self) -> None:
        """
        Submits information for adding a new book to the database.

        This method retrieves book information from the GUI, performs constraints check, and inserts the new book into the database.
        """
        book_name = self.__valueGetter(self.book_name.get())
        quantity = self.__valueGetter(self.quantity.get())
        course_var = self.__valueGetter(self.course_id.get())
        course_id = re.findall(r'\d+', course_var)[0]
        isbn = self.__valueGetter(self.isbn.get())
        publisher = self.__valueGetter(self.publisher.get())

        if error_msg := self.__add_book_constraints(book_name, quantity, course_id, isbn, publisher):
            ShowError("Add Book", error_msg)
            return None

        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''INSERT INTO books(name, quantity, course_id, isbn, publisher)
                VALUES(?, ?, ?, ?, ?);
                ''',
                [book_name, quantity, course_id, isbn, publisher]
            )
            connector.db.commit()

        ShowInfo('Add Book', 'Successfully added the Book.')

    # remove Book
    def remove_book_gui(self, event: any = None) -> None:
        """
        Displays the GUI for removing a book.

        This method sets up the GUI elements, including labels, entry field for book ID, and a submit button for removing a book. It includes a warning about the potential impact on student records if the book is currently borrowed.
        """
        self.content_remover()
        book_id = ctk.StringVar()

        self.content_remover()

        id_frame = ctk.CTkFrame(
            master= self,
            fg_color= ("#f2f2f4", "#4a4a4a")
        )

        id_frame.pack(pady= 5)

        header = ctk.CTkLabel(
            master=id_frame,
            text= 'Remove Book',
            font=('arial', 28)
        )
        header.grid(
            row= 0, 
            column= 0,
            padx=10,
            pady=10,
            columnspan= 2
        )

        id_label = ctk.CTkLabel(
            master=id_frame,
            text='Book ID',
            justify='left'
        )
        id_label.grid(
            row= 1, 
            column= 0,
            padx= (50, 10), 
            pady=5
        )

        entry = ctk.CTkEntry(
            master=id_frame,
            textvariable=book_id,
            width=200
        )
        entry.grid(
            row= 1,
            column= 1,
            padx= (0, 50)
        )

        button = ctk.CTkButton(
            master= id_frame,
            text=' Submit',
            command= lambda: self.__remove_book_data_in_db(book_id),
            width= 200
        )

        button.grid(
            row= 2, 
            column= 1,
            pady=(5, 10),
            sticky= 'w'
        )

    def __remove_book_data_in_db(self, book_id: stringvar) -> None:
        """
        Removes book data from the database.

        This method is called when the user confirms the removal of a book. It deletes the book from the 'books' table and removes any associated records from the 'books_lended' table.

        Parameters:
            book_id (stringvar): The ID of the book to be removed.
        """
        with DatabaseConnector() as connector:
            connector.cursor.execute('SELECT book_id FROM books;')
            all_book_ids = connector.cursor.fetchall()

            book_id = int(book_id.get())

            if book_id in [i[0] for i in all_book_ids]:
                connector.cursor.execute(
                    'DELETE FROM books WHERE book_id = ?', [book_id])
                connector.db.commit()

                connector.cursor.execute(
                    'DELETE FROM books_lended WHERE book_id = ?', [book_id])
                connector.db.commit()

                ShowInfo('Remove Book', 'Successfully removed the book.')

            else:
                ShowError('Remove Book', 'This book ID is not found.')

    # book list
    def show_books(self, event: any = None) -> None:
        """
        Displays information about all available books. This method retrieves book data from the database and displays it on the GUI.
        """
        self.content_remover()

        with DatabaseConnector() as connector:
            connector.cursor.execute('SELECT * FROM books;')
            book_data = connector.cursor.fetchall()

        if not book_data:
            ShowError('Book List', 'No Books available.')
            return None

        #create table
        frame = ctk.CTkFrame(
            master= self
        )

        frame.pack(
            pady= (0, 5), 
            padx= 5,
            fill= 'both',
            expand= True
        )

        book_data_to_display = [('Book ID', 'Name', 'Quantity', 'Course ID', 'ISBN', 'Publisher')]
        book_data_to_display.extend(book_data)

        self.__create_table(
            master= frame,
            header= 'Books List',
            row= len(book_data_to_display),
            col= 6,
            data= book_data_to_display,
            word_wrap_length= 250
        )


    # lend book
    def lend_book(self, event: any = None) -> None:
        self.__ask_enrollment(
            label_text='Lend Book to...',
            command=self.__lend_book_gui
        )

    def __lend_book_gui(self) -> None:
        """
        Displays the GUI for lending books to students.

        This method retrieves the course ID of the student based on the provided enrollment number and then fetches all available books related to that course for lending. It sets up the GUI elements, including labels, checkboxes for book selection, and a submit button.
        """
        enrollment_no = self.enrollment_no.get()
        if not enrollment_no.isnumeric():
            ShowError('Lend Book', 'Invalid enrollment number, it must be a numeric value.')
            return None

        with DatabaseConnector() as connector:
            # getting course_id of student
            connector.cursor.execute(
                '''SELECT course_id 
                FROM student
                WHERE enrollment_no = ?;
                ''',
                [enrollment_no]
            )
            try:
                course_id = connector.cursor.fetchall()[0][0]

            except IndexError:
                ShowError('Lend Book', 'This enrollment no is not found.')

            # getting all books related to the course
            connector.cursor.execute(
                '''SELECT book_id, name, publisher
                FROM books
                WHERE course_id = ? AND quantity > 0;
                ''',
                [course_id]
            )
            all_books_related_to_course = connector.cursor.fetchall()

        if not all_books_related_to_course:
            ShowError('Lend Book', 'No books related to this course.')
            return

        self.content_remover()

        ctk.CTkLabel(
            master=self,
            text='Lend Book',
            font=('arial', 28)
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            master=self,
            text='Select books to lend:'
        ).grid(row=1, column=0, padx=5)

        index = self.__create_checkbox_from_list(all_books_related_to_course)

        submit_button = ctk.CTkButton(
            master=self,
            text='Submit',
            command=self.__lend_book_submit
        )
        submit_button.grid(
            row=index + 3,
            column=1,
            pady=20,
            sticky='e'
        )

    def __lend_book_submit(self) -> None:
        """
        Submits information for lending books to a student.

        This method retrieves the selected books from the GUI checkboxes and updates the 'books_lended' table with the enrollment number and book IDs. It also updates the 'books' table to decrement the quantity of the lent books.
        """
        enrollment_no = self.enrollment_no.get()

        selected_books = []
        for book_id, stringvar in self.stringvars_for_checkbox.items():
            if stringvar.get() == 'on':
                selected_books.append(book_id)

        if not selected_books:
            ShowError('Lend Book', 'Please select atleast one book.')
            return None

        with DatabaseConnector() as connector:
            connector.cursor.executemany(
                'INSERT INTO books_lended(enrollment_no, book_id) VALUES(?, ?)',
                [(enrollment_no, book_id) for book_id in selected_books]
            )

            connector.cursor.executemany(
                '''UPDATE books
                SET quantity = quantity - 1
                WHERE book_id = ?;
                ''',
                [(book_id,) for book_id in selected_books]
            )

            connector.db.commit()

        date_time = datetime.now()
        today_date = date_time.strftime("%d/%m/%Y")

        ShowInfo(
            'Lend Book', 
            f'Successfully lended the books.\nTo enrollment number : {enrollment_no}\n On: {today_date}.\nBook IDs: {', '.join(str(id) for id in selected_books)}'
        )
        self.content_remover()

    # return book
    def return_book(self, event: any = None) -> None:
        self.__ask_enrollment(
            label_text='Return Book from...',
            command=self.__return_book_gui
        )

    def __return_book_gui(self) -> None:
        """
        Displays the GUI for returning books by a student.

        This method retrieves the enrollment number of the student, selects all books that have been lended to the student, and sets up the GUI elements for book selection and a submit button.
        """
        enrollment_no = self.enrollment_no.get()
        if not enrollment_no.isnumeric():
            ShowError(
                'Lend Book', 'Invalid enrollment number, it must be a numeric value.')
            return None

        with DatabaseConnector() as connetor:
            # selecting all books lended to the student
            connetor.cursor.execute(
                '''
                SELECT book_id, name, publisher
                FROM books
                WHERE book_id IN (SELECT book_id FROM books_lended WHERE enrollment_no = ?);
                ''',
                [enrollment_no]
            )

            lended_books = connetor.cursor.fetchall()

        if not lended_books:
            ShowError('Return Book', 'No books lended to this student.')
            return None

        self.content_remover()

        ctk.CTkLabel(
            master=self,
            text='Return Book',
            font=('arial', 28)
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            master=self,
            text='Select books to Return:'
        ).grid(row=1, column=0, padx=5)

        index = self.__create_checkbox_from_list(lended_books)

        submit_button = ctk.CTkButton(
            master=self,
            text='Submit',
            command=self.__return_book_submit
        )
        submit_button.grid(
            row=index + 3,
            column=1,
            pady=20,
            sticky='e'
        )

    def __return_book_submit(self) -> None:
        """
        Submits information for returning books by a student.

        This method retrieves the selected books from the GUI checkboxes and updates the 'books_lended' table to remove the corresponding records. It also updates the 'books' table to increment the quantity of the returned books.
        """
        enrollment_no = self.enrollment_no.get()

        selected_books = []
        for book_id, stringvar in self.stringvars_for_checkbox.items():
            if stringvar.get() == 'on':
                selected_books.append(book_id)

        if not selected_books:
            ShowError('Lend Book', 'Please select atleast one book.')
            return None

        with DatabaseConnector() as connector:
            connector.cursor.executemany(
                '''DELETE FROM books_lended
                WHERE enrollment_no = ? AND book_id = ?;
                ''',
                [(enrollment_no, book_id) for book_id in selected_books]
            )

            connector.cursor.executemany(
                '''
                UPDATE books
                SET quantity = quantity + 1
                WHERE book_id = ?;
                ''',
                [(book_id,) for book_id in selected_books]
            )

            connector.db.commit()

        date_time = datetime.now()
        today_date = date_time.strftime("%d/%m/%Y")

        ShowInfo(
            'Return Book', 
            f'Successfully returned the books.\nBy enrollment number : {enrollment_no}\n On: {today_date}.\nBook IDs: {', '.join(str(id) for id in selected_books)}'
        )
        self.content_remover()

    # update stock
    def update_stock_gui(self, event: any = None) -> None:
        """
        Displays the GUI for updating the stock of books.

        This method sets up the GUI elements for updating the stock, including input fields for the book ID and the quantity by which to update the stock, and a submit button.
        """
        self.content_remover()

        ctk.CTkLabel(
            master=self,
            text='Update Stock',
            font=('arial', 28)
        ).grid(row=0, column=0, padx=10, pady=10)

        book_id = ctk.StringVar()
        self.__create_label_and_entry(
            text='Book ID',
            text_variable=book_id,
            row=1,
            columnspan=1,
            width=120
        )

        quantity = ctk.StringVar()
        self.__create_label_and_entry(
            text='Quantity by which to update',
            text_variable=quantity,
            row=2,
            columnspan=1,
            width=120
        )

        submit_button = ctk.CTkButton(
            master=self,
            text='Submit',
            command=lambda: self.__update_stock_submit(book_id, quantity),
            width=120
        )
        submit_button.grid(
            row=3,
            column=1,
            pady=20
        )

    def __update_stock_submit(
        self,
        book_id: stringvar,
        quantity: stringvar
    ) -> None:
        """
        Submits information for updating the stock of a book.

        This method validates the input values, checks if the book ID is present in the database, and updates the 'books' table to increment the quantity of the specified book.

        Parameters:
            - book_id (str): The book ID.
            - quantity (str): The quantity by which to update the stock.

        Returns:
            - None
        """
        quantity_value = self.__valueGetter(quantity.get())
        book_id_value = self.__valueGetter(book_id.get())

        error_msg = None

        if not quantity_value:
            error_msg = 'Please enter quantity.'

        elif not book_id_value:
            error_msg = 'Please enter book ID'

        elif not quantity_value.isnumeric():
            error_msg = 'Invalid quantity, it must be a numeric value.'

        elif not book_id_value.isnumeric():
            error_msg = 'Invalid book ID, it must be a numeric value.'

        if error_msg:
            ShowError('Update Stock', error_msg)
            return None

        with DatabaseConnector() as connector:
            connector.cursor.execute(
                'SELECT book_id FROM books;'
            )
            all_book_ids = [i[0] for i in connector.cursor.fetchall()]

            if int(book_id_value) not in all_book_ids:
                ShowError('Update Stock', 'This book ID is not present.')
                return None

            connector.cursor.execute(
                '''
                UPDATE books
                SET quantity = quantity + ?
                WHERE book_id = ?;
                ''',
                [quantity_value, book_id_value]
            )
            connector.db.commit()
            ShowInfo('Update Stock', 'Successfully updated the stock.')

    # settings
    def settings_gui(self, event: any = None) -> None:
        """
        Display the settings GUI with options to configure various settings, including theme, default tab, shortcuts, and more.
        """

        self.content_remover()

        # getting settings from db
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                SELECT value
                FROM settings
                WHERE setting = "default_tab" OR setting = "theme";
                '''
            )
            result = connector.cursor.fetchall()

        default_tab = result[0][0]
        theme = result[1][0]

        # stringvars
        default_tab_var = ctk.StringVar(value=default_tab)
        theme_var = ctk.StringVar(value=theme)

        # settings label
        ctk.CTkLabel(
            master=self,
            text="Settings",
            font=('arial', 28)
        ).pack(pady=5, padx=5)

        # theme
        theme_frame = self.__create_frame_and_assign_label(
            header='Theme',
            description='Select theme of College Management System.'
        )
        theme_frame.pack(
            fill='x',
            expand=True,
            pady=5,
            padx=5
        )

        # label for light
        ctk.CTkLabel(
            master=theme_frame,
            text='Light'
        ).grid(row=1, column=0, sticky='e', padx=5)

        # theme switch
        theme_switch = ctk.CTkSwitch(
            master=theme_frame,
            text='  Dark',
            command=lambda: self.__update_theme_and_set_to_db(theme_var),
            variable=theme_var,
            onvalue='dark',
            offvalue='light'
        )

        theme_switch.grid(
            row=1,
            column=1,
            sticky='w',
            padx=5
        )

        # default tab
        default_tab_frame = self.__create_frame_and_assign_label(
            header='Default Tab on Startup',
            description='Default tab to be selected on the start of program.'
        )

        default_tab_frame.pack(
            fill='x',
            expand=True,
            pady=5,
            padx=5
        )

        # radiobuttons
        ctk.CTkRadioButton(
            master=default_tab_frame,
            text='Accounts',
            variable=default_tab_var,
            value='Accounts',
            command=lambda: self.__update_default_tab_in_db(
                default_tab_var.get())
        ).grid(row=1, column=0, padx=5, pady=(0, 5))

        ctk.CTkRadioButton(
            master=default_tab_frame,
            text='Library',
            variable=default_tab_var,
            value='Library',
            command=lambda: self.__update_default_tab_in_db(
                default_tab_var.get())
        ).grid(row=1, column=2, pady=(0, 5))

        ctk.CTkRadioButton(
            master=default_tab_frame,
            text='Courses',
            variable=default_tab_var,
            value='Courses',
            command=lambda: self.__update_default_tab_in_db(
                default_tab_var.get())
        ).grid(row=2, column=0, padx=5, pady=(0, 5))

        ctk.CTkRadioButton(
            master=default_tab_frame,
            text='Excel',
            variable=default_tab_var,
            value='Excel',
            command=lambda: self.__update_default_tab_in_db(
                default_tab_var.get())
        ).grid(row=2, column=2, pady=(0, 5))

        #admin settings
        if self.user == 'Admin':
            self.__create_category_label('Admin')
            # Remove all data
            remove_all_data_frame = self.__create_frame_and_assign_label(
                header='Remove all data',
                description='Click "Clear" to erase all data; backup important information using the Export feature.'
            )

            remove_all_data_frame.pack(
                fill='x',
                expand=True,
                pady=5,
                padx=5
            )

            remove_all_data_button = ctk.CTkButton(
                master=remove_all_data_frame,
                text="Clear",
                width=100,
                command=lambda: ShowWarning(
                    title_of_box="Remove all data",
                    warning_msg='Do you really want to erase all the data? Click OK to continue.',
                    command= self.__remove_all_data_from_db
                )
            )

            remove_all_data_button.grid(
                row=1,
                column=0,
                padx=5,
                pady=5,
                sticky='w'
            )

            #remove user button
            remove_user_frame = self.__create_frame_and_assign_label(
                header= 'Remove User',
                description= 'Select a user from the dropdown and click "Remove" to remove the user.'
            )

            remove_user_frame.pack(
                fill='x',
                expand=True,
                pady=5,
                padx=5
            )

            with DatabaseConnector() as connector:
                connector.cursor.execute(
                    '''
                    SELECT username 
                    FROM user
                    WHERE username != "Admin";
                    '''
                )

                users = [user[0] for user in connector.cursor.fetchall()]

            selected_user = ctk.StringVar(value= '-Select-')
            users_combo_box = ctk.CTkComboBox(
                master= remove_user_frame,
                values= users,
                variable= selected_user
            )

            users_combo_box.grid(
                row= 1,
                column= 1,
                padx= 5,
                pady= 5
            )

            remove_button = ctk.CTkButton(
                master= remove_user_frame,
                text= 'Remove',
                command= lambda: ShowWarning(
                    title_of_box= 'Remove User', 
                    warning_msg= 'Do you really want to remove this user.',
                    command= lambda: self.__remove_user(user= selected_user.get())
                )
            )

            remove_button.grid(
                row= 1,
                column= 2,
                padx= 5, 
                pady= 5
            )

        # shortcuts
        ctk.CTkLabel(
            master=self,
            text="Shortcuts",
            font=('arial', 28)
        ).pack(pady=(30, 5), padx=5)

        # tab shifting shortcuts
        self.__create_category_label('Tab Shifting', pady=5)

        self.__create_shortcut_frame(
            name='Accounts Tab',
            shortcut='ctrl + 1'
        )

        self.__create_shortcut_frame(
            name='Library Tab',
            shortcut='ctrl + 2'
        )

        self.__create_shortcut_frame(
            name='Courses Tab',
            shortcut='ctrl + 3'
        )

        self.__create_shortcut_frame(
            name='Excel Tab',
            shortcut='ctrl + 4'
        )

        # accounts related shortcuts
        self.__create_category_label('Accounts related shortcuts')

        self.__create_shortcut_frame(
            name='New Admission',
            shortcut='ctrl + shift + N'
        )

        self.__create_shortcut_frame(
            name='Fetch Student Data',
            shortcut='ctrl + f'
        )

        self.__create_shortcut_frame(
            name='Update Student Data',
            shortcut='ctrl + u'
        )

        self.__create_shortcut_frame(
            name='Deposit Fee',
            shortcut='ctrl + d'
        )

        self.__create_shortcut_frame(
            name='Remove Student',
            shortcut='ctrl + delete'
        )

        # library related shortcuts
        self.__create_category_label('Library related shortcuts')

        self.__create_shortcut_frame(
            name='Lend Book',
            shortcut='ctrl + l'
        )

        self.__create_shortcut_frame(
            name='Return Book',
            shortcut='ctrl + r'
        )

        self.__create_shortcut_frame(
            name='Books List',
            shortcut='ctrl + b'
        )

        self.__create_shortcut_frame(
            name='Add Book',
            shortcut='ctrl + shift + A'
        )

        self.__create_shortcut_frame(
            name='Remove Book',
            shortcut='ctrl + shift + R'
        )

        self.__create_shortcut_frame(
            name='Update Stock',
            shortcut='ctrl + shift + U'
        )

        # courses related shortcuts
        self.__create_category_label('Courses related shortcuts')

        self.__create_shortcut_frame(
            name='Add Course',
            shortcut='ctrl + alt + c'
        )

        self.__create_shortcut_frame(
            name='Remove Course',
            shortcut='ctrl + alt + r'
        )

        self.__create_shortcut_frame(
            name='Update Course',
            shortcut='ctrl + alt + u'
        )

        self.__create_shortcut_frame(
            name='Show All Courses',
            shortcut='ctrl + alt + s'
        )

        # excel related shortcuts
        self.__create_category_label(
            'Exporting and Importing shortcuts')

        self.__create_shortcut_frame(
            name='Export',
            shortcut='ctrl + shift + X'
        )

        self.__create_shortcut_frame(
            name='Import',
            shortcut='ctrl + insert'
        )

        self.__create_category_label('Settings')

        self.__create_shortcut_frame(
            name='Settings',
            shortcut='ctrl + `'
        )

    @staticmethod
    def __update_theme_and_set_to_db(theme: stringvar) -> None:
        """
        Update the theme setting in the database and apply the selected theme.

        Parameters:
            - theme (ctk.StringVar): The StringVar holding the theme value.

        Returns:
            - None
        """
        
        theme = theme.get()
        ctk.set_appearance_mode(theme)

        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                UPDATE settings
                SET value = ?
                WHERE setting = "theme";
                ''',
                [theme]
            )

            connector.db.commit()

    def __create_frame_and_assign_label(
        self,
        header: str,
        description: str,
        height_of_frame: int = 200
    ) -> ctkFrame:
        """
        Create a frame with a header label and a description label.

        Parameters:
            - header (str): The header text.
            - description (str): The description text.
            - height_of_frame (int): The height of the frame (200 by default).

        Returns:
            - ctk.CTkFrame: The created frame.
        """

        frame = ctk.CTkFrame(
            master=self,
            width=600,
            height=height_of_frame,
            fg_color=("#f2f2f4", "#4a4a4a")
        )

        header_label = ctk.CTkLabel(
            master=frame,
            text=header + ':',
            font=('arial', 14, 'bold')
        )

        header_label.grid(
            row=0,
            column=0,
            pady=5,
            padx=5,
            sticky='w'
        )

        description_label = ctk.CTkLabel(
            master=frame,
            text=description
        )

        description_label.grid(
            row=0,
            column=1,
            pady=5,
            padx=5,
            sticky='w',
            columnspan=4
        )

        return frame

    def __update_default_tab_in_db(self, tab: str) -> None:
        """
        Update the default tab setting in the database.

        Parameters:
            - tab (str): The selected default tab.

        Returns:
            - None
        """
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                UPDATE settings
                SET value = ?
                WHERE setting = "default_tab";
                ''',
                [tab]
            )

            connector.db.commit()

    def __create_shortcut_frame(self, name: str, shortcut: str) -> None:
        """
        Create a frame to display a shortcut with a name and corresponding key combination.

        Parameters:
            - name (str): The name of the shortcut.
            - shortcut (str): The key combination for the shortcut.

        Returns:
            - None
        """
        shortcut_frame = self.__create_frame_and_assign_label(
            header=name,
            description=shortcut
        )

        shortcut_frame.pack(
            fill='x',
            expand=True,
            pady=5,
            padx=5,
            side='top',
            anchor='w'
        )

    def __create_category_label(
        self,
        text: str,
        pady: int | tuple[int] = (20, 5)
    ) -> None:
        """
        Create a label for a category of shortcuts.

        Parameters:
            - text (str): The text of the label.
            - pady (int or tuple): Vertical padding for the label.

        Returns:
            - None
        """
        ctk.CTkLabel(
            master=self,
            text=text,
            font=('arial', 18)
        ).pack(padx=5, pady=pady, side='top', anchor='w')

    @staticmethod
    def __remove_all_data_from_db() -> None:
        """
        Removes all data from the student, courses, books, books_lended tables and resets the auto_increment of student and books.
        """
        with DatabaseConnector() as connector:
            # Delete data from tables
            tables_to_delete = ['student', 'courses', 'books', 'books_lended']
            for table in tables_to_delete:
                connector.cursor.execute(f'DELETE FROM {table};')

            # Reset AUTO_INCREMENT for specific tables
            connector.cursor.executemany('UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME=?;', [('student',), ('books',)])

            connector.db.commit()

        ShowInfo('Erased', 'Successfully erased all the data.')

    def __remove_user(self, user: str) -> None:
        if user == '-Select-':
            ShowError(error_msg= 'Please select user.')
            return 
        
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                DELETE FROM user
                WHERE username = ?;
                ''',
                (user,)
            )
            connector.db.commit()

        ShowInfo('Remove User', 'Successfully removed the user.')
        self.settings_gui()

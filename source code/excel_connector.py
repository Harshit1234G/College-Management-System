import pandas as pd
import numpy as np
import customtkinter as ctk
from PIL import ImageTk
import os
from tkinter.filedialog import askdirectory, askopenfilename
from database_connector import DatabaseConnector
from messagebox import ShowInfo, ShowError

type dataframe = pd.DataFrame


class ExportToExcel(ctk.CTkToplevel):
    """
    customtkinter Toplevel window for exporting data to an Excel file.

    Attributes:
        - `current_directory` (str): The current working directory.
        - `description_label` (ctk.CTkLabel): Label widget displaying export instructions.
        - `folder_path` (ctk.StringVar): StringVar storing the selected folder path.
        - `entry` (ctk.CTkEntry): Entry widget for displaying/editing the folder path.
        - `browse_button` (ctk.CTkButton): Button for opening a folder selection dialog.
        - `student_var_for_checkbox` (ctk.StringVar): StringVar for the Students checkbox.
        - `courses_var_for_checkbox` (ctk.StringVar): StringVar for the Courses checkbox.
        - `books_var_for_checkbox` (ctk.StringVar): StringVar for the Books checkbox.
        - `books_lended_var_for_checkbox` (ctk.StringVar): StringVar for the Books Lended checkbox.
        - `export_button` (ctk.CTkButton): Button for triggering the data export process.

    Methods:
        `__init__(self, *args, **kwargs):`
            Initializes the ExportToExcel instance.

        `__open_folder(self) -> None:`
            Opens a folder selection dialog and sets the chosen path in the entry widget.

        `__export_data(self) -> None:`
            Exports selected data to an Excel file based on checkbox choices.

    Example:
        ```
        #directly call the class or create and object in the Menu class.
        ExportToExcel()
        ```
    """
    current_directory = os.getcwd()

    def __init__(self, *args, **kwargs):
        """
        Initializes the ExportToExcel instance. Creates the GUI for Exporting TopLevel Window.
        """
        super().__init__(*args, **kwargs)

        # basic attributes
        self.geometry("500x415")
        self.resizable(False, False)
        self.title("Export to Excel")

        # changing icon
        self.imagepath = ImageTk.PhotoImage(
            file=os.path.join('icons', 'app.png'))
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, self.imagepath))

        # gui of toplevel
        # Label
        description_text = '''
Steps to export data in the form of Excel file:

Step 1 - Select a folder (by default, it is set to the current working directory; click Browse to change it).

Step 2 - Choose the data to export from the checkbox provided (by default, all are selected).

Step 3 - Click Export.

After clicking Export, an Excel file will be created in the selected folder, containing data as per your selection in different sheets.'''
        self.description_label = ctk.CTkLabel(
            master=self,
            text=description_text,
            wraplength=450,
            justify='left'
        )
        self.description_label.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky='w',
            padx=(30, 0)
        )

        # Entry widget for path
        self.folder_path = ctk.StringVar(value=self.current_directory)

        self.entry = ctk.CTkEntry(
            master=self,
            textvariable=self.folder_path,
            width=340
        )
        self.entry.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=(30, 0),
            pady=(20, 0)
        )

        # browse button
        self.browse_button = ctk.CTkButton(
            master=self,
            text='Browse...',
            width=97,
            command=self.__open_folder
        )
        self.browse_button.grid(
            row=2,
            column=2,
            padx=5,
            pady=(20, 0)
        )

        # checkboxes
        self.student_var_for_checkbox = ctk.StringVar(value='on')
        self.courses_var_for_checkbox = ctk.StringVar(value='on')
        self.books_var_for_checkbox = ctk.StringVar(value='on')
        self.books_lended_var_for_checkbox = ctk.StringVar(value='on')

        ctk.CTkLabel(
            master=self,
            text='Select data to export...'
        ).grid(row=3, column=0, pady=(13, 7))

        ctk.CTkCheckBox(
            master=self,
            text='Students',
            variable=self.student_var_for_checkbox,
            onvalue='on',
            offvalue='off'
        ).grid(row=4, column=0)

        ctk.CTkCheckBox(
            master=self,
            text='Courses',
            variable=self.courses_var_for_checkbox,
            onvalue='on',
            offvalue='off'
        ).grid(row=4, column=1)

        ctk.CTkCheckBox(
            master=self,
            text='Books',
            variable=self.books_var_for_checkbox,
            onvalue='on',
            offvalue='off'
        ).grid(row=5, column=0, pady=10)

        ctk.CTkCheckBox(
            master=self,
            text='Books Lended',
            variable=self.books_lended_var_for_checkbox,
            onvalue='on',
            offvalue='off'
        ).grid(row=5, column=1, padx=(11, 0))

        # export button
        self.export_button = ctk.CTkButton(
            master=self,
            text='Export',
            width=97,
            command=self.__export_data
        )

        self.export_button.grid(
            row=6,
            column=2,
            padx=5
        )

        # lifting toplevel
        self.after(100, self.lift)

    def __open_folder(self) -> None:
        """
        Opens a folder selection dialog and sets the chosen path in the entry widget.
        """
        path = askdirectory(
            initialdir=self.current_directory,
            mustexist=True,
            title="Select Folder"
        )
        self.folder_path.set(path)
        self.after(100, self.lift)

    def __export_data(self) -> None:
        """
        Exports selected data to an Excel file based on checkbox choices.
        """
        # getting all the values from checkboxes and append them to list if they are on
        list_of_tables_to_export: list[str] = []

        if self.student_var_for_checkbox.get() == 'on':
            list_of_tables_to_export.append('student')

        if self.courses_var_for_checkbox.get() == 'on':
            list_of_tables_to_export.append('courses')

        if self.books_var_for_checkbox.get() == 'on':
            list_of_tables_to_export.append('books')

        if self.books_lended_var_for_checkbox.get() == 'on':
            list_of_tables_to_export.append('books_lended')

        if not list_of_tables_to_export:
            ShowError(
                'Error',
                'Select atleast one option.'
            )
            return None

        header_dict = {
            'student': ['Enrollment Number', 'Name', 'Date of Birth', 'Address', 'Mobile no', 'Email', 'Year of Admission', 'Age', 'Gender', 'Pincode', 'Course ID', 'Father Name', '10th Percentage', '12th Percentage', 'Fee Deposited'],
            'courses': ['Course ID', 'Course Name', 'Fee', 'Year'],
            'books': ['Book ID', 'Name', 'Quantity', 'Course ID', 'ISBN', 'Publisher'],
            'books_lended': ['Enrollment Number', 'Book ID']
        }

        self.export_button.configure(text='Exporting...', state='disabled')

        # retrieving data from database according to the tables and writing them to excel file
        with DatabaseConnector() as connector:

            # creating a excel writer object
            excel_file_path = os.path.join(
                self.folder_path.get(), "Exported Data.xlsx")
            with pd.ExcelWriter(excel_file_path) as writer:

                # one by one retreiving data and writing to separate excel file sheets
                for table in list_of_tables_to_export:
                    try:
                        connector.cursor.execute(f"SELECT * FROM {table};")
                        data = connector.cursor.fetchall()

                        # creating dataframe and writing it to excel
                        data_frame = pd.DataFrame(data)
                        data_frame.to_excel(
                            excel_writer=writer,
                            sheet_name=table,
                            header=header_dict[table],
                            index=False
                        )
                    
                    except ValueError:
                        continue

        self.destroy()
        ShowInfo(
            'Export Completed',
            f'Successfully exported the data to {excel_file_path}'
        )


class ImportFromExcel(ctk.CTkToplevel):
    """
    customtkinter Toplevel window for importing data from an Excel file into a database.

    Attributes:
        - `file_path` (ctk.StringVar): StringVar storing the selected Excel file path.
        - `file_entry` (ctk.CTkEntry): Entry widget for displaying/editing the Excel file path.
        - `browse_button` (ctk.CTkButton): Button for opening a file selection dialog.
        - `sheet_name` (ctk.StringVar): StringVar storing the selected sheet name.
        - `frame_for_radio_buttons` (ctk.CTkFrame): Frame for radio buttons to select the type of data to import.
        - `radio_button_selection` (ctk.StringVar): StringVar storing the selected radio button value.
        - `must_contain_label` (ctk.CTkLabel): Label displaying constraints and required columns for the selected data.
        - `import_button` (ctk.CTkButton): Button for triggering the data import process.

    Methods:
        `__init__(self, *args, **kwargs):`
            Initializes the ImportFromExcel instance.

        `__open_file(self) -> None:`
            Opens a file selection dialog and sets the chosen Excel file path in the entry widget.

        `__create_label_from_list_in_grid_form(self, columns: list[str]) -> str:`
            Creates a formatted label text from a list of column names for display.

        `__update_label_according_to_radio_button(self) -> None:`
            Updates the must_contain_label based on the selected radio button.

        `__enable_import_button(self) -> None:`
            Enables the Import button.

        `__import_data(self) -> None:`
            Imports data from the selected Excel file into the database based on user choices.

        `__write_data_in_db_for_student(self, df: pd.DataFrame) -> None:`
            Writes student data from DataFrame to the database.

        `__write_data_in_db_for_courses(self, df: pd.DataFrame) -> None:`
            Writes courses data from DataFrame to the database.

        `__write_data_in_db_for_books(self, df: pd.DataFrame) -> None:`
            Writes books data from DataFrame to the database.

    Example:
        ```
        #directly call the class or create and object in the Menu class.
        ImportToExcel()
        ```
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the ImportFromExcel instance. Creates the GUI for Importing TopLevel Window.
        """
        super().__init__(*args, **kwargs)

        # basic attributes
        self.geometry("500x600")
        self.resizable(False, False)
        self.title("Import from Excel")

        # changing icon
        self.imagepath = ImageTk.PhotoImage(
            file=os.path.join('icons', 'app.png'))
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, self.imagepath))

        # asking for file path
        ctk.CTkLabel(
            master=self,
            text="Enter or browse the excel file path."
        ).grid(row=0, column=0, columnspan=2, sticky='w', padx=30, pady=(15, 0))

        self.file_path = ctk.StringVar()

        self.file_entry = ctk.CTkEntry(
            master=self,
            textvariable=self.file_path,
            width=340
        )
        self.file_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=(30, 0),
            pady=(3, 0)
        )

        # browse button
        self.browse_button = ctk.CTkButton(
            master=self,
            text='Browse...',
            width=97,
            command=self.__open_file
        )
        self.browse_button.grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

        # asking sheet name
        ctk.CTkLabel(
            master=self,
            text='Enter the name of sheet (by default it is Sheet1)'
        ).grid(row=2, column=0, padx=30, pady=(15, 5), sticky='w', columnspan=2)

        self.sheet_name = ctk.StringVar(value='Sheet1')
        ctk.CTkEntry(
            master=self,
            textvariable=self.sheet_name,
            width=340
        ).grid(row=3, column=0, padx=(30, 0), sticky='w', columnspan=2)

        # radio buttons for which type of data to import (basically in which table to write the data from excel)
        ctk.CTkLabel(
            master=self,
            text="Select the type of data that you want to insert"
        ).grid(row=4, column=0, columnspan=2, sticky='w', pady=(20, 5), padx=30)

        self.frame_for_radio_buttons = ctk.CTkFrame(
            master=self,
            width=440
        )
        self.frame_for_radio_buttons.grid(
            row=5,
            column=0,
            pady=(0, 10),
            padx=(30, 0),
            sticky='w',
            columnspan=3
        )

        self.radio_button_selection = ctk.StringVar()

        ctk.CTkRadioButton(
            master=self.frame_for_radio_buttons,
            text='Student',
            variable=self.radio_button_selection,
            value='student',
            command=self.__update_label_according_to_radio_button
        ).grid(row=0, column=0, padx=(20, 10), pady=10, sticky='w')

        ctk.CTkRadioButton(
            master=self.frame_for_radio_buttons,
            text='Courses',
            variable=self.radio_button_selection,
            value='courses',
            command=self.__update_label_according_to_radio_button
        ).grid(row=0, column=1, pady=10, sticky='w')

        ctk.CTkRadioButton(
            master=self.frame_for_radio_buttons,
            text='Books',
            variable=self.radio_button_selection,
            value='books',
            command=self.__update_label_according_to_radio_button
        ).grid(row=0, column=2, padx=(10, 0), pady=10, sticky='w')

        # the must contain columns for the file
        ctk.CTkLabel(
            master=self,
            text='''Constraints:
1. For the student table, certain columns like Father Name and Email may not require values.
2. If a cell lacks a value, the entire row will be skipped.
3. Every cell in the table, excluding specific student table columns, must contain a value.
4. The order of columns doesn't matter.
5. Additional columns beyond the specified ones won't disrupt the import process.
6. In case of any data error within a cell, the entire row will be skipped or import may fail.
7. The selected Excel file must include the specified columns.''',
            wraplength=440,
            justify='left'
        ).grid(row=6, column=0, columnspan=3, sticky='w', padx=(30, 0), pady=15)

        self.frame_for_must_contain_label = ctk.CTkFrame(
            master=self,
            corner_radius=7
        )
        self.frame_for_must_contain_label.grid(
            row=7,
            column=0,
            pady=(0, 10),
            padx=(30, 0),
            sticky='w',
            columnspan=3
        )

        self.must_contain_label = ctk.CTkLabel(
            master=self.frame_for_must_contain_label,
            text='Please select type of data from radio buttons above...',
            width=420,
            height=40,
            font=('consolas', 12)
        )
        self.must_contain_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        # import button
        self.import_button = ctk.CTkButton(
            master=self,
            text='Import',
            width=97,
            command=self.__import_data
        )
        self.import_button.grid(
            row=8,
            column=2,
            padx=5,
            pady=5
        )

        self.after(100, self.lift)

    def __open_file(self) -> None:
        """
        Opens a file selection dialog and sets the chosen Excel file path in the entry widget.

        Returns:
            None
        """
        file_path = askopenfilename(
            defaultextension='.xlsx',
            filetypes=[('All Excel Files', '*.xlsx')],
            title='Select Excel File'
        )
        self.file_path.set(file_path)
        self.after(100, self.lift)

    def __create_label_from_list_in_grid_form(self, columns: list[str]) -> str:
        """
        Creates a formatted label text from a list of column names for display.

        Parameters:
            columns (list): List of column names.

        Returns:
            str: Formatted label text.
        """
        text = ''
        for index, column in enumerate(columns):
            if index % 2 == 0:
                text += f'{index + 1: >2}. {column: <30}'

            else:
                text += f'{index + 1: >2}. {column}\n'

        if len(columns) > 4:
            self.geometry('500x655')

        else:
            self.geometry('500x600')

        return text

    def __update_label_according_to_radio_button(self) -> None:
        """
        Updates the `must_contain_label based` on the selected radio button.

        Returns:
            None
        """
        column_names = {
            'student': ['Name', 'Date of Birth', 'Address', 'Mobile no', 'Email', 'Year of Admission', 'Age', 'Gender', 'Pincode', 'Course ID', 'Father Name', '10th Percentage', '12th Percentage', 'Fee Deposited'],
            'courses': ['Course ID', 'Course Name', 'Fee', 'Year'],
            'books': ['Name', 'Quantity', 'Course ID', 'ISBN', 'Publisher']
        }

        text_to_update_on_label = self.__create_label_from_list_in_grid_form(
            column_names[self.radio_button_selection.get()])[0: -1]

        self.must_contain_label.configure(
            text=text_to_update_on_label, justify='left')

    def __enable_import_button(self) -> None:
        """
        Enables the Import button.
        """
        self.import_button.configure(text='Import', state='enabled')

    def __import_data(self) -> None:
        """
        Imports data from the selected Excel file into the database based on user choices.

        Returns:
            None
        """

        table_name = self.radio_button_selection.get()
        sheet_name = self.sheet_name.get()
        file_path = self.file_path.get()

        if not os.path.exists(file_path):
            ShowError('Import Failed', f'The provided path "{file_path}" does not exists.')
            return None

        try:
            data = pd.read_excel(
                io=file_path,
                sheet_name=sheet_name
            )

        except ValueError as ve:
            ShowError('Import Failed', ve)
            return None

        data_frame = pd.DataFrame(data)

        self.import_button.configure(text='Importing...', state='disabled')

        match table_name:
            case 'student':
                self.__write_data_in_db_for_student(data_frame)

            case 'courses':
                self.__write_data_in_db_for_courses(data_frame)

            case 'books':
                self.__write_data_in_db_for_books(data_frame)

            case _:
                ShowError('Import Failed',
                          'Please select type of data from the radio buttons.')
                self.__enable_import_button()

    def __write_data_in_db_for_student(self, df: dataframe) -> None:
        """
        Writes student data from DataFrame to the database.

        Parameters:
            df (pd.DataFrame): DataFrame containing student data.

        Returns:
            None
        """
        with DatabaseConnector() as connector:
            for row in df.index:
                data_set = df.iloc[row]
                null_set = df.isnull().iloc[row]

                if null_set['Name']:
                    continue

                elif null_set['Date of Birth']:
                    continue

                elif null_set['Address']:
                    continue

                elif null_set['Mobile no']:
                    continue

                elif null_set['Year of Admission']:
                    continue

                elif null_set['Age']:
                    continue

                elif null_set['Gender']:
                    continue

                elif null_set['Pincode']:
                    continue

                elif null_set['Course ID']:
                    continue

                elif null_set['10th Percentage']:
                    continue

                elif null_set['12th Percentage']:
                    continue

                else:
                    connector.cursor.execute(
                        '''
                        INSERT INTO student(name, dob, address, phone_no, email, year_of_ad, age, gender, pincode, course_id, f_name, class_10_per, class_12_per, fee_deposited) 
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                        ''',
                        [
                            data_set['Name'],
                            pd.Timestamp(data_set['Date of Birth']).to_pydatetime().strftime('%Y-%m-%d'),
                            data_set['Address'],
                            str(np.int64(data_set['Mobile no']).item()),
                            None if null_set['Email'] else data_set['Email'],
                            np.uint16(data_set['Year of Admission']).item(),
                            np.uint8(data_set['Age']).item(),
                            data_set['Gender'],
                            np.int64(data_set['Pincode']).item(),
                            np.int32(data_set['Course ID']).item(),
                            None if null_set['Father Name'] else data_set['Father Name'],
                            round(np.float16(data_set['10th Percentage']).item(), 2),
                            round(np.float16(data_set['12th Percentage']).item(), 2),
                            0 if null_set['Fee Deposited'] else np.int32(data_set['Fee Deposited']).item()
                        ]
                    )

                    connector.db.commit()

        ShowInfo('Import Data', 'Successfully imported the data.')
        self.__enable_import_button()

    def __write_data_in_db_for_courses(self, df: dataframe) -> None:
        """
        Writes courses data from DataFrame to the database.

        Parameters:
            df (pd.DataFrame): DataFrame containing courses data.

        Returns:
            None
        """
        with DatabaseConnector() as connector:
            for row in df.index:
                if df.isnull().iloc[row].any():
                    continue

                else:
                    data_set = df.iloc[row]

                    try:
                        connector.cursor.execute(
                            '''
                            INSERT INTO courses(course_id, name, fee, year)
                            VALUES(?, ?, ?, ?);
                            ''',
                            [
                                np.int32(data_set['Course ID']).item(),
                                data_set['Course Name'],
                                np.int64(data_set['Fee']).item(),
                                np.uint8(data_set['Year']).item()
                            ]
                        )
                        connector.db.commit()

                    except:
                        ShowError(
                            'Import Failed', 'Your Excel sheet may contain duplicate data, or the row in the Excel sheet is already present in the software. Please remove them.')
                        self.__enable_import_button()
                        return None

        ShowInfo('Import Data', 'Successfully imported the data.')
        self.__enable_import_button()

    def __write_data_in_db_for_books(self, df: dataframe) -> None:
        """
        Writes books data from DataFrame to the database.

        Parameters:
            df (pd.DataFrame): DataFrame containing books data.

        Returns:
            None
        """
        with DatabaseConnector() as connector:
            for row in df.index:
                if df.isnull().iloc[row].any():
                    continue

                else:
                    data_set = df.iloc[row]
                    connector.cursor.execute(
                        '''
                        INSERT INTO books(name, quantity, course_id, isbn, publisher)
                        VALUES(?, ?, ?, ?, ?);
                        ''',
                        [
                            data_set['Name'],
                            np.int32(data_set['Quantity']).item(),
                            np.int32(data_set['Course ID']).item(),
                            np.int64(data_set['ISBN']).item(),
                            data_set['Publisher']
                        ]
                    )
                    connector.db.commit()

        ShowInfo('Import Data', 'Successfully imported the data.')
        self.__enable_import_button()

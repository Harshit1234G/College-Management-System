import customtkinter as ctk
from content_frame import CTkWindow, ContentFrame
from excel_connector import ExportToExcel, ImportFromExcel
from database_connector import DatabaseConnector
from PIL import Image
import os

type ScrollableFrame = ContentFrame
type icon = ctk.CTkImage


class Menu(ctk.CTkTabview):
    """
    A customtkinter (ctk) Tabview for organizing and displaying menu options related to various functionalities.

    Usage:
        In class example,
        ```
        self.menu = Menu(
            master=self,
            self.content_frame=<instance of ContentFrame class>,
            width=200
        )
        self.menu.pack(
            expand=True,
            anchor='w',
            pady=(0, 5),
            padx=(5, 0)
        )
        ```

    Parameters:
        - master (CTkWindow): The master widget.
        - self.content_frame (ScrollableFrame): The frame containing the content or functions associated with each menu option.

    Attributes:

        Student Related Buttons
        - new_admission_button (ctk.CTkButton): Button to initiate a new student admission.
        - fetch_data_button (ctk.CTkButton): Button to fetch student data.
        - update_data_button (ctk.CTkButton): Button to update student data.
        - deposit_fee_button (ctk.CTkButton): Button to deposit fees for a student.
        - remove_student_button (ctk.CTkButton): Button to remove a student record.

        Library Related Buttons
        - lend_book_button (ctk.CTkButton): Button to lend a book from the library.
        - return_book_button (ctk.CTkButton): Button to return a book to the library.
        - book_list_button (ctk.CTkButton): Button to view the list of available books.
        - add_book_button (ctk.CTkButton): Button to add a new book to the library.
        - remove_book_button (ctk.CTkButton): Button to remove a book from the library.
        - update_book_stock_button (ctk.CTkButton): Button to update the stock of a book in the library.

        Course Related Buttons
        - add_course_button (ctk.CTkButton): Button to add a new course.
        - remove_course_button (ctk.CTkButton): Button to remove a course.
        - update_course_button (ctk.CTkButton): Button to update course information.
        - show_course_button (ctk.CTkButton): Button to display a list of all courses.

        Excel Related Buttons
        - export_data_button (ctk.CTkButton): Button to export data to excel file.
        - import_data_button (ctk.CTkButton): Button to import data from excel file.

    Note:
        - master must be a customtkinter window instance
        - self.content_frame prefered to be a customtkinter ScrollableFrame
    """

    def __init__(
            self, 
            master: CTkWindow, 
            content_frame: ScrollableFrame, 
            **kwargs
        ) -> None:

        super().__init__(master, **kwargs)
        self.content_frame = content_frame

        self.pack(fill='y')

        # tabs
        self.add('Accounts')
        self.add('Library')
        self.add('Courses')
        self.add('Excel')

        self._segmented_button.configure(font= ('arial', 12, 'bold'))

        #getting default tab from db and setting it
        with DatabaseConnector() as connector:
            connector.cursor.execute(
                '''
                SELECT value
                FROM settings
                WHERE setting = "default_tab";
                '''
            )
            tab = connector.cursor.fetchall()[0][0]
            self.set(tab)

        # adding widgets
        # accounts
        self.new_admission_button = ctk.CTkButton(
            master=self.tab('Accounts'),
            text='New Admission',
            command= self.content_frame.new_admission_gui,
            image= self.__create_ctkimage('new_admission.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.fetch_data_button = ctk.CTkButton(
            master=self.tab('Accounts'),
            text='Fetch Student Data',
            command= self.content_frame.fetch_student_data,
            image= self.__create_ctkimage('fetch_student.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.update_data_button = ctk.CTkButton(
            master=self.tab('Accounts'),
            text='Update Student Data',
            command= self.content_frame.update_student_gui,
            image= self.__create_ctkimage('update_student.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.deposit_fee_button = ctk.CTkButton(
            master=self.tab('Accounts'),
            text='Deposit Fee',
            command= self.content_frame.deposit_fee,
            image= self.__create_ctkimage('fee_deposit.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.remove_student_button = ctk.CTkButton(
            master=self.tab('Accounts'),
            text='Remove Student',
            command= self.content_frame.remove_student_gui,
            image= self.__create_ctkimage('remove_student.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )


        self.new_admission_button.pack(pady=5)
        self.__create_canvas_and_line('Accounts')
        self.fetch_data_button.pack(pady=5)
        self.__create_canvas_and_line('Accounts')
        self.update_data_button.pack(pady=5)
        self.__create_canvas_and_line('Accounts')
        self.deposit_fee_button.pack(pady=5)
        self.__create_canvas_and_line('Accounts')
        self.remove_student_button.pack(pady=5)
        self.__create_canvas_and_line('Accounts')

        # library
        self.lend_book_button = ctk.CTkButton(
            master=self.tab('Library'),
            text='Lend Book',
            command= self.content_frame.lend_book,
            image= self.__create_ctkimage('lend_book.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.return_book_button = ctk.CTkButton(
            master=self.tab('Library'),
            text='Return Book', 
            command= self.content_frame.return_book,
            image= self.__create_ctkimage('return_book.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.book_list_button = ctk.CTkButton(
            master=self.tab('Library'),
            text='Books List',
            command= self.content_frame.show_books,
            image= self.__create_ctkimage('book_list.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.add_book_button = ctk.CTkButton(
            master=self.tab('Library'),
            text='Add Book',
            command= self.content_frame.add_book_gui,
            image= self.__create_ctkimage('add_book.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.remove_book_button = ctk.CTkButton(
            master=self.tab('Library'),
            text='Remove Book',
            command= self.content_frame.remove_book_gui,
            image= self.__create_ctkimage('remove_book.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.update_book_stock_button = ctk.CTkButton(
            master=self.tab('Library'),
            text='Update Stock',
            command= self.content_frame.update_stock_gui,
            image= self.__create_ctkimage('update_stock.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )


        self.lend_book_button.pack(pady=5)
        self.__create_canvas_and_line('Library')
        self.return_book_button.pack(pady=5)
        self.__create_canvas_and_line('Library')
        self.book_list_button.pack(pady=5)
        self.__create_canvas_and_line('Library')
        self.add_book_button.pack(pady=5)
        self.__create_canvas_and_line('Library')
        self.remove_book_button.pack(pady=5)
        self.__create_canvas_and_line('Library')
        self.update_book_stock_button.pack(pady=5)
        self.__create_canvas_and_line('Library')

        # courses
        self.add_course_button = ctk.CTkButton(
            master=self.tab('Courses'),
            text='Add Course',
            command= self.content_frame.add_course_gui,
            image= self.__create_ctkimage('add_course.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.remove_course_button = ctk.CTkButton(
            master=self.tab('Courses'),
            text='Remove Course',
            command= self.content_frame.remove_course_gui,
            image= self.__create_ctkimage('remove_course.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.update_course_button = ctk.CTkButton(
            master=self.tab('Courses'),
            text='Update Course',
            command= self.content_frame.update_course_gui,
            image= self.__create_ctkimage('update_course.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.show_course_button = ctk.CTkButton(
            master=self.tab('Courses'),
            text='Show all Courses',
            command= self.content_frame.show_all_courses,
            image= self.__create_ctkimage('show_all_courses.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )


        self.add_course_button.pack(pady=5)
        self.__create_canvas_and_line('Courses')
        self.remove_course_button.pack(pady=5)
        self.__create_canvas_and_line('Courses')
        self.update_course_button.pack(pady=5)
        self.__create_canvas_and_line('Courses')
        self.show_course_button.pack(pady=5)
        self.__create_canvas_and_line('Courses')

        # excel
        self.export_data_button = ctk.CTkButton(
            master=self.tab('Excel'),
            text='Export Data',
            command= self.export_data_to_excel,
            image= self.__create_ctkimage('export.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )

        self.import_data_button = ctk.CTkButton(
            master=self.tab('Excel'),
            text='Import Data',
            command= self.import_data_from_excel,
            image= self.__create_ctkimage('import.png'),
            font= ('arial', 14),
            anchor= 'w',
            width= 200,
            fg_color= '#1F6AA5'
        )


        self.export_data_button.pack(pady=5)
        self.__create_canvas_and_line('Excel')
        self.import_data_button.pack(pady=5)
        self.__create_canvas_and_line('Excel')

    def export_data_to_excel(self, event: any = None) -> None:
        self.content_frame.content_remover()
        ExportToExcel()

    def import_data_from_excel(self, event: any = None) -> None:
        self.content_frame.content_remover()
        ImportFromExcel()

    def __create_canvas_and_line(self, tab_name: str) -> None:
        """
        Creates a canvas widget and draws a line to it.

        Parameters:
            - tab_name (str): name of the tab in which to create the canvas.

        Returs:
            - None
        """
        canvas_widget = ctk.CTkCanvas(
            master= self.tab(tab_name),
            width= 200,
            height= 20,
            bg= '#1F6AA5',
            highlightthickness= 0
        )
        canvas_widget.pack()

        canvas_widget.create_line(10, 10, 180, 10, fill= 'white')

    @staticmethod
    def __create_ctkimage(file_name: str) -> icon:
        """
        Gets the image from the icons folder, creates and CTkImage object and returns it.

        Parameters:
            - file_name (str): name of the image file in icons folder.

        Returns:
            - icon: customtkinter CTkImage object.
        """
        img = ctk.CTkImage(Image.open(os.path.join('icons', file_name)), size= (40, 40))
        return img

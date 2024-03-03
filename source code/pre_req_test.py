import os
import numpy as np

class PreReqTester:
    """
    Run preliminary tests to ensure the existence of necessary files and the feasibility of a database connection. Verify that all required files are present and confirm the ability to connect to the database.
    """
    error = ''

    def __init__(self) -> None:
        try:
            icons_files = np.array(os.listdir('icons'))

        except FileNotFoundError:
            self.error = 'icons folder is missing.'
            return None
        
        if not os.path.exists('data.sqlite'):
            self.error = 'Cannot access database, either data.sqlite is removed or renamed.'

        testing_files = np.array(
            [
                'add_book.png', 
                'add_course.png', 
                'app.png', 
                'book_list.png', 
                'error.png', 
                'export.png', 
                'fee_deposit.png', 
                'fetch_student.png', 
                'import.png', 
                'info.png', 
                'lend_book.png', 
                'new_admission.png', 
                'remove_book.png', 
                'remove_course.png', 
                'remove_student.png', 
                'return_book.png', 
                'settings.png', 
                'show_all_courses.png', 
                'sigin_form_img.jpg', 
                'update_course.png', 
                'update_stock.png', 
                'update_student.png', 
                'warning.png'
            ]
        )

        try:
            icons_files == testing_files
        
        except:
            self.error = 'Either files are removed or renamed from icons folder.'
            return None


    def __len__(self) -> int:
        return len(self.error)

    def __str__(self) -> str:
        return self.error

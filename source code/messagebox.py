import customtkinter as ctk
from PIL import ImageTk, Image
import os

type NoneOrCallable = None | callable

class ShowError(ctk.CTkToplevel):
    """
    A customtkinter Toplevel window for displaying error messages.

    Parameters:
        title_of_box (str): The title of the error box. Default is 'ShowError'.
        error_msg (str): The error message to be displayed. Default is 'Error'.

    Usage:
        ```
        ShowError('Title', 'Error msg to display')
        ```
    """

    def __init__(
        self,
        title_of_box: str = 'Error',
        error_msg: str = 'Error',
        *args,
        **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)

        self.title(title_of_box)
        self.geometry('300x100')
        self.resizable(False, False)

        # changing icon
        self.imagepath = ImageTk.PhotoImage(
            file=os.path.join('icons', 'app.png'))
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, self.imagepath))

        img_path = os.path.join('icons', 'error.png')

        self.icon = ctk.CTkImage(
            dark_image=Image.open(img_path),
            light_image=Image.open(img_path),
            size=(30, 30)
        )

        self.icon_label = ctk.CTkLabel(
            master=self,
            image=self.icon,
            text=''
        )

        self.icon_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.label = ctk.CTkLabel(
            master=self,
            text=error_msg,
            font=('arial', 12),
            wraplength=230
        )

        self.label.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # Center the label in both directions
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.after(100, self.lift)


class ShowInfo(ctk.CTkToplevel):
    """
    A customtkinter Toplevel window for displaying informational messages.

    Parameters:
        title_of_box (str): The title of the information box. Default is 'ShowInfo'.
        info_msg (str): The information message to be displayed. Default is 'info'.

    Usage:
        ```
        ShowInfo('Title', 'Informational msg to display')
        ```
    """

    def __init__(
        self,
        title_of_box: str = 'ShowInfo',
        info_msg: str = 'info',
        *args,
        **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)

        self.title(title_of_box)
        self.geometry('300x100')
        self.resizable(False, False)

        # changing icon
        self.imagepath = ImageTk.PhotoImage(
            file=os.path.join('icons', 'app.png'))
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, self.imagepath))

        img_path = os.path.join('icons', 'info.png')

        self.icon = ctk.CTkImage(
            dark_image=Image.open(img_path),
            light_image=Image.open(img_path),
            size=(30, 30)
        )

        self.icon_label = ctk.CTkLabel(
            master=self,
            image=self.icon,
            text=''
        )

        self.icon_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.label = ctk.CTkLabel(
            master=self,
            text=info_msg,
            font=('arial', 12),
            wraplength=230
        )

        self.label.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.after(100, self.lift)


class ShowWarning(ctk.CTkToplevel):
    """
    A custom tkinter Toplevel window for displaying warning messages.

    Parameters:
        title_of_box (str): The title of the warning box. Default is 'ShowWarning'.
        warning_msg (str): The warning message to be displayed. Default is 'warning'.
        command (None or callable): A function to be executed when the 'OK' button is clicked, default is None.

    Usage:
        ```
        ShowWarning('Title', 'Warning msg to display', command=#any callable function)
        ```
    """

    def __init__(
        self,
        title_of_box: str = 'ShowWarning',
        warning_msg: str = 'warning',
        command: NoneOrCallable = None,
        *args,
        **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)
        self.command = command

        self.title(title_of_box)
        self.geometry('300x100')
        self.resizable(False, False)

        # changing icon
        self.imagepath = ImageTk.PhotoImage(
            file=os.path.join('icons', 'app.png'))
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, self.imagepath))

        img_path = os.path.join('icons', 'warning.png')

        self.icon = ctk.CTkImage(
            dark_image=Image.open(img_path),
            light_image=Image.open(img_path),
            size=(30, 30)
        )

        self.icon_label = ctk.CTkLabel(
            master=self,
            image=self.icon,
            text=''
        )

        self.icon_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.label = ctk.CTkLabel(
            master=self,
            text=warning_msg,
            font=('arial', 12),
            wraplength=230
        )

        self.label.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.ok_button = ctk.CTkButton(
            master=self,
            text='OK',
            command=lambda: self.remove_toplevel_and_run_command()
        )

        self.ok_button.grid(
            row=1,
            column=1,
            pady=5
        )

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.after(100, self.lift)

    def remove_toplevel_and_run_command(self) -> None:
        """
        Destroy the warning window and execute the provided command.
        """

        self.destroy()
        if self.command:
            self.command()

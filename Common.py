# By Abdullah As-Sadeed

from tkinter import filedialog, ttk
import sys
import tkinter
import tkinter.font as tkFont

TKINTER_WINDOW_WIDTH_BUFFER = 100


def exit_program():
    sys.exit(0)


def select_directory_or_file(type):
    tkinter_root = tkinter.Tk()
    tkinter_root.withdraw()
    tkinter_root.protocol("WM_DELETE_WINDOW", exit_program)

    if type == "Directory":
        path = filedialog.askdirectory()
    if type == "File":
        path = filedialog.askopenfilename()

    tkinter_root.destroy()
    tkinter_root.quit()

    return path


def select_option(title, options):
    tkinter_root = tkinter.Tk()
    tkinter_root.protocol("WM_DELETE_WINDOW", exit_program)

    tkinter_font = tkFont.Font()
    title_width = tkinter_font.measure(title)
    tkinter_root.minsize(title_width + TKINTER_WINDOW_WIDTH_BUFFER, 0)

    tkinter_root.title(title)
    selected_option = tkinter.StringVar()
    combobox = ttk.Combobox(
        tkinter_root,
        values=options,
        textvariable=selected_option,
    )
    combobox.pack()
    combobox.current(0)

    def next():
        global return_value
        return_value = selected_option.get()
        tkinter_root.destroy()
        tkinter_root.quit()

    next_button = tkinter.Button(tkinter_root, text="Next", command=next)
    next_button.pack()
    tkinter_root.mainloop()

    return return_value


def select_number(title, minimum, maximum, default_value):
    tkinter_root = tkinter.Tk()
    tkinter_root.protocol("WM_DELETE_WINDOW", exit_program)

    tkinter_font = tkFont.Font()
    title_width = tkinter_font.measure(title)
    tkinter_root.minsize(title_width + TKINTER_WINDOW_WIDTH_BUFFER, 0)

    tkinter_root.title(title)
    slider_value = tkinter.IntVar(value=default_value)
    slider = tkinter.Scale(
        tkinter_root,
        from_=minimum,
        to=maximum,
        orient=tkinter.HORIZONTAL,
        length=title_width + TKINTER_WINDOW_WIDTH_BUFFER,
        variable=slider_value,
    )
    slider.pack()

    def next():
        global return_value
        return_value = slider_value.get()
        tkinter_root.destroy()
        tkinter_root.quit()

    next_button = tkinter.Button(tkinter_root, text="Next", command=next)
    next_button.pack()
    tkinter_root.mainloop()

    return return_value


def enter_text(title, default_value):
    tkinter_root = tkinter.Tk()
    tkinter_root.protocol("WM_DELETE_WINDOW", exit_program)

    tkinter_font = tkFont.Font()
    title_width = tkinter_font.measure(title)
    tkinter_root.minsize(title_width + TKINTER_WINDOW_WIDTH_BUFFER, 0)

    tkinter_root.title(title)
    input_text = tkinter.StringVar(value=default_value)
    entry = tkinter.Entry(
        tkinter_root,
        textvariable=input_text,
    )
    entry.pack()

    def next():
        global return_value
        return_value = input_text.get()
        tkinter_root.destroy()
        tkinter_root.quit()

    next_button = tkinter.Button(tkinter_root, text="Next", command=next)
    next_button.pack()
    tkinter_root.mainloop()

    return return_value

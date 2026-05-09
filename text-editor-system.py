import os
from tkinter import *
from tkinter.ttk import *
from tkinter import font, colorchooser, filedialog, messagebox
from datetime import datetime

#functions
def date_time(event=None):
    currentDateTime = datetime.now()
    formattedDateTime = currentDateTime.strftime("%d/%m/%Y - %#I:%M:%S %p (%H:%M:%S) ")
    textarea.insert(1.0, formattedDateTime)

def change_theme(bg_color, fg_color):
    textarea.config(background=bg_color, fg=fg_color)

def toolbarFunc():
    if show_toolbar.get()==False:
        tool_bar.pack_forget()
    if show_toolbar.get()==True:
        textarea.pack_forget()
        tool_bar.pack(fill=X)
        textarea.pack(fill=BOTH, expand=True)

def statusbarFunc():
    if show_statusbar.get()==False:
        status_bar.pack_forget()
    else:
        status_bar.pack(side=BOTTOM)

def find():
    #functionality
    def find_words():
        textarea.tag_remove("match", "1.0", END)
        start_pos = "1.0"
        word = FindentryField.get()
        if word:
            while True:
                start_pos = textarea.search(word, start_pos, stopindex=END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word)}c"
                textarea.tag_add("match", start_pos, end_pos)

                textarea.tag_config("match", foreground="red", background="yellow")
                start_pos=end_pos

    def replace_text():
        word = FindentryField.get()
        replaceword = replaceEntryField.get()
        content = textarea.get(1.0, END)
        new_content = content.replace(word, replaceword)
        textarea.delete(1.0, END)
        textarea.insert(1.0, new_content)

    #GUI
    root1 = Toplevel(root)

    root1.title("Find")
    root1.geometry("450x250+500+200")
    root1.resizable(False, False)
    root1.iconbitmap("text-editor-icon.ico")
    labelFrame = LabelFrame(root1, text="Find/Replace")
    labelFrame.pack(pady=20)

    findLabel = Label(labelFrame, text="Find")
    findLabel.grid(row=0, column=0, padx=5, pady=5)
    FindentryField = Entry(labelFrame)
    FindentryField.grid(row=0, column=1, padx=5, pady=5)
    replaceLabel = Label(labelFrame, text="Replace")
    replaceLabel.grid(row=1, column=0, padx=5, pady=5)
    replaceEntryField = Entry(labelFrame)
    replaceEntryField.grid(row=1, column=1, padx=5, pady=5)

    findButton = Button(labelFrame, text="Find", command=find_words)
    findButton.grid(row=2, column=0, padx=5, pady=5)

    replaceButton = Button(labelFrame, text="Replace", command=replace_text)
    replaceButton.grid(row=2, column=1, padx=5, pady=5)

    def delete_find_window():
        textarea.tag_remove("match", "1.0", END)
        root1.destroy()

    root1.protocol("WM_DELETE_WINDOW", delete_find_window)
    
    root1.mainloop()

def statusBarFunction(event):
    if textarea.edit_modified():
        word = len(textarea.get(0.0, END).split())
        characters = len(textarea.get(0.0, "end -1c").replace(" ", ""))
        status_bar.config(text=f"Characters: {characters} Words: {word}")

    textarea.edit_modified(False)

url = ""
def new_file(event):
    global url
    url = ""
    textarea.delete(0.0, END)

def open_file(event):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("Text files", "txt"), ("All files", "*.*")))

    if url != "":
        data = open(url, "r")
        textarea.insert(0.0, data.read())
    root.title(os.path.basename(url))

def save_file(event):
    if url == "":
        save_url = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=(("Text files", "txt"), ("All files", "*.*")))
        if save_url is None:
            pass
        else:
            content = textarea.get(0.0, END)
            save_url.write(content)
            save_url.close()
    else:
        content = textarea.get(0.0, END)
        file = open(url, "w")
        file.write(content)

def saveas_file(event):
    save_url = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=(("Text files", "txt"), ("All files", "*.*")))
    content = textarea.get(0.0, END)
    save_url.write(content)
    save_url.close()
    if url != "":
        os.remove(url)

def iexit(event=None):
    if textarea.edit_modified():
        result = messagebox.askyesnocancel("Warning", "Do you want to save the file?")
        if result is True:
            if url != "":
                content = textarea.get(0.0, END)
                file = open(url, "w")
                file.write(content)
                root.destroy()
            else:
                content = textarea.get(0.0, END)
                save_url = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=(("Text files", "txt"), ("All files", "*.*")))
                save_url.write(content)
                save_url.close()
                root.destroy()

        elif result is False:
            root.destroy()
        else:
            pass
    else:
        root.destroy()

fontSize = 12
fontStyle = "Arial"
def font_style(event):
    global fontStyle
    fontStyle = font_family_variable.get()
    textarea.config(font=(fontStyle, fontSize))

def font_size(event):
    global fontSize
    fontSize = size_variable.get()
    textarea.config(font=(fontStyle, fontSize))

def bold_text():
    text_property = font.Font(font=textarea["font"]).actual()
    if text_property["weight"] == "normal":
        textarea.config(font=(fontStyle, fontSize, "bold"))

    if text_property["weight"] == "bold":
        textarea.config(font=(fontStyle, fontSize, "normal"))

def italic_text():
    text_property = font.Font(font=textarea["font"]).actual()
    if text_property["slant"] == "roman":
        textarea.config(font=(fontStyle, fontSize, "italic"))

    if text_property["slant"] == "italic":
        textarea.config(font=(fontStyle, fontSize, "roman"))

def underline_text():
    text_property = font.Font(font=textarea["font"]).actual()
    if text_property["underline"] == 0:
        textarea.config(font=(fontStyle, fontSize, "underline"))
    if text_property["underline"] == 1:
        textarea.config(font=(fontStyle, fontSize,))

def color_select():
    color = colorchooser.askcolor()
    textarea.config(fg=color[1])

def align_right():
    data = textarea.get(0.0, END)
    textarea.tag_config("right", justify=RIGHT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, "right")

def align_left():
    data = textarea.get(0.0, END)
    textarea.tag_config("left", justify=LEFT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, "left")

def align_center():
    data = textarea.get(0.0, END)
    textarea.tag_config("center", justify=CENTER)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, "center")

#window system
root = Tk()
root.iconbitmap("text-editor-icon.ico")
root.title("Text editor")
root.geometry("1200x620+10+10")
menuBar = Menu(root)
root.config(menu=menuBar)

#file menu
fileMenu = Menu(menuBar, tearoff=False)
menuBar.add_cascade(label="File", menu=fileMenu)

New_image = PhotoImage(file="images/new.png")
fileMenu.add_command(label="New", accelerator="Ctrl+N", image=New_image, compound=LEFT, command=new_file)
Open_image = PhotoImage(file="images/open.png")
fileMenu.add_command(label="Open", accelerator="Ctrl+O", image=Open_image, compound=LEFT, command=open_file)
Save_image = PhotoImage(file="images/save.png")
fileMenu.add_command(label="Save", accelerator="Ctrl+S", image=Save_image, compound=LEFT, command=save_file)
fileMenu.add_command(label="Save As", accelerator="Ctrl+Alt+S", image=Save_image, compound=LEFT, command=saveas_file)
fileMenu.add_separator()
Exit_image = PhotoImage(file="images/exit.png")
fileMenu.add_command(label="Exit", accelerator="Ctrl+Q", image=Exit_image, compound=LEFT, command=iexit)


#edit menu
editMenu = Menu(menuBar, tearoff=False)
Find_image = PhotoImage(file="images/find.png")
Cut_image = PhotoImage(file="images/cut.png")
Copy_image = PhotoImage(file="images/copy.png")
Paste_image = PhotoImage(file="images/paste.png")
Clear_image = PhotoImage(file="images/eraser.png")
Select_all_image = PhotoImage(file="images/select_all.png")
Undo_image = PhotoImage(file="images/undo.png")
Redo_image = PhotoImage(file="images/redo.png")
Date_time_image = PhotoImage(file="images/calendar.png")


#toolbar section
tool_bar = Label(root)
tool_bar.pack(side=TOP, fill=X)
font_families = font.families()
font_family_variable = StringVar()
fontFamily_Combobox = Combobox(tool_bar, width=30, state="readonly", values=font_families, textvariable=font_family_variable)
fontFamily_Combobox.current(font_families.index("Arial"))
fontFamily_Combobox.grid(row=0, column=0, padx=5)
size_variable = IntVar()
font_size_Combobox=Combobox(tool_bar, width=14, textvariable=size_variable, state="readonly", values=tuple(range(8, 81)))
font_size_Combobox.current(4)
font_size_Combobox.grid(row=0, column=1, padx=5)

fontFamily_Combobox.bind("<<ComboboxSelected>>", font_style)
font_size_Combobox.bind("<<ComboboxSelected>>", font_size)

#buttons section
bold_image = PhotoImage(file="images/bold.png")
bold_button = Button(tool_bar, image=bold_image, command=bold_text)
bold_button.grid(row=0, column=2, padx=5)

italic_image = PhotoImage(file="images/italic.png")
italic_button = Button(tool_bar, image=italic_image, command=italic_text)
italic_button.grid(row=0, column=3, padx=5)

underline_image = PhotoImage(file="images/underline.png")
underline_button = Button(tool_bar, image=underline_image, command=underline_text)
underline_button.grid(row=0, column=4, padx=5)

font_color_image = PhotoImage(file="images/color_wheel.png")
font_color_button = Button(tool_bar, image=font_color_image, command=color_select)
font_color_button.grid(row=0, column=5, padx=5)

left_align_image = PhotoImage(file="images/left_align.png")
left_align_button = Button(tool_bar, image=left_align_image, command=align_left)
left_align_button.grid(row=0, column=6, padx=5)

right_align_image = PhotoImage(file="images/right_align.png")
right_align_button = Button(tool_bar, image=right_align_image, command=align_right)
right_align_button.grid(row=0, column=7, padx=5)

center_align_image = PhotoImage(file="images/center_align.png")
center_align_button = Button(tool_bar, image=center_align_image, command=align_center)
center_align_button.grid(row=0, column=8, padx=5)

#text area system
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
textarea = Text(root, yscrollcommand=scrollbar.set, font=("Arial", 12), undo=True)
textarea.pack(fill=BOTH, expand=True)
scrollbar.config(command=textarea.yview)

editMenu.add_command(label="Cut", accelerator="Ctrl+X", image=Cut_image, compound=LEFT, command=lambda:textarea.event_generate("<Control x>"))
editMenu.add_command(label="Copy", accelerator="Ctrl+C", image=Copy_image, compound=LEFT, command=lambda:textarea.event_generate("<Control c>"))
editMenu.add_command(label="Paste", accelerator="Ctrl+V", image=Paste_image, compound=LEFT, command=lambda:textarea.event_generate("<Control v>"))
editMenu.add_command(label="Select all", accelerator="Ctrl+A", image=Select_all_image, compound=LEFT, command=find)
editMenu.add_command(label="Clear", accelerator="Ctrl+Alt+X", image=Clear_image, compound=LEFT, command=lambda:textarea.delete(0.0, END))
editMenu.add_command(label="Find", accelerator="Ctrl+F", image=Find_image, compound=LEFT, command=find)
editMenu.add_separator()
editMenu.add_command(label="Undo", accelerator="Ctrl+Z", image=Undo_image, compound=LEFT)
editMenu.add_command(label="Redo", accelerator="Ctrl+Y", image=Redo_image, compound=LEFT)
editMenu.add_command(label="Time/Date", accelerator="Ctrl+D", image=Date_time_image, compound=LEFT, command=date_time)
menuBar.add_cascade(label="Edit", menu=editMenu)

#view menu section
show_toolbar = BooleanVar()
show_statusbar = BooleanVar()
show_toolbar.set(True)
show_statusbar.set(True)
Tool_image = PhotoImage(file="images/tools.png")
Status_bar_image = PhotoImage(file="images/status-bar.png")
viewMenu = Menu(menuBar, tearoff=False)
viewMenu.add_checkbutton(label="Tool bar", variable=show_toolbar, onvalue=True, offvalue=False, image=Tool_image, compound=LEFT, command=toolbarFunc)
viewMenu.add_checkbutton(label="Status bar", variable=show_statusbar, onvalue=True, offvalue=False, image=Status_bar_image, compound=LEFT, command=statusbarFunc)
menuBar.add_cascade(label="View", menu=viewMenu)

#themes
themesMenu = Menu(menuBar, tearoff=False)
menuBar.add_cascade(label="Themes", menu=themesMenu)

white_theme = PhotoImage(file="images/white.png")
dark_theme = PhotoImage(file="images/dark.png")
flavescent_theme = PhotoImage(file="images/flavescent.png")
dark_blue_theme = PhotoImage(file="images/dark_blue.png")
pink_theme = PhotoImage(file="images/pink.png")
theme_choice = StringVar()
theme_choice.set("white")

themesMenu.add_radiobutton(label="White (default)", image=white_theme, compound=LEFT, variable=theme_choice, value="white", command= lambda:change_theme("white", "black"))
themesMenu.add_radiobutton(label="Dark", image=dark_theme, compound=LEFT, variable=theme_choice, value="dark", command= lambda:change_theme("#1C1C1C", "white"))
themesMenu.add_radiobutton(label="Flavescent", image=flavescent_theme, compound=LEFT, variable=theme_choice, value="flavescent", command= lambda:change_theme("#FFEB9A", "black"))
themesMenu.add_radiobutton(label="Dark blue", image=dark_blue_theme, compound=LEFT, variable=theme_choice, value="dark_blue", command= lambda:change_theme("#030180", "white"))
themesMenu.add_radiobutton(label="Pink", image=pink_theme, compound=LEFT, variable=theme_choice, value="pink", command= lambda:change_theme("pink", "blue"))

status_bar = Label(root, text="Status Bar")
status_bar.pack(side=BOTTOM)

textarea.bind("<<Modified>>", statusBarFunction)

root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-n>", new_file)
root.bind("<Control-Alt-S>", saveas_file)
root.bind("<Control-q>", iexit)
root.bind("<Control-d>", date_time)

root.resizable(False, False)
root.mainloop()
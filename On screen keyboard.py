from tkinter import *
import pyperclip
import requests

def start_drag(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def drag_window(event):
    x = event.x_root - x_offset
    y = event.y_root - y_offset
    root.geometry(f"+{x}+{y}")

def check_clipboard():
    clipboard_text = pyperclip.paste()
    if text_box.get() != clipboard_text:
        text_box.delete(0, END)
        text_box.insert(0, clipboard_text)
    root.after(1000, check_clipboard)

def get_meaning():
    word = text_box.get().strip().lower()
    if word:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            meaning = data[0]['meanings'][0]['definitions'][0]['definition']
        else:
            meaning = "Word not found"
        show_popup(meaning)

def show_popup(meaning):
    popup = Toplevel(root)
    popup.title("Meaning")
    popup.geometry("300x100")
    Label(popup, text=meaning, wraplength=280).pack(pady=10)
    Button(popup, text="Close", command=popup.destroy).pack(pady=5)

def close_window():
    root.destroy()

def minimize_window():
    root.iconify()

root = Tk()
root.title("overlay")
x = "50"
y = "50"
root.geometry(f'300x200+{x}+{y}')
root.overrideredirect(True)

title_bar = Frame(root, bg="blue", relief="raised", bd=2)
title_bar.pack(fill=X)
close_button = Button(title_bar, text="X", command=close_window, bg="red", fg="white", bd=0)
close_button.pack(side=RIGHT, padx=5, pady=2)
minimize_button = Button(title_bar, text="_", command=minimize_window, bg="yellow", fg="black", bd=0)
minimize_button.pack(side=RIGHT, padx=5, pady=2)
title_bar.bind("<Button-1>", start_drag)
title_bar.bind("<B1-Motion>", drag_window)

text_box = Entry(root, width=50)
text_box.pack(pady=10)
Button(root, text="Get Meaning", command=get_meaning).pack(pady=10)
meaning_label = Label(root, text="", wraplength=280)
meaning_label.pack(pady=10)

check_clipboard()
root.mainloop()
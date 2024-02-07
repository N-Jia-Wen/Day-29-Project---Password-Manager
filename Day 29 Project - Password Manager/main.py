from tkinter import *
from tkinter import messagebox
from password_generator import random_password
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    new_password = random_password()
    password_entry.delete(0, END)
    password_entry.insert(index=0, string=new_password)
    pyperclip.copy(new_password)
    messagebox.showinfo(title="Password Copied", message="Password copied to clipboard.")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email_or_username = email_username_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(email_or_username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Blank Fields", message="You've left some fields blank. Please try again.")

    else:
        is_okay = messagebox.askokcancel(title=f"Details for {website}", message=f"You have entered: "
                                                                                 f"\nEmail/Username: "
                                                                                 f"{email_or_username}"
                                                                                 f"\nPassword: {password} "
                                                                                 f"\n Is this okay to save?")

        if is_okay is True:
            with open(file="data.txt", mode="a") as file:
                file.write(f"{website} | {email_or_username} | {password}\n")

            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.minsize(width=220, height=220)
window.config(padx=50, pady=50)

# Setting up canvas:
canvas = Canvas(width=200, height=200)
logo_file = PhotoImage(file="logo.png")
logo = canvas.create_image(100, 100, image=logo_file)
canvas.grid(row=0, column=1)

# All Labels:
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# All Entries:
website_entry = Entry(width=40)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

email_username_entry = Entry(width=40)
email_username_entry.grid(row=2, column=1, columnspan=2)
email_username_entry.insert(index=0, string="example")

password_entry = Entry(width=27)
password_entry.place(x=131, y=247.5)

# All Buttons:
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()

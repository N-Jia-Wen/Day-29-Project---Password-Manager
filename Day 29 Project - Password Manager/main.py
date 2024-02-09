from tkinter import *
from tkinter import messagebox
from password_generator import random_password
import pyperclip
import json


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
    new_data = {
        website: {
            "email/username": email_or_username,
            "password": password
        }
    }

    if len(website) == 0 or len(email_or_username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Blank Fields", message="You've left some fields blank. Please try again.")

    else:
        is_okay = messagebox.askokcancel(title=f"Details for {website}", message=f"You have entered: "
                                                                                 f"\nEmail/Username: "
                                                                                 f"{email_or_username}"
                                                                                 f"\nPassword: {password} "
                                                                                 f"\n Is this okay to save?")

        if is_okay is True:
            try:
                with open(file="data.json", mode="r") as file:
                    data = json.load(file)
                    data.update(new_data)

                with open(file="data.json", mode="w") as file:
                    json.dump(data, file, indent=4)

            # To account for when json file does not yet exist when running programme for the first time:
            except FileNotFoundError:
                with open(file="data.json", mode="w") as file:
                    json.dump(new_data, file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- SEARCH FOR INFORMATION ------------------------------- #


def search_password():
    website = website_entry.get()
    # Tells user that field is blank and does not execute further code
    if len(website) == 0:
        messagebox.showinfo(title="Empty Field", message="Please enter the name of the website.")
    else:
        
        try:
            with open(file="data.json", mode="r") as file:
                data = json.load(file)

        # Catches error is json file does not exist and informs the user:
        except FileNotFoundError:
            messagebox.showinfo(title="JSON File Not Found", message="You have not saved any information yet.")

        else:

            # Otherwise, obtains data of particulars saved for that website by using name of website as key.
            website_info = data.get(website)
            if website_info is not None:
                saved_email_or_username = website_info.get("email/username")
                saved_password = website_info.get("password")
                messagebox.showinfo(title=f"Details for {website} account",
                                    message=f"Email/Username: {saved_email_or_username}\nPassword: {saved_password}")

            # If info on that particular website is not found, it informs the user that it is so.
            elif website_info is None:
                messagebox.showinfo(title="Website Info Not Found",
                                    message=f"Sorry, there is no details related to the website {website}.\n"
                                            f"Do note that this search function is case sensitive.")


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
website_entry = Entry(width=33)
website_entry.place(x=131, y=208)
website_entry.focus()

email_username_entry = Entry(width=40)
email_username_entry.grid(row=2, column=1, columnspan=2)
email_username_entry.insert(index=0, string="example123@email.com")

password_entry = Entry(width=27)
password_entry.place(x=131, y=255)

# All Buttons:
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", command=search_password)
search_button.grid(row=1, column=2)

window.mainloop()

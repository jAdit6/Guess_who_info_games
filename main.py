from tkinter import *
from tkinter import messagebox
from random import choice
from PIL import Image, ImageTk  # Import necessary Pillow modules
from tkinter import IntVar, Label, ttk, Tk
from tkinter.ttk import Style, Radiobutton as ThemedRadiobutton
import csv

participant = input("Participant number: ")

class Person:
    def __init__(self,name, alice, bob, charlie, diane, eve, male, female, black_haired, red_haired, white_haired, photo):
        self.name = name
        self.alice = alice
        self.bob = bob
        self.charlie = charlie
        self.diane = diane
        self.eve = eve
        self.male = male
        self.female = female
        self.black_haired = black_haired
        self.red_haired = red_haired
        self.white_haired = white_haired
        self.photo = photo


class GuessWhoGame:
    def __init__(self, people):
        self.people = people

    def guess_person(self, attribute, value):
        self.people = [person for person in self.people if getattr(person, attribute) == value]

    def get_remaining_people(self):
        return [person.name for person in self.people]


# Creating people for the game
people_list = [
    Person("Alice", "yes", "no", "no", "no", "no", "no", "yes", "no", "no", "yes", "alice.jpg"),
    Person("Bob", "no", "yes", "no", "no", "no", "yes", "no", "yes", "no", "no", "bob.jpg"),
    Person("Charlie", "no", "no", "yes", "no", "no", "yes", "no", "no", "yes", "no", "charlie.jpg"),
    Person("Diane", "no", "no", "no", "yes", "no", "no", "yes", "no", "yes", "no", "diana.jpg"),
    Person("Eve", "no", "no", "no", "no", "yes", "no", "yes", "no", "no", "yes", "eve.jpg")
]

# Initialize the game with the list of people
game = GuessWhoGame(people_list)

# Choosing a person randomly for the game
chosen_person = choice(game.people)

print(chosen_person.name)
with open('game_logs.csv', 'a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow([f"Participant: {participant}",
                        f"Chosen: {chosen_person.name}"])

# Radio scale
engagement_var1 = None  # Declare the variable outside the radios function
engagement_var2 = None


def radios():
    global engagement_var1, engagement_var2
    engagement_var1 = IntVar()
    engagement_var2 = IntVar()

    engagement_label1 = Label(text="How engaged do you feel?")
    engagement_label1.grid(row=7, column=2, pady=5)

    engagement_label2 = Label(text="How effortful does this feel?")
    engagement_label2.grid(row=8, column=2, pady=5)

    style = Style()
    style.configure('TRadiobutton', background='lightgray', padding=5)

    labels = ["Not at all", "Slightly", "Somewhat", "Moderately", "Very", "Extremely"]

    for i, label in enumerate(labels, start=1):
        radio = ThemedRadiobutton(window, text=label, variable=engagement_var1, value=i, style='TRadiobutton')
        radio.grid(row=7, column=i + 3, padx=1)

        radio2 = ThemedRadiobutton(window, text=label, variable=engagement_var2, value=i, style='TRadiobutton')
        radio2.grid(row=8, column=i + 3, padx=1)


# def update_people_label():
#   remaining_people = game.get_remaining_people()
#   people_label.config(text=", ".join(remaining_people))


def update_people_images():
    # Remove existing image labels from the window
    for widget in window.winfo_children():
        if isinstance(widget, Label) and hasattr(widget, "image"):
            widget.grid_forget()

    remaining_people = game.get_remaining_people()
    num_cols = 3  # Define the number of columns for the grid
    for i, person_name in enumerate(remaining_people):
        row_num = i // num_cols
        col_num = i % num_cols

        # Get the person object
        person = next((p for p in people_list if p.name == person_name), None)
        if person is not None:
            # Load and display the person's image
            image = Image.open(person.photo)
            image = image.resize((100, 100))  # Resize the image if needed
            photo = ImageTk.PhotoImage(image)

            # Create a label to display the image
            image_label = Label(window, image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection
            image_label.grid(row=row_num, column=col_num, padx=5, pady=5)  # Adjust padding as needed


def guess_name():
    action_taken = name_entry.get().lower()

    if engagement_var1.get() != 0 and engagement_var2.get() != 0 and action_taken != "select action":
        print(action_taken)
        print(engagement_var1.get())
        print(engagement_var2.get())
        with open('game_logs.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(
                [f"Engagement1: {engagement_var1.get()}",
                 f"Engagement2: {engagement_var2.get()}",
                 f"End: {action_taken}"]
            )

    if engagement_var1.get() == 0 or engagement_var2.get() == 0:
        messagebox.showinfo("Attention", "Please complete the scale!")

    elif action_taken == "select action":
        messagebox.showinfo("Attention", "Please choose an action!")

    else:
        if action_taken.lower() == "Who is it?".lower():
            messagebox.showinfo("Game over", f"It was {chosen_person.name}")
            window.quit()
        else:
            messagebox.showinfo("Game over", "Bye")
            window.quit()


def guess_attr():
    chosen_attribute = attribute_entry.get().lower()
    remove_attrib = attribute_entry.get()

    if engagement_var1.get() != 0 and engagement_var2.get() != 0 and chosen_attribute != "select attribute":

        # only print when scales are ticked
        print(f"Engagement1: {engagement_var1.get()}")
        print(f"Engagement2: {engagement_var2.get()}")
        with open('game_logs.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([f"Engagement1: {engagement_var1.get()}",
                                 f"Engagement2: {engagement_var2.get()}"])

    if engagement_var1.get() == 0 or engagement_var2.get() == 0:
        messagebox.showinfo("Attention", "Please select an engagement level!")

    elif chosen_attribute == "select attribute":
        messagebox.showinfo("Attention", "Please choose an attribute!")
    else:
        radios()
        attribute_value = getattr(chosen_person, chosen_attribute)
        attribute_value_label.config(text=f" Is the chosen person {chosen_attribute}?: {attribute_value}")
        game.guess_person(chosen_attribute, attribute_value)
        remaining_people = game.get_remaining_people()

        update_people_images()
        # update_people_label()

        print(remaining_people)
        print(f"Attribute: {chosen_attribute}, Value: {attribute_value}")
        with open('game_logs.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([f"Remaining people: {remaining_people}",
                                 f"Attribute: {chosen_attribute}",
                                 f"Value: {attribute_value}"])

        attribute_entry.set("Select attribute")
        attribute_options.remove(remove_attrib)
        attribute_entry['values'] = attribute_options

        if chosen_attribute == chosen_person.name.lower():
            messagebox.showinfo("Correct!", f"Yes, the person is {remaining_people[0]}!")
            window.quit()

        elif len(remaining_people) == 1:
            messagebox.showinfo("Game Over", f"The person is {remaining_people[0]}!")
            window.quit()


# ------------------------- UI --------------------------------------------
window = Tk()
window.title("Guess Who")
window.config(padx=50, pady=50)

# Define colors
bg_color = "#FFFFFF"  # White
label_color = "#333333"  # Dark gray
button_bg = "#4CAF50"  # Green
button_fg = "#FFFFFF"  # White
highlight_color = "#FFD700"  # Gold

# Define font
main_font = ("Arial", 12)

# Remaining people display
people_label = Label(text="", fg=label_color, font=main_font)
people_label.grid(row=0, column=0, columnspan=2)

# Guess name input - Dropdown menu using ttk.Combobox
name_label = Label(text="End game options", fg=label_color, font=main_font)
name_label.grid(row=2, column=0)

action_options = ["Who is it?", "Next"]
name_entry = ttk.Combobox(window, values=action_options, state="readonly")
name_entry.set("Select action")  # Set default value
name_entry.grid(row=2, column=1, padx=5, pady=5)

name_button = Button(text="Submit", command=guess_name, bg=button_bg, fg=button_fg)
name_button.grid(row=3, column=1, pady=5)

# Choose attribute input using ttk.Combobox
attribute_label = Label(text="Choose an attribute:", fg=label_color, font=main_font)
attribute_label.grid(row=9, column=2)

attribute_options = ["Male", "Female", "black_Haired", "red_Haired", "white_Haired", "Alice", "Bob","Charlie","Diane","Eve"]
attribute_entry = ttk.Combobox(window, values=attribute_options, state="readonly")
attribute_entry.set("Select attribute")  # Set the default value
attribute_entry.grid(row=9, column=3, padx=10, pady=10)

guess_attr_button = Button(text="Submit", command=guess_attr, bg=button_bg, fg=button_fg)
guess_attr_button.grid(row=10, column=3, pady=5)


# Search Box for Attribute Selection

def filter_attributes(event):
    query = search_var.get().lower()
    matched_attributes = [attr for attr in attribute_options if query in attr.lower()]

    attribute_entry['values'] = matched_attributes


search_label = Label(text="Search for an attribute:", fg=label_color, font=main_font)
search_label.grid(row=12, column=2)

search_var = StringVar()
search_entry = Entry(window, textvariable=search_var)
search_entry.grid(row=12, column=3, padx=10, pady=10)
search_entry.bind('<KeyRelease>', filter_attributes)

# Print: The chosen person's attribute is X (e.g., male)
attribute_value_label = Label(text="", font=main_font, fg=label_color)
attribute_value_label.grid(row=13, column=3, columnspan=2, pady=10)

# Scale for engagement
radios()

# Update remaining people
# update_people_label()
update_people_images()

window.mainloop()

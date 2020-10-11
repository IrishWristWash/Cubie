from tkinter import *
from CubieGameV4 import *
import CubieGameV4
import json


# GUI Class
class CubieHomeGUI:

    # Init function creates necessary labels, buttons and images to be displayed.
    def __init__(self, parent):
        # Creating variables to be used.

        self.parent = parent
        self.home_frame = Frame(parent, bg="white")
        self.instructions_frame = Frame(parent, bg="white")
        self.highscore_frame = Frame(parent, bg="white")
        self.play_frame = Frame(parent, bg="white")

        self.button_styling = ("Small fonts","30","bold")

        # Setting current frame as the home frame before showing it.
        self.current_frame = self.home_frame
        self.show_home()

    # Function below displays the home frame.
    def show_home(self):

        # Creating home frame and setting its attributes
        self.home_frame = Frame(self.parent, bg="white")

        # If another frame is currently active it is destroyed before the current frame is set to the home frame.
        if self.current_frame == self.instructions_frame:

            self.instructions_frame.destroy()

        if self.current_frame == self.highscore_frame:

            self.highscore_frame.destroy()

        if self.current_frame == self.play_frame:

            self.play_frame.destroy()

        self.current_frame = self.home_frame

        # Loading Cubie image from a .gif file
        self.img = PhotoImage(file="cubie_logo.gif")

        # Loading image into a label widget before packing it.
        self.img_panel = Label(self.home_frame, image=self.img, borderwidth=0)
        self.img_panel.pack(side=TOP)

        # Play button
        self.play_button = Button(self.home_frame, text="Play", bg="white", borderwidth=0, command=self.show_play_frame)
        self.play_button.configure(font=self.button_styling)
        self.play_button.pack(side=TOP)

        # Highscore button
        self.highscore_button = Button(self.home_frame, text="Highscores", bg="white", borderwidth=0, command=self.show_highscores)
        self.highscore_button.configure(font=self.button_styling)
        self.highscore_button.pack(side=TOP)

        # Instructions button
        self.instructions_button = Button(self.home_frame, text="Instructions", bg="white", borderwidth=0, command=self.show_instructions)
        self.instructions_button.configure(font=self.button_styling)
        self.instructions_button.pack(side=TOP)

        # Quit Button
        self.quit_button = Button(self.home_frame, text="Quit", bg="white", borderwidth=0, command=self.quit_cubie)
        self.quit_button.configure(font=self.button_styling)
        self.quit_button.pack(side=TOP)

        # Packing the home frame onto the GUI
        self.home_frame.pack()

    # Function below displays the instruction frame
    def show_instructions(self):

        # Creating instructions frame and settings its attributes.
        self.instructions_frame = Frame(self.parent, bg="white")

        # Removing home frame
        self.home_frame.destroy()

        # Setting the current frame as the instructions frame
        self.current_frame = self.instructions_frame

        # The instructions text is first stored within a variable to improve the flow of the code.
        self.instructions_text = "The dastardly circles have struck again! Using their immense wealth and influence " \
                                 "to hire square assassins the life of our four-cornered protagonist is in mortal" \
                                 " danger. \n\n Your task is to help him survive the assassins by controlling the" \
                                 " protagonist with the WASD and arrow keys."

        # Instructions frame labels and widgets
        self.instructions_label = Label(self.instructions_frame,bg="white", text=self.instructions_text, font=
                                        ("Small fonts", "15"), wraplength=600)
        self.back_button = Button(self.instructions_frame,font=self.button_styling, text="Back", bg="white",
                                  borderwidth=0, command=self.show_home)

        # Packing instructions frame labels and widgets onto the frame
        self.instructions_label.pack()
        self.back_button.pack()

        # Packing the instructions frame onto the GUI
        self.instructions_frame.pack()

    def show_highscores(self):

        # Creating the highscore frame
        self.highscore_frame = Frame(self.parent, bg="white")

        # Removing the home frame
        self.home_frame.destroy()

        # Setting the current frame as the highscore frame
        self.current_frame = self.highscore_frame


        # Creating a list in which the label instances will be stored
        labels = [1,2,3,4,5]

        # Opening the game dictonary file and then loading the dictionary from it
        with open('game_dictionary.txt', 'r') as json_file:
            game_data = json.load(json_file)

        # Creating lists to be displayed by the GUI from data found in the file
        top_scores = game_data["scores_and_names"][0]
        top_player_names = game_data["scores_and_names"][1]

        # For loop iterates through the aforementioned labels list, creates a new label instance for each item
        # before packing it.
        for i in range(len(labels)):

            labels[i] = Label(self.highscore_frame,bg="white", text= (str(top_player_names[i]) + ": " + str(top_scores[i])),
                              font=("Small fonts", "20", "bold"))

        # Highscore frame widgets and labels
        self.highscore_label = Label(self.highscore_frame, bg="white", text = "Highscores", font=self.button_styling)
        self.back_button = Button(self.highscore_frame, font=("Small fonts", "70", "bold"), text="Back", bg="white",
                                  borderwidth=0, command=self.show_home)

        # Packing the highscore frame widgets and labels
        self.highscore_label.pack()

        for label in labels:
            label.pack()

        self.back_button.pack()

        # Packing the highscore frame itself onto the GUI
        self.highscore_frame.pack()

    def show_play_frame(self):

        # Creating play frame
        self.play_frame = Frame(self.parent, bg="white")

        # Removing the home frame
        self.home_frame.destroy()

        # Setting the current frame as the highscore frame
        self.current_frame = self.play_frame

        # Play frame entry boxes and labels
        self.play_label = Label(self.play_frame, bg="white", text = "Settings", font=self.button_styling)
        self.player_name_label = Label(self.play_frame, bg="white", text = "Username (Max 10 characters)", font=("Small fonts", "20", "bold"))
        self.player_name_entry = Entry(self.play_frame, bd=3, font=("Small fonts", "15", "bold"))
        self.difficulty_label = Label(self.play_frame, bg="white", text = "Difficulty Level (1-10)", font=("Small fonts", "20", "bold"))
        self.difficulty_entry = Entry(self.play_frame, bd=3, font=("Small fonts", "15", "bold"))

        # Play frame buttons
        self.play_button = Button(self.play_frame, font=("Small fonts", "30", "bold"), text="Play", bg="white", borderwidth=0, command=self.play_cubie)
        self.back_button = Button(self.play_frame, font=("Small fonts", "30", "bold"), text="Back", bg="white", borderwidth=0, command=self.show_home)

        # Packing play frame widgets
        self.play_label.pack()
        self.player_name_label.pack()
        self.player_name_entry.pack()
        self.difficulty_label.pack()
        self.difficulty_entry.pack()
        self.play_button.pack(side=RIGHT)
        self.back_button.pack(side=LEFT)

        # Packing the play frame itself onto the GUI
        self.play_frame.pack()

    # Function closes/destroys the tkinter window after initializing the game state and loop
    # (if data validation is confirmed).
    def play_cubie(self):

        self.player_name = self.player_name_entry.get()

        try:
            self.difficulty = int(self.difficulty_entry.get())
        except ValueError:
            self.difficulty = 11
            self.difficulty_entry.configure(fg="red")
        # Data validation on inputs: if the player name is too long or too short the text is turned red
        # Likewise, if the difficult entered is too high or too low the textbox is turned red

        if len(self.player_name) > 10 or len(self.player_name) == 0:
            self.player_name_entry.configure(fg="red")
        if self.difficulty > 10 or self.difficulty < 1:
            self.difficulty_entry.configure(fg="red")

        # If the conditions for data validation are passed the GUI is destroyed before the game is started.
        if len(self.player_name) < 10 and 11 > self.difficulty > 0:

            self.parent.destroy()

    # Function quits from home screen if the "Quit" button is pressed
    def quit_cubie(self):

        self.parent.destroy()

    # Function will return the settings set by the user to be passed into the main game function
    def return_settings(self):

        # Tries to return the difficulty and player name however, if neither exists (when the player doesn't want to
        # play anymore) the function will return none
        try:
            return self.difficulty, self.player_name
        except AttributeError:
            return None


# Mainloop function
def home_main():
    # Naming, sizing and starting mainloop/GUI
    root = Tk()
    root.title("Cubie")
    root.geometry("700x700")
    root.configure(bg="white")
    show_label = CubieHomeGUI(root)

    root.mainloop()
    return show_label.return_settings()




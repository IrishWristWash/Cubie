from CubieGameV4 import *
from CubieHomeV4 import *

# Settings variable is created to store the options set by the user
settings = 0

# If the user quits the program settings is returned as none and the program stops
while settings is not None:
    # Settings is assigned to the settings returned by the GUI
    settings = home_main()

    # The game will only be run if game settings currently exist
    if settings is not None:
        # The main game function is called using the settings from the GUI
        game_main(settings[0], settings[1])

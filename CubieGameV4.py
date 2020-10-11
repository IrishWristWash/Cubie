# Imports
import pygame
import ctypes
import random
import json

# Defining the player class - the one included below inherits from the pygame built in sprite class.
class Player(pygame.sprite.Sprite):

    # Defining the player init function
    def __init__(self, screen_width, screen_height):

        # Initiating pygame sprite class
        pygame.sprite.Sprite.__init__(self)

        # Establishing player attributes (velocity, x & y position, etc.)
        self.player_velocity = 8
        self.dx = 1
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Creating the player sprite
        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, (255, 255, 255), self.rect)

        self.rect.x = (screen_width / 2)
        self.rect.y = (screen_height - 100)

        pygame.draw.rect(self.image, (0, 0, 0), self.rect)

    # Function below changes the x-position of the player(hence moving the player)
    def move(self, dx):

        if dx == 1:
            self.dx = 1
        elif dx == -1:
            self.dx = -1

    # Function below returns the player sprites current x position (for positioning the bullet)
    def get_x(self):

        return self.rect.x

    # The update() method is a in-built function run every time the player instance is drawn.
    # This makes it ideal for use in checking for player conditions, e.g whether the player is touching the
    # border.

    def update(self):

        if self.dx == 1:

            self.rect.x += self.player_velocity
        elif self.dx == -1:

            self.rect.x -= self.player_velocity

        # If the x position of the player is past the border of the game the x position is set to the other side.
        if self.rect.x > self.screen_width:

            self.rect.x = 0

        if self.rect.x < 0:

            self.rect.x = self.screen_width


# Defining the enemy class
class Enemy(pygame.sprite.Sprite):

    # Defining the enemy init function
    def __init__(self, enemy_sprite, player_sprites, shield_sprites, bullet_sprites, screen_width, screen_height):

        # Initiating pygame sprite class
        pygame.sprite.Sprite.__init__(self)

        # Creating misc attributes
        self.screen_height = screen_height

        # Setting sprite image as the saved png file
        self.image = enemy_sprite
        self.rect = self.image.get_rect()

        # Establishing enemy attributes (x & y position, etc).
        self.rect.x = random.randint(50, (screen_width - 50))
        self.rect.y = 0

        # Drawing the sprite
        pygame.draw.rect(self.image, (0, 0, 0), self.rect)

    # Function below checks for a player loss when an enemy sprite reaches the bottom of the screen
    def lost(self, enemy_sprites):

        # If the enemy instance's y-position is greater than the height of the screen the function returns True
        if self.rect.y > self.screen_height:
            return True

    # This function is (automatically) called whenever the sprite is drawn. It's in charge of checking
    # the sprites position and updating the game because of it (e.g player loses when enemy reaches the bottom).
    def update(self):

        # Updating y-position of the enemy sprite so that it moves.
        self.rect.y += 4


# Defining the shield class
class Shield(pygame.sprite.Sprite):

    def __init__(self,shield_sprite, player_x, screen_width, screen_height):

        # Initiating pygame sprite class
        pygame.sprite.Sprite.__init__(self)

        # Setting sprite image as the saved png file
        self.image = shield_sprite
        self.rect = self.image.get_rect()

        # Establishing enemy attributes (x & y position, etc).
        self.rect.x = player_x
        self.rect.y = (screen_height - 170)

        pygame.draw.rect(self.image, (0, 0, 0), self.rect)


# Defining the bullet class
class Bullet(pygame.sprite.Sprite):

    def __init__(self, bullet_sprite, player_x, screen_width, screen_height):
        # Initiating pygame sprite class
        pygame.sprite.Sprite.__init__(self)

        # Setting sprite image as the saved png file
        self.image = bullet_sprite
        self.rect = self.image.get_rect()

        # Fetching the current size of the bullet sprite so that it can be scaled correctly.
        self.size = self.image.get_size()

        # Scaling the bullet image down to the correct size
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/3), int(self.size[1]/3)))

        # Establishing enemy attributes (x & y position, etc).
        self.rect.x = player_x
        self.rect.y = (screen_height - 100)

        pygame.draw.rect(self.image, (0, 0, 0), self.rect)

    # Update function called whenever the bullet sprite changes it's y-position to make it move.
    def update(self):

        # Changing y-position of the bullet for movement
        self.rect.y -= 17

        # If the bullet sprite reaches the top of the screen it is deleted from the games memory
        if self.rect.y < 0:

            self.kill()


# Main loop function
def game_main(difficulty, player_name):

    # Creating user(to find native screen resolution)
    user32 = ctypes.windll.user32

    # Initiating pygame
    pygame.init()

    # Setting up screen and misc variables
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    screen_size = screen_width, screen_height
    title = "Cubie"

    # Setting display to full screen
    window = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    # Loading in the sprite images (loading them in here increases the speed at which the game can run).
    enemy_sprite = pygame.image.load('enemy_sprite.png').convert_alpha()
    shield_sprite = pygame.image.load('shield_sprite.png').convert_alpha()
    bullet_sprite = pygame.image.load('bullet_sprite.png').convert_alpha()

    # Setting the window title (Cubie)
    pygame.display.set_caption(title)

    # The following integer dictates how many enemies must be killed before the game is made more difficult
    enemy_difficulty_number = 12 - difficulty

    # Code below creates two sprite groups

    # The 'player_sprites' group contains all sprites that aid the player (shields, bullets, player sprite itself)
    # that will aid the player (and kill enemy sprites).
    player_sprites = pygame.sprite.Group()

    # The enemy sprites group contains all current (non-dead) instances of the enemy sprite.
    enemy_sprites = pygame.sprite.Group()

    # The bullet sprites group will contain all instances of the bullet sprite.
    bullet_sprites = pygame.sprite.Group()

    # The shield sprites group will contain all instances of the shield sprite.
    shield_sprites = pygame.sprite.Group()

    # Creating player & adding to its respective group
    player = Player(screen_width, screen_height)

    # Adding sprites into player_sprite group
    player_sprites.add(player)

    # Starting the game & creating font
    points_font = pygame.font.Font('Pixeboy-z8XGD.ttf', 70)
    game_over_font = pygame.font.Font('Pixeboy-z8XGD.ttf', 130)
    game_over_sub_font = pygame.font.Font('Pixeboy-z8XGD.ttf', 90)

    clock = pygame.time.Clock()
    running = True

    lost = False
    points = 0
    # Game loop
    while running:

        # Setting the maximum frame rate as 30 (per second)
        clock.tick(30)
        if not lost:

            # Fetching pygame events and checking for quit action
            for event in pygame.event.get():

                # If there is a quit action running is set as false and the game stops.
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:

                    running = False

                # Resetting if a shield has been placed (to allow another to be placed)
                shield_placed = False

                # Resetting if a bullet has been fired (to allow another to fired)
                bullet_shot = False

            # Checking if left arrow key has been pressed for movement to the left.
            if keys[pygame.K_LEFT]:
                player.move(-1)

            # Checking if right arrow key has been pressed for movement to the right.
            if keys[pygame.K_RIGHT]:
                player.move(1)

            # Checking if the space bar has been pressed to fire a bullet.
            if keys[pygame.K_SPACE]:

                # If less than 5 bullets are currently on the screen a new one will be created.
                # this makes it difficult for the player to hold down the space bar and cheat.
                # The bullet will also fire if one has not been fired yet in the current game loop.
                if len(bullet_sprites) < 6 and not bullet_shot:

                    # Adding a new bullet instance to the bullet_sprites group
                    bullet_sprites.add(Bullet(bullet_sprite, player.get_x(), screen_width, screen_height))

                    # Remembers that a bullet has now been fired in the current game loop meaning another
                    # cannot be fired until the next cycle.
                    bullet_shot = True

            # Checking if up arrow key has been pressed to place a shield.
            if keys[pygame.K_UP]:

                # Will place a new shield if there are less than the maximum currently placed and if a
                # shield has not already been placed in this cycle of the game loop
                if len(shield_sprites) < 5 and not shield_placed:

                    # Adding a new shield instance to the shield_sprites group
                    shield_sprites.add(Shield(shield_sprite, player.get_x(), screen_width, screen_height))

                    # Remembers that a shield has now been placed in the current game loop meaning another
                    # cannot be placed until the next cycle.
                    shield_placed = True

            # Creating enemy instances based on difficulty
            if random.randint(1, (200 - round(18.5 * difficulty))) == 1:
                enemy_sprites.add(Enemy(enemy_sprite,player_sprites, shield_sprites, bullet_sprites, screen_width,
                                        screen_height))

            # Checking if a bullet -> enemy collision has occurred. If so, add one point
            if len(pygame.sprite.groupcollide(enemy_sprites, bullet_sprites, True, True)) > 0:

                # Adding points based on difficulty
                points += (2 + round(difficulty/2))

            # Checking if a shield -> enemy collision has occurred. If so, add one point
            if len(pygame.sprite.groupcollide(enemy_sprites, shield_sprites, True, True)) > 0:

                # Adding points based on difficulty
                points += (1 + round(difficulty/2))

            # Checking if a player -> enemy collision has occurred. If so, add one point
            if len(pygame.sprite.groupcollide(enemy_sprites, player_sprites, True, False)) > 0:

                # Adding points based on difficulty
                points += (5 + round(difficulty/2))

            # Updating screen
            window.fill((0, 0, 0))

            # Updating sprites
            bullet_sprites.update()
            shield_sprites.update()
            enemy_sprites.update()
            player_sprites.update()

            # Drawing sprites
            enemy_sprites.draw(window)
            player_sprites.draw(window)
            bullet_sprites.draw(window)
            shield_sprites.draw(window)

            # Displaying player points
            points_text = points_font.render(str(points), True, (255, 0, 0))
            window.blit(points_text, (5, 5))

            # Checking if any enemy instance has gotten to the bottom of the screen. If so, lost is set to true.
            for enemy in enemy_sprites:

                if enemy.lost(enemy_sprites):

                    lost = True

        # Once the player has lost the game is stopped.
        if lost:

            # Removing sprites from groups
            bullet_sprites.empty()
            shield_sprites.empty()
            enemy_sprites.empty()
            player_sprites.empty()

            # Settings points as an integer
            points = int(points)

            # Opening the json file to retrieve player names and highscores.
            with open("game_dictionary.txt", "r") as highscores_json:

                data = json.load(highscores_json)

            # Creating lists from data found in the file
            top_scores = data["scores_and_names"][0]
            top_player_names = data["scores_and_names"][1]

            # If the player score is higher than the lowest score in the current top scores the player has created a new
            # highscore.
            if int(points) > int(min(top_scores)):

                # Sorting the top scores
                top_scores_sorted = sorted(top_scores)

                # Iterating the top scores list to find what rank the new highscore is
                x = 0
                while True:
                    x += 1
                    print(top_scores[x])

                    if points > int(top_scores_sorted[x]):
                        top_scores[x] = points
                        top_player_names[x] = player_name
                        break

                # Cretaing the new highscores array that will be stored in the json file.
                data["scores_and_names"][0] = top_scores
                data["scores_and_names"][1] = top_player_names

                # Opening the json file to overwrite the current information
                with open('game_dictionary.txt', "w") as highscores_json:
                    print(data, "array json")
                    json.dump(data, highscores_json)

                # Changing displayed text
                game_over_message = "New Highscore!"

            # The player has not achieved a new highscore and will therefore only see a simple "Game Over!" screen.
            elif int(points) < int(min(top_scores)):
                game_over_message = "Game Over!"

            # Displaying the game over text using fonts previously set.
            game_over_text = game_over_font.render(game_over_message, True, (255, 0, 0))
            game_over_text_sub = game_over_sub_font.render("Score: " + str(points), True, (255, 0, 0))
            space_to_cont_text = game_over_sub_font.render("(Space to continue)", True, (255, 0, 0))

            # Actually drawing the text to the game window
            window.blit(game_over_text, (screen_width / 2 - 300, screen_height / 2))
            window.blit(game_over_text_sub, (screen_width / 2 - 300, screen_height / 2 - 70))
            window.blit(space_to_cont_text, (screen_width / 2 - 300, screen_height / 2 + 70))

            # Fetching pygame events and checking for quit action
            for event in pygame.event.get():

                # If there is a quit action running is set as false and the game stops.
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE]:

                    running = False

        # Updating the display
        pygame.display.flip()

    # Quitting pygame (and stopping the game) once the game is over.
    pygame.quit()


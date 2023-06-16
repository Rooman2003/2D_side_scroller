# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\Home\\Desktop\\pygame\\images\\missile.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

   # Move the sprite based on the speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            

# Define the cloud object by extending pygame.sprite.Spirte
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\Home\\Desktop\\pygame\\images\\cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # the starting position is randomly generated
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
    # Move the cloud based on constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        try:
            self.rect.move_ip(-5,0)
            if self.rect.right < 0:
                self.kill()
        except pygame.error as e:
            print("An error occurred during Pygame initialization:", str(e))

# Setup for music and sound playback. Defaults are okay.
pygame.mixer.init()

# Intialize pygame
pygame.init()

# Set up the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by constants SCREEN_WIDTH AND SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom event for adding a new enemy and new cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Instantiate the player. Will be rectangle initially
player = Player()

# Create groups to hold enemy sprites and all sprites
# -enemies is used for collision detection and position updates
# -all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player) # to add a sprite to group is used add method with Object Player

# Load and play background music
# Sound source: Chris Bailey = artist Tripnet
# License: https://creativecommons.org/licenses/by/3.0
pygame.mixer.music.load("C:\\Users\\Home\\Desktop\\pygame\\sounds\\sky_dodge_theme.ogg")
try:
    pygame.mixer.music.play(loops=-1)  # -1 is infinite loop
    pygame.mixer.music.set_volume(0.1)
except pygame.error as e:
    print("An error occurred while playing the music:", str(e))

# Load all sound files
# Sound source: Chris Bailey
move_up_sound = pygame.mixer.Sound("C:\\Users\\Home\\Desktop\\pygame\\sounds\\jet_up.ogg")
move_down_sound = pygame.mixer.Sound("C:\\Users\\Home\\Desktop\\pygame\\sounds\\Jet_down.ogg")
collision_sound = pygame.mixer.Sound("C:\\Users\\Home\\Desktop\\pygame\\sounds\\Boom.ogg")

# Adjust volume of the sounds
move_up_sound.set_volume(0.6)
move_down_sound.set_volume(0.6)
collision_sound.set_volume(1.0)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the ESCAPE key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud and add to sprite group
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input and then update
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the enemy position abd clouds
    enemies.update()
    clouds.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Update player sprite based on user keypresses
    player.update(pressed_keys)


    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()

        # Stop any moving sounds and play the collision
        move_up_sound.stop()
        move_down_sound.stop()
        pygame.mixer.music.stop()
        pygame.time.delay(50)
        collision_sound.play()
        pygame.time.delay(500)

        # Stop the loop
        running = False

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update the display
    pygame.display.flip()

    # Ensure the program maintains a maximum rate of 30 fps
    clock.tick(30)

# All done! Stop and quit the mixer

pygame.mixer.quit()

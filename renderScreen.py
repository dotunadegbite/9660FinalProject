import pygame
import os

BLACK  = (   0,   0,   0)
WHITE  = ( 255, 255, 255)


pygame.init()
screen = pygame.display.set_mode([256, 256])

input_path = "C:\\Users\\Dotun Local\\Documents\\9.660Sprites\\"

for (dirpath, dirnames, filenames) in os.walk(input_path):
    for filename in filenames:
        if filename.endswith(".png"):
            name_split = filename.split("_")
            if "player" in name_split:
                player = pygame.image.load(input_path + filename)
            elif len(name_split) == 1:
                asteroid = pygame.image.load(input_path + filename)
            elif "asteroid.png" in name_split and len(name_split) > 1:
                grey_asteroid = pygame.image.load(input_path + filename)
            elif "laser" in name_split:
                if "yellow" in name_split:
                    yellow_laser = pygame.image.load(input_path + filename)
                elif "blue" in name_split:
                    blue_laser = pygame.image.load(input_path + filename)
                elif "red" in name_split:
                    red_laser = pygame.image.load(input_path + filename)
                elif "green" in name_split:
                    green_laser = pygame.image.load(input_path + filename)
            elif "ship" in name_split and "small" in name_split:
                if "red" in name_split:
                    red_ship = pygame.image.load(input_path + filename)
                elif "blue" in name_split:
                    blue_ship = pygame.image.load(input_path + filename)
                elif "green" in name_split:
                    green_ship = pygame.image.load(input_path + filename)

output_path = "C:\\Users\\Dotun Local\\Dropbox (MIT)\\Classwork\\9.660\\project\\Screenshots"
done = False

all_sprites = pygame.sprite.Group()

while not done:
    imagex = 50
    imagey = 50
    screen.fill(BLACK)
    screen.blit(green_ship, (imagex, imagey))
    pygame.display.flip()
    pygame.display.update()
    pygame.image.save(screen, output_path + "\\test.png")
    done = True
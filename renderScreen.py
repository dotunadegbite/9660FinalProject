import pygame
import os

BLACK  = (   0,   0,   0)
WHITE  = ( 255, 255, 255)


pygame.init()
screen = pygame.display.set_mode([256, 256])

input_path = "9.660Sprites/"

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

output_path = "Screenshots/"
done = False

all_sprites = pygame.sprite.Group()

import numpy as np
import matplotlib.pyplot as plt
latent_state = np.array([[4, 0, 0, 4, 0],
                         [0, 1, 1, 0, 0],
                         [0, 1, 0, 0, 0],
                         [3, 0, 0, 5, 0],
                         [0, 2, 0, 0, 0]])

plt.imshow(latent_state)
plt.show()


num_to_sprite = {1: grey_asteroid,
                 2: player,
                 3: green_laser,
                 4: red_ship,
                 5: red_laser}


for x in range(5):
    for y in range(5):
        sprite = latent_state[x, y]
        imagex = x * 50
        imagey = y * 50
        screen.fill(BLACK)
        all_sprites.add()
        screen.blit(sprite, (imagex, imagey))
pygame.display.flip()
pygame.display.update()

pygame.image.save(screen, output_path + "test.png")

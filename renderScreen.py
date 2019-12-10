import pygame
import os
import numpy as np
os.environ["SDL_VIDEODRIVER"] = "dummy"

from generator import get_latent, latent_to_one_hot
BLACK  = (   0,   0,   0)
WHITE  = ( 255, 255, 255)
SCREEN_SIZE = [256, 256]

class GameObject(pygame.sprite.Sprite):

    def __init__(self,x,y,sprite):

        super().__init__()

        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

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
sprite_locations = []


""" latent_state = np.array([[4, 0, 0, 4, 0],
                         [0, 1, 1, 0, 0],
                         [0, 1, 0, 0, 0],
                         [3, 0, 0, 5, 0],
                         [0, 2, 0, 0, 0]]) """


num_to_sprite = {1: grey_asteroid,
                 2: player,
                 3: green_laser,
                 4: red_ship,
                 5: red_laser}

def get_sprite(sprite_num):
    if sprite_num == 1:
        return grey_asteroid
    elif sprite_num == 2:
        return player
    elif sprite_num == 3:
        return green_laser
    elif sprite_num == 4:
        return red_ship
    elif sprite_num == 5:
        return red_laser

def check_bounds(x,y,sprite_rect):
    newX = x
    newY = y
    # print("Height: " + str(sprite_rect.height))
    # print("Width: " + str(sprite_rect.width))
    if (x + sprite_rect.width > SCREEN_SIZE[0]):
        newX = (x + sprite_rect.width) - SCREEN_SIZE[0]
        newX += x
    if (y + sprite_rect.height > SCREEN_SIZE[1]):
        newY = (y + sprite_rect.height) - SCREEN_SIZE[1]
        print("Diff: " + str(newY))
        newY = y - newY
    return(newX,newY)


def render_from_latent(latent_state, path):
    done = False
    screen.fill(BLACK)
    all_sprites = pygame.sprite.Group()
    for x in range(5):
        for y in range(5):
            if latent_state[x, y] != 0:
                sprite = num_to_sprite[latent_state[x, y]]
                sprite_rect = sprite.get_rect()
                # print("Name of: " + str(latent_state[x,y]))
                center = ((x * 50) + 25, (y * 50) + 25)
                realX = center[0] - np.ceil(sprite_rect.width / 2)
                realY = center[1] - np.ceil(sprite_rect.height / 2)
                # bounds = check_bounds(realY, realX, sprite_rect)
                imagex = realY + 3
                imagey = realX + 3
                # print("Latent State: " + str((x,y)))
                # print("Rendered " + str((realX, realY)))
                # print("Adjusted " + str(bounds))

                game_object = GameObject(imagex, imagey, sprite)
                all_sprites.add(game_object)

    while not done:
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.update()

        pygame.image.save(screen, path)
        # stimulus = pygame.surfarray.array3d(screen)
        # stimulus = np.moveaxis(stimulus, 0, 1)
        #
        # # print("Screen: ",x.shape)
        # # from PIL import Image
        # # Image.fromarray(x).show()
        # np.save(path, stimulus)
        # np.save(label_directory + str(i) + ".npy", latent_state)
        done = True

stimulus_directory = "./data/stimuli/"
label_directory = "./data/labels/"

# for i in range(1000):
#     latent_state = get_latent()
#     label = latent_to_one_hot(latent_state)
#     done = False
#     screen.fill(BLACK)
#     all_sprites = pygame.sprite.Group()
#     for x in range(5):
#         for y in range(5):
#             if latent_state[x,y] != 0 :
#                 sprite = num_to_sprite[latent_state[x,y]]
#                 sprite_rect = sprite.get_rect()
#                 # print("Name of: " + str(latent_state[x,y]))
#                 center = ((x * 50) + 25, (y * 50) + 25)
#                 realX = center[0] - np.ceil(sprite_rect.width / 2)
#                 realY = center[1] - np.ceil(sprite_rect.height / 2)
#                 #bounds = check_bounds(realY, realX, sprite_rect)
#                 imagex = realY + 3
#                 imagey = realX + 3
#                 # print("Latent State: " + str((x,y)))
#                 # print("Rendered " + str((realX, realY)))
#                 #print("Adjusted " + str(bounds))
#
#                 game_object = GameObject(imagex, imagey, sprite)
#                 all_sprites.add(game_object)
#
#     while not done:
#         screen.fill(BLACK)
#         all_sprites.draw(screen)
#         pygame.display.update()
#
#         pygame.image.save(screen, output_path + "test" + str(i) + ".png")
#         stimulus = pygame.surfarray.array3d(screen)
#         stimulus = np.moveaxis(stimulus, 0, 1)
#
#         # print("Screen: ",x.shape)
#         # from PIL import Image
#         # Image.fromarray(x).show()
#         np.save(stimulus_directory + str(i) + ".npy", stimulus)
#         np.save(label_directory + str(i) + ".npy", latent_state)
#         done = True


"""         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True """
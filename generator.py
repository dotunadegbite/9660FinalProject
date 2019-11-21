import numpy as np
import pyro
import torch
import torch.distributions


"""
First, we defined a 5x5 grid to represent the latent space, where each cell can 
contain a value indicating one of the 5 game objects or a value indicating an empty 
cell. This represents perhaps the most intuitive human understanding of the state-space
 here (as opposed to understanding it as a collection of 2^16 pixels).

Objects:
“Empty” : 0
*Asteroid : 1
Player Ship : 2
*Player Laser : 3
*Enemy Ship : 4
*Enemy Laser : 5

Note: We introduced the following additional constraints to our latent space to make it more “space invaders”-esque.
- At most one object can be present at a time at each cell in the grid
- Exactly one player ship must be on the grid
- The player ship can only be on the bottom row of the grid
- Enemy ships can only be on the top row of the grid
- Asteroids cannot be located in the bottom two rows or the top row of the grid
Laser constraints:
- Any open spaces in middle 3 rows, proportional to amount of ships 
"""


def get_latent(enemy_ship_bernoulli_p=0.4,
               enemy_laser_bernoulli_p_base=0.05,
               asteroid_bernoulli_p=0.4,
               player_laser_bernoulli_p=1/15):

    latent = np.zeros((5, 5), dtype=int)

    # Exactly one player ship must be on the grid
    # The player ship can only be on the bottom row of the grid
    player_pos = torch.distributions.Categorical(torch.tensor([i / 5 for i in range(1, 6)])).sample()
    latent[4, player_pos] = 2

    # Enemy ships can only be on the top row of the grid
    enemy_ship_dist = torch.distributions.Bernoulli(enemy_ship_bernoulli_p)
    latent[0, :] = 4 * enemy_ship_dist.sample((5,))

    # # Asteroids cannot be located in the bottom two rows or the top row of the grid
    asteroid_dist = torch.distributions.Bernoulli(asteroid_bernoulli_p)
    latent[1:3, :] = 1 * asteroid_dist.sample((2, 5))

    # Lasers: Any open spaces in middle 3 rows, proportional to amount of ships
    num_enemy_ships = np.sum(latent[0] == 4)
    enemy_laser_dist = torch.distributions.Bernoulli(enemy_laser_bernoulli_p_base * num_enemy_ships)
    sample = 5 * enemy_laser_dist.sample((3, 5))
    latent[1:4, :] = (sample * torch.Tensor(latent[1:4, :] == 0)) + torch.Tensor(latent[1:4, :]) # must be empty already

    player_laser_dist = torch.distributions.Bernoulli(player_laser_bernoulli_p)
    psample = 3 * player_laser_dist.sample((3, 5))
    latent[1:4, :] = (psample * torch.Tensor(latent[1:4, :] == 0)) + torch.Tensor(latent[1:4, :])

    return latent

""" import matplotlib.pyplot as plt
for _ in range(10):
    plt.imshow(get_latent(), vmin=0, vmax=5)
    plt.colorbar()
    plt.show() """

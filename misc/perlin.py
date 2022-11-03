import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import random
import time

game_x, game_y = 400,400
octave = random.randrange(1, 30)

noise = PerlinNoise(octaves=octave, seed=random.randrange(0, 100000)) # random.randrange(0, 100000)

pic = [[noise([i/(game_x*0.5), j/(game_y*1.7)]) for j in range(game_x)]for i in range(game_y)]

def generatePerlin():
    for i in range(len(pic)):
        for j in range(len(pic[i])):
            #" .:-=+*#%@"
            if pic[i][j] < -0.5:
                pic[i][j] = " " # " "
            elif pic[i][j] >= -0.5 and pic[i][j] < -0.4:
                pic[i][j] = "." # .
            elif pic[i][j] >= -0.4 and pic[i][j] < -0.3:
                pic[i][j] = "." # .
            elif pic[i][j] >= -0.3 and pic[i][j] < -0.2:
                pic[i][j] = ":" # -
            elif pic[i][j] >= -0.2 and pic[i][j] < -0.1:
                pic[i][j] = "-" # -
            elif pic[i][j] >= -0.1 and pic[i][j] < 0:
                pic[i][j] = "=" # =
            elif pic[i][j] >= 0 and pic[i][j] < 0.1:
                pic[i][j] = "+" # +
            elif pic[i][j] >= 0.1 and pic[i][j] < 0.2:
                pic[i][j] = "*" # *
            elif pic[i][j] >= 0.2 and pic[i][j] < 0.3:
                pic[i][j] = "#" # #
            elif pic[i][j] >= 0.3 and pic[i][j] < 0.4:
                pic[i][j] = "%" # %
            elif pic[i][j] >= 0.4 and pic[i][j] < 0.5:
                pic[i][j] = "@" # @
            elif pic[i][j] > 0.5:
                pic[i][j] = "@" # @


    for i in range(len(pic)):
        for j in range(len(pic[i])):
            print(pic[i][j], end='')
        print('')
        
generatePerlin()
print(f"Octave: {octave}")

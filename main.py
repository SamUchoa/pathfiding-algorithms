import pygame 
import numpy as np
import graphs

pygame.init()

height = 600
width = 1200
background = "#0b3142"

grafo = np.array([0])
teste = graphs.Graph(grafo)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pathfinding")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill(background)

    pygame.display.update()

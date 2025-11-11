import pygame 
import numpy as np
import graphs

pygame.init()

height = 600
width = 1200
padding = 200

background = "#0b3142"
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pathfinding")

grafo = np.array([[0,1,1,0],
                  [1,0,0,1],
                  [1,0,0,1],
                  [0,1,1,0]])

teste = graphs.Graph(grafo)
position_x = np.random.randint(padding, width - padding, size=(teste.vertices_number,1))
position_y = np.random.randint(padding, height - padding, size=(teste.vertices_number,1))

positions = np.hstack((position_x, position_y))
colors = np.array([[255,0,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]])

def draw_graph(graph: graphs.Graph, positions: np.ndarray, colors: np.ndarray):
    for row in range(graph.vertices_number):
        vertex_color = colors[row,:].tolist()
        vertex_position = positions[row,:].tolist()

        pygame.draw.circle(screen, vertex_color, vertex_position, 10)

        for col in range(graph.vertices_number):
            item = graph.adjacency_matrix[row,col]
            if col >= row and item:
                pygame.draw.line(screen, vertex_color,  positions[row].tolist(), positions[col].tolist(), 5)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(background)

    draw_graph(teste, positions, colors)

    pygame.display.update()

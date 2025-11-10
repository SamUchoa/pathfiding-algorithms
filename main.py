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
                  [1,0,0,0],
                  [0,1,1,0]])

teste = graphs.Graph(grafo)
position_x = np.random.randint(padding, width - padding, size=(teste.vertices_number,1))
position_y = np.random.randint(padding, height - padding, size=(teste.vertices_number,1))

positions = np.hstack((position_x, position_y))

def draw_graph(graph: graphs.Graph, positions: np.ndarray):
    for vertex in range(teste.vertices_number):
        pygame.draw.circle(screen, "white", positions[vertex,:].tolist(), 10)

        vertex_edges = graph.adjacency_matrix[vertex,:].nonzero()[0]
        for edge in vertex_edges:
            pygame.draw.line(screen,"white", positions[vertex].tolist(),positions[edge].tolist(), 5)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(background)

    draw_graph(teste, positions)            

    pygame.display.update()

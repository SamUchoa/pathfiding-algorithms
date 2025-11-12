import pygame 
import numpy as np
import graphs

pygame.init()

height = 600
width = 1200
padding = 200

background = "#0b3142"
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Pathfinding")

adjacency_matrix = np.array([[0,1,1,0],
                             [1,0,0,1],
                             [1,0,0,1],
                             [0,1,1,0]])

graph = graphs.Graph(adjacency_matrix)
position_x = np.random.randint(padding, width - padding, size=(graph.vertices_number,1))
position_y = np.random.randint(padding, height - padding, size=(graph.vertices_number,1))

positions = np.hstack((position_x, position_y))
colors = np.array([[255,0,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]])

"""
0 - Add vertex
1 - Move vertex
2 - Add edge
"""
modes = [0, 1, 2]
current_mode = modes[0]

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
    mouse_pos = pygame.mouse.get_pos()

    screen.fill(background)

    draw_graph(graph, positions, colors)
    print(graph.vertices_number, graph.edges_number)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if current_mode == modes[0]:
                graph.add_vertex()
                colors = np.vstack((colors, [255,255,255,255]))
                positions = np.vstack((positions, mouse_pos))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_mode = modes[0]
            if event.key == pygame.K_2:
                current_mode = modes[1]
            if event.key == pygame.K_3:
                current_mode = modes[2]
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

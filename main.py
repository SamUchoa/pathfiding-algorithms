import pygame 
import numpy as np
import draw_graphs
import graphs
import algorithms

pygame.init()

height = 600
width = 1200
padding = 200

node_radius = 10

background = "#0b3142"
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Pathfinding")

shining_surface = pygame.image.load("light.png").convert_alpha()
shining_small = pygame.transform.scale(shining_surface, (50, 50))  

adjacency_matrix = np.array([
#   0  1  2  3  4  5  6  7  8  9
    [0, 4, 0, 0, 9, 0, 0, 0, 0, 0],  # 0
    [4, 0, 3, 0, 0, 7, 0, 0, 0, 0],  # 1
    [0, 3, 0, 5, 0, 0, 8, 0, 0, 0],  # 2
    [0, 0, 5, 0, 2, 0, 0, 6, 0, 0],  # 3
    [9, 0, 0, 2, 0, 4, 0, 0, 7, 0],  # 4
    [0, 7, 0, 0, 4, 0, 3, 0, 0, 5],  # 5
    [0, 0, 8, 0, 0, 3, 0, 6, 0, 9],  # 6
    [0, 0, 0, 6, 0, 0, 6, 0, 5, 0],  # 7
    [0, 0, 0, 0, 7, 0, 0, 5, 0, 2],  # 8
    [0, 0, 0, 0, 0, 5, 9, 0, 2, 0],  # 9
])

#adjacency_matrix = np.array([[0,1,1,0],
#                            [1,0,0,1],
#                            [1,0,0,1],
#                            [0,1,1,0]])

graph = graphs.Graph(adjacency_matrix)
position_x = np.random.randint(padding, width - padding, size=(graph.vertices_number,1))
position_y = np.random.randint(padding, height - padding, size=(graph.vertices_number,1))

positions = np.hstack((position_x, position_y))

graph_draw_handler = draw_graphs.GraphFigure(positions, node_radius, graph.edges_number)

##
a_star_gen = algorithms.a_star_step(
    graph.adjacency_matrix,
    start=0,
    goal=7,
    heuristic=lambda x: 0,
    graph_draw_handler=graph_draw_handler
)
a_star_finished = False
delay_ms = 100  
last_step_time = 0
##

while True:
    mouse_pos = pygame.mouse.get_pos()

    if graph_draw_handler.mouse_attached["is_attached"]:
        index = graph_draw_handler.mouse_attached["vertex"]
        graph_draw_handler.rects[index].center = mouse_pos

    # TODO: Check responsabilities and principles
    if graph_draw_handler.new_edge[0] >= 0 and graph_draw_handler.new_edge[1] >= 0:
        graph.add_edge(*graph_draw_handler.new_edge)
        graph_draw_handler.new_edge = np.array((-1,-1))

    #print(graph_draw_handler.edge_colors)

    screen.fill(background)

    graph_draw_handler.draw_graph(graph, screen, shining_small)
    ##
    
    current_time = pygame.time.get_ticks()

    if not a_star_finished and current_time - last_step_time >= delay_ms:
        last_step_time = current_time
        try:
            step = next(a_star_gen)
        except StopIteration:
            a_star_finished = True
    ##
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if graph_draw_handler.current_mode == graph_draw_handler.modes[0]:
                graph.add_vertex()

                error_margin = node_radius * 20
                rect = pygame.Rect((0,0), (error_margin, error_margin))
                rect.center = mouse_pos
                graph_draw_handler.rects.append(rect)
                graph_draw_handler.vertex_colors = np.vstack((graph_draw_handler.vertex_colors, [255]*3))

            if graph_draw_handler.current_mode == graph_draw_handler.modes[1]:
                graph_draw_handler.attach_mouse(mouse_pos)

            if graph_draw_handler.current_mode == graph_draw_handler.modes[2]:
                graph_draw_handler.add_edge(mouse_pos)


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                graph_draw_handler.current_mode = graph_draw_handler.modes[0]
            if event.key == pygame.K_2:
                graph_draw_handler.current_mode = graph_draw_handler.modes[1]
            if event.key == pygame.K_3:
                graph_draw_handler.current_mode = graph_draw_handler.modes[2]
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

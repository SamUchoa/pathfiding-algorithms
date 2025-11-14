import time
import pygame 
import numpy as np
import draw_graphs
import graphs

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

adjacency_matrix = np.array([[0,1,1,0],
                             [1,0,0,1],
                             [1,0,0,1],
                             [0,1,1,0]])

graph = graphs.Graph(adjacency_matrix)
position_x = np.random.randint(padding, width - padding, size=(graph.vertices_number,1))
position_y = np.random.randint(padding, height - padding, size=(graph.vertices_number,1))

positions = np.hstack((position_x, position_y))

graph_draw_handler = draw_graphs.GraphFigure(positions, node_radius, graph.edges_number)
graph_draw_handler.change_edge_color(1,[0,0,0])

while True:
    mouse_pos = pygame.mouse.get_pos()

    if graph_draw_handler.mouse_attached["is_attached"]:
        index = graph_draw_handler.mouse_attached["vertex"]
        graph_draw_handler.rects[index].center = mouse_pos

    if graph_draw_handler.new_edge[0] >= 0 and graph_draw_handler.new_edge[1] >= 0:
        graph.add_edge(*graph_draw_handler.new_edge)
        graph_draw_handler.new_edge = np.array((-1,-1))

    print(graph_draw_handler.edge_colors)

    screen.fill(background)

    graph_draw_handler.draw_graph(graph, screen, shining_small)
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

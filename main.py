import pygame 
import numpy as np
import draw_graphs
import graphs
import algorithms

pygame.init()

height = 600
width = 1200
padding = 100

node_radius = 10

background = "#0b3142"
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Pathfinding")

shining_surface = pygame.image.load("assets/light.png").convert_alpha()
shining_small = pygame.transform.scale(shining_surface, (50, 50))  

icons_size = 50
icons_distance = 10

add_vertex_icon = pygame.image.load("assets/add_vertex.png").convert_alpha()
move_vertex_icon = pygame.image.load("assets/move_vertex.png").convert_alpha()
add_edge_icon = pygame.image.load("assets/add_edge.png").convert_alpha()
add_start_icon = pygame.image.load("assets/add_start.png").convert_alpha()
add_end_icon = pygame.image.load("assets/add_end.png").convert_alpha()

selected_icon = pygame.image.load("assets/selected.png").convert_alpha()
selected_large = pygame.transform.scale(selected_icon, (icons_size, icons_size))
selected_rect = selected_large.get_rect()

icons = [
    add_end_icon,
    add_start_icon,
    add_edge_icon,
    move_vertex_icon,
    add_vertex_icon,
]


def config_icons(icons: list[pygame.Surface], icons_size: float):
    resized = []
    for i in icons:
        resized.append(pygame.transform.scale(i, (icons_size, icons_size)))
    return resized

def config_icon_rects(surfaces: list[pygame.Surface], icons_size: float, start_pos: int, y_pos: int, icons_distance: int):
    rects = []
    position = start_pos
    for s in surfaces:
        rect = s.get_rect()
        rect.center = (position, y_pos)
        rects.append(rect)
        position -= icons_size + icons_distance
    return rects

icons = config_icons(icons, icons_size)
icon_rects = config_icon_rects(icons, icons_size, width - padding, height - padding, 10)

icons = icons[::-1]
icon_rects = icon_rects[::-1]


adjacency_matrix = np.array([
#    0  1  2  3  4  5  6  7  8  9
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
#                             [1,0,0,1],
#                             [1,0,0,1],
#                             [0,1,1,0]])

graph = graphs.Graph(adjacency_matrix)
position_x = np.random.randint(padding, width - padding, size=(graph.vertices_number,1))
position_y = np.random.randint(padding, height - padding, size=(graph.vertices_number,1))

positions = np.hstack((position_x, position_y))

graph_draw_handler = draw_graphs.GraphFigure(positions, node_radius, graph.edges_number)

##
delay_ms = 100  
last_step_time = 0
##

path_start = -1
path_destination = -2

proceed_algorithm = False

while True:
    mouse_pos = pygame.mouse.get_pos()

    if graph_draw_handler.mouse_attached["is_attached"]:
        index = graph_draw_handler.mouse_attached["vertex"]
        graph_draw_handler.rects[index].center = mouse_pos

    # TODO: Check responsabilities and principles
    if None not in graph_draw_handler.new_edge:
        if graph_draw_handler.new_edge[0] >= 0 and graph_draw_handler.new_edge[1] >= 0:
            graph.add_edge(*graph_draw_handler.new_edge)
            graph_draw_handler.new_edge = np.array((-1,-1))

    #print(graph_draw_handler.edge_colors)

    screen.fill(background)

    graph_draw_handler.draw_graph(graph, screen, shining_small)
    if path_start >= 0:
        graph_draw_handler.vertex_colors[path_start,:] = [0,0,0]
    if path_destination >= 0:
        graph_draw_handler.vertex_colors[path_destination,:] = [0,0,0]
    ##
    current_time = pygame.time.get_ticks()

    if proceed_algorithm and current_time - last_step_time >= delay_ms:
        last_step_time = current_time
        try:
            step = next(a_star_gen)
        except StopIteration:
            proceed_algorithm = False
    ##

    for i, r in enumerate(icon_rects):
        if i == graph_draw_handler.current_mode:
            print(i,r.center)
            selected_rect.center = r.center
            screen.blit(selected_large, selected_rect)
        screen.blit(icons[i], r)

    #print(path_start, path_destination)
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

            if graph_draw_handler.current_mode == graph_draw_handler.modes[3] and not proceed_algorithm:
                selected_node = graph_draw_handler.get_node_from_mouse(mouse_pos)
                if path_start != path_destination and selected_node:
                    path_start = selected_node
                
            if graph_draw_handler.current_mode == graph_draw_handler.modes[4] and not proceed_algorithm:
                selected_node = graph_draw_handler.get_node_from_mouse(mouse_pos)
                if path_start != path_destination and selected_node:
                    path_destination = selected_node

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                graph_draw_handler.current_mode = graph_draw_handler.modes[0]
            if event.key == pygame.K_2:
                graph_draw_handler.current_mode = graph_draw_handler.modes[1]
            if event.key == pygame.K_3:
                graph_draw_handler.current_mode = graph_draw_handler.modes[2]
            if event.key == pygame.K_4:
                graph_draw_handler.current_mode = graph_draw_handler.modes[3]
            if event.key == pygame.K_5:
                graph_draw_handler.current_mode = graph_draw_handler.modes[4]
            if event.key == pygame.K_SPACE and path_destination >= 0 and path_start >= 0:
                a_star_gen = algorithms.a_star_step(
                    graph.adjacency_matrix,
                    start=path_start,
                    goal=path_destination,
                    heuristic=lambda x: 0,
                    graph_draw_handler=graph_draw_handler
                )
                proceed_algorithm = True
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

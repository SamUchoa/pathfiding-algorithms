import pygame
import numpy as np
import graphs


class GraphFigure:
    def __init__(self, positions: np.ndarray, node_radius: int, edges_number: int):
        self.node_radius = node_radius
        self.modes = [0, 1, 2]
        self.current_mode = self.modes[0]
        self.new_edge = np.array((-1, -1))
        self.mouse_attached = {"is_attached": False, "vertex": -1}
        self.rects = []

        #self.last_update = 0.0

        self.edges = []
        
        vertex_number = np.size(positions, axis=0)
        self.vertex_colors = np.array([[255,255,255]]*vertex_number)
        self.edge_colors = np.array([[255,255,255]]*edges_number)


        for position in positions:
            rect = pygame.Rect((0,0), (self.node_radius, self.node_radius))
            rect.center = position
            self.rects.append(rect)

    def draw_graph(self, graph: graphs.Graph, screen: pygame.Surface, selected_surface: pygame.Surface):
        self.edges = []
        selected_rect = selected_surface.get_rect()
        for row in range(graph.vertices_number):
            vertex_color = self.vertex_colors[row,:].tolist()
            vertex_position = self.rects[row].center


            if self.new_edge[0] >= 0 and self.new_edge[0] == row:
                selected_rect.center = vertex_position
                screen.blit(selected_surface, selected_rect)
            for col in range(graph.vertices_number):
                item = graph.adjacency_matrix[row,col]
                if col >= row and item:
                    position = self.rects[col].center


                    self.edges.append((row, col))
                    edge_index = len(self.edges) - 1
                    edge_color = self.edge_colors[edge_index,:]

                    pygame.draw.line(screen, edge_color,  vertex_position, position, 5)

            pygame.draw.circle(screen, vertex_color, vertex_position, self.node_radius)

    def add_edge(self, mouse_pos: tuple[int, int]):
        for index, rect in enumerate(self.rects):
            if rect.collidepoint(mouse_pos):
                self.new_edge = self.check_new_edge(index)

    def check_new_edge(self, end: int):
        if end in self.new_edge:
            return self.new_edge
        if self.new_edge[0] < 0:
            return np.array((end, self.new_edge[1]))
        elif self.new_edge[0] >= 0:
            self.edge_colors = np.vstack((self.edge_colors, (255,255,255)))
            return np.array((self.new_edge[0], end))

    def change_edge_color(self, index: int, color: list[float]):
        self.edge_colors[index,:] = color

    def set_edge_color_by_vertices(self, u: int, v: int, color: list[int]):
        for i, (a, b) in enumerate(self.edges):
            if (a == u and b == v) or (a == v and b == u):
                self.change_edge_color(i, color)
                break


    def attach_mouse(self, mouse_pos: tuple[int, int]):
        if self.mouse_attached["is_attached"]:
            self.mouse_attached["is_attached"] = False
            self.mouse_attached["vertex"] = -1
            return
        for index, rect in enumerate(self.rects):
            if rect.collidepoint(mouse_pos):
                self.mouse_attached["is_attached"] = True
                self.mouse_attached["vertex"] = index

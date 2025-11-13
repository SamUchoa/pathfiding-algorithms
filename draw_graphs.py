import pygame
import numpy as np
import graphs


class GraphFigure:
    def __init__(self, positions: np.ndarray, node_radius: int):
        self.node_radius = node_radius
        self.modes = [0, 1, 2]
        self.current_mode = self.modes[0]
        self.new_edge = np.array((-1, -1))
        self.mouse_attached = {"is_attached": False, "vertex": -1}
        self.rects = []

        for position in positions:
            rect = pygame.Rect((0,0), (self.node_radius, self.node_radius))
            rect.center = position
            self.rects.append(rect)

    def draw_graph(self, graph: graphs.Graph, colors: np.ndarray, screen: pygame.Surface):
        for row in range(graph.vertices_number):
            vertex_color = colors[row,:].tolist()
            vertex_position = self.rects[row].center

            pygame.draw.circle(screen, vertex_color, vertex_position, self.node_radius)

            for col in range(graph.vertices_number):
                item = graph.adjacency_matrix[row,col]
                if col >= row and item:
                    position = self.rects[col].center
                    pygame.draw.line(screen, vertex_color,  vertex_position, position, 5)

    def add_edge(self, mouse_pos: tuple[float]):
        for index, rect in enumerate(self.rects):
            if rect.collidepoint(mouse_pos):
                self.new_edge = self.check_new_edge(index)

    def check_new_edge(self, end: int) -> np.ndarray:
        if end in self.new_edge:
            return self.new_edge
        if self.new_edge[0] < 0:
            return np.array((end, self.new_edge[1]))
        elif self.new_edge[0] >= 0:
            return np.array((self.new_edge[0], end))


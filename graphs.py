import numpy as np

class Graph:
    def __init__(self, adjacency_matrix: np.ndarray):
        self.adjacency_matrix = adjacency_matrix
        self.vertices_number = adjacency_matrix.shape[0]
        self.edges_number = np.count_nonzero(adjacency_matrix)

    def add_vertex(self):
        new_line = np.array([0] * self.vertices_number)
        new_column = np.array([[0]] * (self.vertices_number + 1))

        self.adjacency_matrix = np.vstack((self.adjacency_matrix, new_line))
        self.adjacency_matrix = np.hstack((self.adjacency_matrix, new_column))

        self.vertices_number += 1

    def remove_vertex(self, vertex: int): 
        self.adjacency_matrix = np.delete(self.adjacency_matrix, vertex, axis=0)
        self.adjacency_matrix = np.delete(self.adjacency_matrix, vertex, axis=1)

    def add_edge(self, start_vertex: int, end_vertex: int):
        self.adjacency_matrix[start_vertex,end_vertex] = 1
        self.adjacency_matrix[end_vertex,start_vertex] = 1

    def remove_edge(self, start_vertex: int, end_vertex: int):
        self.adjacency_matrix[start_vertex,end_vertex] = 0
        self.adjacency_matrix[end_vertex,start_vertex] = 0

    def __str__(self):
        return self.adjacency_matrix.__str__()
    

if __name__ == "__main__":
    matrix = np.array([[0,1],[1,0]])
    graph = Graph(matrix)
    print("Matrix representation:")
    print(graph, "\n")
    print("Number of vertices:", graph.vertices_number)
    print("Number of edges:", graph.edges_number)
    
    graph.add_vertex()
    print("Matrix representation:")
    print(graph, "\n")
    print("Number of vertices:", graph.vertices_number)
    print("Number of edges:", graph.edges_number)

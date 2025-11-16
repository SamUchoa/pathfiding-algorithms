import heapq
import math

def a_star_step(adj_matrix, start, goal, heuristic, graph_draw_handler,
                explored_color=[1, 0, 0]):
    n = len(adj_matrix)

    g_cost = [math.inf] * n
    g_cost[start] = 0

    f_cost = [math.inf] * n
    f_cost[start] = heuristic(start)

    open_set = [(f_cost[start], start)]
    came_from = [-1] * n

    while open_set:
        _, current = heapq.heappop(open_set)

        # --- PAUSA AQUI PARA O PYGAME DESENHAR ---
        yield ("current", current)

        if current == goal:
            # reconstruir caminho final
            path = [goal]
            while came_from[path[-1]] != -1:
                path.append(came_from[path[-1]])
            yield ("done", path[::-1], g_cost[goal])
            return

        for neighbor in range(n):
            weight = adj_matrix[current][neighbor]
            if not weight:
                continue

            # pintar aresta explorada
            graph_draw_handler.set_edge_color_by_vertices(
                current, neighbor, explored_color
            )

            # --- PAUSA DEPOIS DE COLORIR A ARESTA ---
            yield ("edge", current, neighbor)

            tentative_g = g_cost[current] + weight

            if tentative_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g
                f_cost[neighbor] = tentative_g + heuristic(neighbor)
                heapq.heappush(open_set, (f_cost[neighbor], neighbor))


from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.
    """

    dist = {}
    prev = {}
    queue = []

    dist[initial_position] = 0
    prev[initial_position] = None
    heappush(queue,(dist[initial_position],initial_position))

    while queue is not None:
        _, u = heappop(queue)

        if u == destination:
            break

        maze = adj(graph,u)
        for v in maze:
            alt = dist[u] + get_distance(u,v)
            if alt < dist.get(v,alt+1):
                dist[v] = alt
                prev[v] = u
                heappush(queue,(alt,v))

    if u == destination:
        path = []
        while u:
            path.append(u)
            u = prev[u]
        path.reverse()
        return path
    else:
        return None

    pass


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """

    pass


def get_distance(initial_position, destination):
    x1 = initial_position[0]
    y1 = initial_position[1]
    x2 = destination[0]
    y2 = destination[1]
    distance = sqrt((x1-x2)**2+(y1-y2)**2)

    return distance
    pass

# def get_path(path, destination, previous):
#     if path == destination:
#         route = []
#         while path:
#             route.append(path)
#             path = previous[path]
#         route.reverse()
#         return route
#     else:
#         return None
#     pass

def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    adj_list = []
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]
    diagdirs = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
    for dir in dirs:
        neighbors = (dir[0] + cell[0], dir[1] + cell[1])
        reach = sqrt(dir[0] * dir[0] + dir[1] * dir[1])
        if reach > 0  and neighbors in level['spaces']:
            adj_list.append(neighbors)
            if dir in diagdirs:
                cost = sqrt(2) * (0.5 * level['spaces'].get(cell)) + (0.5 * level['spaces'].get(neighbors))
            else:
                cost = (0.5 * level['spaces'].get(cell) + (0.5 * level['spaces'].get(neighbors)))
            #adj_list.append(cost)

    return adj_list
    pass

# def del_none(dict, key):
#     for none in dict:
#         if dict.get(key) is None:
#             del dict[key]
#
#     pass

def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'my_maze.txt', 'a','e'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')

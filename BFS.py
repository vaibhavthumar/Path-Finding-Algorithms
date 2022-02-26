from queue import Queue

def BFSAlgorithm(draw, construct_path, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = set()

    while not queue.empty():
        current = queue.get()
        if current not in visited:
            if current == end:
                construct_path(came_from, end, draw)
                end.make_end()
                return True
            else:
                visited.add(current)
                for neighbor in current.neighbors:
                    if neighbor not in visited:
                        queue.put(neighbor)
                        came_from[neighbor] = current
                        neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
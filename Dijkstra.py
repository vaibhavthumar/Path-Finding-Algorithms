from queue import PriorityQueue

def DijkstraAlgorithm(draw, construct_path, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # (Distance, Time, Node)
    came_from = {}
    cost = {spot: float("inf") for row in grid for spot in row}
    cost[start] = 0
    
    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            construct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_cost = cost[current] + 1

            if temp_cost < cost[neighbor]:
                came_from[neighbor] = current
                cost[neighbor] = temp_cost
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((cost[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
import pygame
from Spot import Spot
from AStar import AStarAlgorithm
from DFS import DFSAlgorithm
from BFS import BFSAlgorithm
from Dijkstra import DijkstraAlgorithm
from button import Button

HEIGHT = 700
WIDTH = 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding Algorithm")

RED = pygame.Color('red')
GREEN = pygame.Color('green')
BLUE = pygame.Color('blue')
YELLOW = pygame.Color('yellow')
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
PURPLE = pygame.Color('purple')
ORANGE = pygame.Color('orange')
GREY = pygame.Color('grey')
TURQUOISE = pygame.Color('turquoise')
SLATEGRAY1 = pygame.Color('slategray1')

astar_img = pygame.image.load('Images/Astar.jpg').convert_alpha()
dfs_img = pygame.image.load('Images/DFS.jpg').convert_alpha()
bfs_img = pygame.image.load('Images/BFS.jpg').convert_alpha()
dijkstra_img = pygame.image.load('Images/Dijkstra.jpg').convert_alpha()

def construct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()
        draw()

def make_grid(rows, HEIGHT):
    grid = []
    gap = HEIGHT // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, HEIGHT):
    gap = HEIGHT // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (HEIGHT, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, HEIGHT))

def draw(win, grid, rows, HEIGHT, buttons):
    win.fill(SLATEGRAY1)

    for button in buttons:
        button.draw(win)
        
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, HEIGHT)
    pygame.display.update()

def get_click_pos(pos, rows, HEIGHT):
    gap = HEIGHT // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

def visualizer(win, HEIGHT):
    ROWS = 50
    grid = make_grid(ROWS, HEIGHT)
    buttons = []

    start = None
    end = None
    algorithm = None

    run = True
    started = False

    astar_button = Button(750, 100, image=astar_img)
    dfs_button = Button(750, 150, image=dfs_img)
    bfs_button = Button(750, 200, image=bfs_img)
    dijkstra_button = Button(750, 250, image=dijkstra_img)
    # astar_button = Button(750, 100, width=100, height=30, color=CADETBLUE)
    buttons.append(astar_button)
    buttons.append(dfs_button)
    buttons.append(bfs_button)
    buttons.append(dijkstra_button)

    while run:
        draw(win, grid, ROWS, HEIGHT, buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
  
            if started:
                continue

            if pygame.mouse.get_pressed()[0]: # Left
                pos = pygame.mouse.get_pos()

                if astar_button.is_clicked(pos):
                    algorithm = AStarAlgorithm
                elif dfs_button.is_clicked(pos):
                    algorithm = DFSAlgorithm
                elif bfs_button.is_clicked(pos):
                    algorithm = BFSAlgorithm
                elif dijkstra_button.is_clicked(pos):
                    algorithm = DijkstraAlgorithm
                else:
                    row, col = get_click_pos(pos, ROWS, HEIGHT)
                    if row != 0 and col != 0 and row != ROWS - 1 and col != ROWS - 1 and row < ROWS and col < ROWS:
                        spot = grid[row][col]
                        if not start:
                            start = spot
                            start.make_start()

                        if not end and spot != start:
                            end = spot
                            end.make_end()

                        elif spot != start and spot != end:
                            spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # Right
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, ROWS, HEIGHT)
                if row != 0 and col != 0 and row != ROWS - 1 and col != ROWS - 1 and row < ROWS and col < ROWS:
                    spot = grid[row][col]
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None
                    spot.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and not started and algorithm:
                    started = True
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, HEIGHT, buttons), construct_path, grid, start, end)
                    started = False
                
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    algorithm = None
                    grid = make_grid(ROWS, HEIGHT)

        pygame.display.update()
            
    pygame.quit()

if __name__ == '__main__':
    visualizer(WIN, HEIGHT)
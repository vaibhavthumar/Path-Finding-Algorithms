import pygame
from Spot import Spot
from AStar import AStarAlgorithm

HEIGHT = 700
WIDTH = 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

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

def draw(win, grid, rows, HEIGHT):
    win.fill(WHITE)

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

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, HEIGHT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
  
            if started:
                continue

            if pygame.mouse.get_pressed()[0]: # Left
                pos = pygame.mouse.get_pos()
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
                if event.key == pygame.K_SPACE and start and end and not started:
                    started = True
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    AStarAlgorithm(lambda: draw(win, grid, ROWS, HEIGHT), construct_path, grid, start, end)
                    started = False
                
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, HEIGHT)

    pygame.quit()

if __name__ == '__main__':
    visualizer(WIN, HEIGHT)
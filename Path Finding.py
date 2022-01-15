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
pygame.display.set_caption("Path Finding Algorithm Visualiser")

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

def draw(win, grid, rows, HEIGHT, buttons, input_rect, user_text, base_font):
    win.fill(SLATEGRAY1)

    for button in buttons:
        button.draw(win)
        
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, HEIGHT)
    
    pygame.draw.rect(win, WHITE, input_rect)
    text_surface = base_font.render(user_text, True, BLACK)
    win.blit(text_surface, (input_rect.x + 5, input_rect.y + 10))

    pygame.display.update()

def get_click_pos(pos, rows, HEIGHT):
    gap = HEIGHT // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

def button_selector(clicked_button, buttons):
    for button in buttons:
        if button == clicked_button:
            button.is_selected(True)
        else:
            button.is_selected(False)

def visualizer(win, HEIGHT):
    ROWS = 50
    grid = make_grid(ROWS, HEIGHT)
    buttons = []

    start = None
    end = None
    algorithm = None

    run = True
    started = False

    astar_button = Button(725, 100, image=astar_img)
    buttons.append(astar_button)
    dfs_button = Button(725, 150, image=dfs_img)
    buttons.append(dfs_button)
    bfs_button = Button(725, 200, image=bfs_img)
    buttons.append(bfs_button)
    dijkstra_button = Button(725, 250, image=dijkstra_img)
    buttons.append(dijkstra_button)
    generate_button = Button(790, 50, 75, color=GREY)
    buttons.append(generate_button)

    pygame.init()
    base_font = pygame.font.Font(None, 30)
    user_text = str(ROWS)
    text_active = False
    input_rect = pygame.Rect(725, 50, 50, 30)
    numbers = [pygame.K_0,
               pygame.K_1,
               pygame.K_2,
               pygame.K_3,
               pygame.K_4,
               pygame.K_5,
               pygame.K_6,
               pygame.K_7,
               pygame.K_8,
               pygame.K_9]

    while run:
        draw(win, grid, ROWS, HEIGHT, buttons, input_rect, user_text, base_font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
  
            if started:
                continue

            if pygame.mouse.get_pressed()[0]: # Left
                pos = pygame.mouse.get_pos()
                text_active = False

                if astar_button.is_clicked(pos):
                    algorithm = AStarAlgorithm
                    button_selector(astar_button, buttons)
                elif dfs_button.is_clicked(pos):
                    algorithm = DFSAlgorithm
                    button_selector(dfs_button, buttons)
                elif bfs_button.is_clicked(pos):
                    algorithm = BFSAlgorithm
                    button_selector(bfs_button, buttons)
                elif dijkstra_button.is_clicked(pos):
                    algorithm = DijkstraAlgorithm
                    button_selector(dijkstra_button, buttons)
                elif generate_button.is_clicked(pos) and int(user_text) > 9:
                    ROWS = int(user_text)
                elif input_rect.collidepoint(pos):
                    text_active = True
                else:
                    text_active = False
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
                text_active = False
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

                    algorithm(lambda: draw(win, grid, ROWS, HEIGHT, buttons, input_rect, user_text, base_font), construct_path, grid, start, end)
                    started = False
                
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, HEIGHT)

                if text_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key in numbers:
                        if int(user_text) == 0:
                            user_text = event.unicode
                        else:
                            user_text += event.unicode
                        if int(user_text) > 50:
                            text_active = False
                
                if user_text == '':
                    user_text = str(0)
            
            if not text_active:
                if int(user_text) < 10:
                    user_text = str(10)
                if int(user_text) > 50:
                    user_text = str(50)

        pygame.display.update()
            
    pygame.quit()

if __name__ == '__main__':
    visualizer(WIN, HEIGHT)
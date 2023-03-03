import pygame
import random
import heapq
import time
from PIL import Image

WIDTH = 1800
HEIGHT = 950
OBSTACLE_PROBABILITY = 0.3
BLOCK_SIZE = 20
# GRID_X = 41
NUM_OBSTACLES = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)


LEVEL_1 = r".\normal.png"
LEVEL_2 = r".\braid200.png"

LEVEL = None

if LEVEL == LEVEL_1:
    GRID_X = 41
    GRID_Y = 41
elif LEVEL == LEVEL_2:
    GRID_X = 201
    GRID_Y = 201
else: 
    GRID_X = 41
    GRID_Y = 41


class Node:
    def __init__(self, x, y, cost, parent):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def convert_to_map(image):
    # converts the image into a map array of 0's and 1's
    # image size is 41x41
    # takes the average of the RGB values and if it is less than 128, it is an obstacle
    map = []
    for y in range(GRID_Y):
        map.append([])
        for x in range(GRID_X):
            if rgb_of_pixel(image, x, y) < 128:
                map[y].append(1)
            else:
                map[y].append(0)
    print('finished converting image to map')
    return map
        
def rgb_of_pixel(image, x, y):
    # returns the RGB value of a pixel
    im = Image.open(image).convert('RGB')
    r, g, b = im.getpixel((x, y))
    a = (r + g + b)
    return a

def generate_map():
    map = []
    for i in range(GRID_Y):
        map.append([])
        for j in range(GRID_X):
            if random.random() < OBSTACLE_PROBABILITY:
                map[i].append(1)
            else:
                map[i].append(0)
    return map

def neighbors(node, map):
    x, y = node
    results = []
    if x > 0 and map[x - 1][y] != 1:
        results.append((x - 1, y))
    if x < GRID_X - 1 and map[x + 1][y] != 1:
        results.append((x + 1, y))
    if y > 0 and map[x][y - 1] != 1:
        results.append((x, y - 1))
    if y < GRID_X - 1 and map[x][y + 1] != 1:
        results.append((x, y + 1))

    # diagonal up right if there is no obstacle up and right
    if x < GRID_X - 1 and y > 0 and map[x + 1][y - 1] != 1 and map[x + 1][y] != 1 and map[x][y - 1] != 1:
        results.append((x + 1, y - 1))
    # diagonal up left if there is no obstacle up and left
    if x > 0 and y > 0 and map[x - 1][y - 1] != 1 and map[x - 1][y] != 1 and map[x][y - 1] != 1:
        results.append((x - 1, y - 1))
    # diagonal down right if there is no obstacle down and right
    if x < GRID_X - 1 and y < GRID_Y - 1 and map[x + 1][y + 1] != 1 and map[x + 1][y] != 1 and map[x][y + 1] != 1:
        results.append((x + 1, y + 1))
    # diagonal down left if there is no obstacle down and left
    if x > 0 and y < GRID_Y - 1 and map[x - 1][y + 1] != 1 and map[x - 1][y] != 1 and map[x][y + 1] != 1:
        results.append((x - 1, y + 1))
    

    return results

def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(start, goal, map):
    heap = []
    heapq.heappush(heap, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    startTime = time.time()
    while heap:
        current = heapq.heappop(heap)[1]

        if current == goal:
            break

        for next_node in neighbors(current, map):
            new_cost = cost_so_far[current] + 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                heapq.heappush(heap, (priority, next_node))
                came_from[next_node] = current
    elapsed_time = time.time() - startTime
    # round to 2 decimal places
    elapsed_time = round(elapsed_time * 1000, 2)
    elapsed_time = str(elapsed_time)
    print("Time taken: ", elapsed_time, "ms")
    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        if current in came_from:
            current = came_from[current]
            path.append(current)
        else:
            print("Path not found")
            return []
    path.reverse()
    return path

def base_grid(screen, map):
    for x in range(GRID_Y):
            for y in range(GRID_X):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if map[x][y] == 1:
                    pygame.draw.rect(screen, BLACK, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                    
                pygame.draw.rect(screen, BLACK, rect, 1)

def draw_grid(screen, map, start, goal, came_from, path):
    base_grid(screen, map)
            
    rect = pygame.Rect(start[0] * BLOCK_SIZE, start[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, BLUE, rect)
    rect = pygame.Rect(goal[0] * BLOCK_SIZE, goal[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, RED, rect)

    # get time until goal is reached
    
    start_time = time.time()
    for node in came_from:
        x, y = node
        if came_from[node] is not None:
            x2, y2 = came_from[node]
            
            if (x2, y2) in came_from and (x, y) in came_from:
                pygame.draw.line(screen, RED, (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2),
                                 (x2 * BLOCK_SIZE + BLOCK_SIZE // 2, y2 * BLOCK_SIZE + BLOCK_SIZE // 2), 2)
               
        pygame.display.update()
        # pygame.time.wait(5)

    elapsed_time = time.time() - start_time
    # round to 2 decimal places
    elapsed_time = round(elapsed_time * 1000, 2)
    elapsed_time = str(elapsed_time)
    # display the time it took to reach the goal
    font = pygame.font.SysFont("Arial", 20)
    text = font.render('Search took ' + elapsed_time + 'ms', True, WHITE)
    screen.blit(text, (1010,10))
    pygame.display.update()
    
    for i in range(len(path) - 1):
        node = path[i]
        next_node = path[i + 1]
        x1, y1 = node
        x2, y2 = next_node
        pygame.draw.line(screen, GREEN, (x1 * BLOCK_SIZE + BLOCK_SIZE // 2, y1 * BLOCK_SIZE + BLOCK_SIZE // 2),
                         (x2 * BLOCK_SIZE + BLOCK_SIZE // 2, y2 * BLOCK_SIZE + BLOCK_SIZE // 2), 5)
        pygame.display.update()
        # pygame.time.delay(10)
        
        
        
    for i in range(len(path) - 1):
        node = path[i]
        next_node = path[i + 1]
        x1, y1 = node
        x2, y2 = next_node
        # swap blue block with white block and black outline
        rect = pygame.Rect(x1 * BLOCK_SIZE, y1 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        rect = pygame.Rect(x1 * BLOCK_SIZE, y1 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        # duration = .1 # seconds
        start_pos = (x1 * BLOCK_SIZE, y1 * BLOCK_SIZE)
        end_pos = (x2 * BLOCK_SIZE, y2 * BLOCK_SIZE)
        for new_rect in interpolate_rect(rect, start_pos, end_pos, 0):
            pygame.draw.rect(screen, BLUE, new_rect)
            pygame.display.update()
            # pygame.time.delay(8)
            
        # after the update, let's call the draw_grid function to restore the grid 
        # and draw the goal node in red again while setting the start node empty
            if not i == len(path) - 1:
                base_grid(screen, map)
        # draw_grid(screen, map, , goal, came_from, path)
        pygame.display.update()

        # pygame.display.update()
        pygame.time.delay(1)

    # when finished, draw the goal node in blue
    x, y = goal
    rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, BLUE, rect)
    pygame.display.update()    

    # call mouse click function and restart draw_grid function
    start = goal
    goal = get_mouse_click(screen, map, "Choose a new goal node")
    came_from, cost_so_far = a_star(start, goal, map)
    path = reconstruct_path(came_from, start, goal)
    draw_grid(screen, map, start, goal, came_from, path)


def interpolate_rect(rect, start_pos, end_pos, duration):
    start_time = time.time()
    current_time = time.time()
    while current_time - start_time < duration:
        elapsed_time = current_time - start_time
        progress = elapsed_time / duration
        rect.x = int(start_pos[0] + (end_pos[0] - start_pos[0]) * progress)
        rect.y = int(start_pos[1] + (end_pos[1] - start_pos[1]) * progress)
        current_time = time.time()
        yield rect

def get_mouse_click(screen, map, message):
    pygame.draw.rect(screen, BLACK, (1010, 10, 200, 30))
    # display message to user
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(message, True, WHITE)
    screen.blit(text, (1010,10))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0] // BLOCK_SIZE
                y = pos[1] // BLOCK_SIZE
                if map[x][y] != 1:
                    # delete message
                    pygame.draw.rect(screen, BLACK, (1010, 10, 200, 30))

                    return x, y

    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Generate a random map with obstacles
    # map = generate_map()
    if LEVEL == 1 or LEVEL == 2:
        map = convert_to_map(LEVEL)
    else:
        map = generate_map()
    # display temporary grid to allow user to choose nodes
    draw_grid(screen, map, (0, 0), (0, 0), {}, [])
    pygame.display.update()

    # Set start and goal nodes by getting a mouse click
    start = get_mouse_click(screen, map, "Choose start node")
    draw_grid(screen, map, (0, 0), (0, 0), {}, [])
    pygame.display.update()
    goal = get_mouse_click(screen, map, "Choose goal node")
    # start = (0, 0)
    # goal = (GRID_X - 1, GRID_X - 1)
    

    came_from, cost_so_far = a_star(start, goal, map)
    path = reconstruct_path(came_from, start, goal)
    print("Path: ", path)

    draw_grid(screen, map, start, goal, came_from, path)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

if __name__ == "__main__":
    main()
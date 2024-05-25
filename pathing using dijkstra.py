import pygame
import sys
from tkinter import messagebox, Tk

window_width = 800
window_height = 800

window = pygame.display.set_mode((window_width, window_height))

columns = 25
rows = 25

box_width = window_width // columns
box_height = window_height // rows

grid = []


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
        self.weight = 1 
        self.color = (255, 255, 255) 

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

    def increase_weight(self):
        if (self.weight < 41):
            self.weight += 5 

    def decrease_weight(self):
        if self.weight > 1:
            self.weight -= 5 

# Create Grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue = [(start_box, 0)]

max_weight = 1

# Dijkstra Algorithm
def dijkstra(start_box, target_box):
    global max_weight
    start_box.visited = True
    queue = [(start_box, 0)]  # Priority queue of tuples (box, accumulated weight)
    while queue:
        current_tuple = queue.pop(0)  # Pop the tuple (box, accumulated weight)
        current_box, accumulated_weight = current_tuple
        if current_box == target_box:
            # Path found, return it
            return current_box
        for neighbour in current_box.neighbours:
            weight = neighbour.weight
            if not neighbour.queued and not neighbour.wall:
                neighbour.queued = True
                neighbour.prior = current_box
                queue.append((neighbour, accumulated_weight + weight))  # Update accumulated weight
                max_weight = max(max_weight, neighbour.weight)  # Update max_weight
        queue.sort(key=lambda x: x[1])  # Sort the queue by accumulated weight
        current_box.visited = True
    return None  # No path found


def main():
    global path, max_weight
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                i, j = x // box_width, y // box_height
                clicked_box = grid[i][j]
                if event.buttons[0]: 
                    clicked_box.increase_weight()
                elif event.buttons[2]: 
                    clicked_box.decrease_weight()
            # Set Wall
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                x, y = pygame.mouse.get_pos()
                i, j = x // box_width, y // box_height
                grid[i][j].wall = True
                # Set Target Box
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_t and not target_box_set:
                x, y = pygame.mouse.get_pos()
                i, j = x // box_width, y // box_height
                target_box = grid[i][j]
                target_box.target = True
                target_box_set = True
            # Start Algorithm
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and target_box_set:
                begin_search = True

        if begin_search:
            if searching:
                start_box.visited = True
                end_box = dijkstra(start_box, target_box) 
                if end_box:
                    searching = False
                    path = []
                    while end_box != start_box:
                        path.append(end_box)
                        end_box = end_box.prior
                    path.append(start_box)
                    path.reverse()  # Reverse the path to draw from start to target
                else:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False
        window.fill((10, 10, 10))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                if box.start:
                    color = (0, 200, 200)  # Start box color
                elif box.target:
                    color = (200, 50, 50)  # Target box color
                elif box.wall:
                    color = (210, 10, 210)  # Wall color
                elif box in path:
                    color = (80, 80, 200)  # Path color
                elif box.queued and not box.visited:
                    color = (200, 200, 50)  # Queued box color
                elif box.visited:
                    color = (80, 180, 80)  # Visited box color 
                else:
                    intensity = int((box.weight / max_weight) * 25)/5
                    color = (intensity+40, intensity+40, intensity+40)
                box.color = color
                box.draw(window)

        pygame.display.flip()


path = []
main()
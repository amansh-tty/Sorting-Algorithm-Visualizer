import pygame, random, sys

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Sorting Algorithm Visualization')
FONT = pygame.font.SysFont('Arial', 24)

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREY = (170, 170, 170)
LIGHT_BLUE = (64, 224, 208)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

RECT_WIDTH = 20
clock = pygame.time.Clock()
FPS = 10
selected_sort = None

sorting_algorithms = {
    'Selection Sort': 'selection_sort',
    'Bubble Sort': 'bubble_sort',
    'Merge Sort': 'merge_sort',
    'Quick Sort': 'quick_sort',
    'Insertion Sort': 'insertion_sort'
}

class Rectangle:
    def __init__(self, color, x, height):
        self.color = color
        self.x = x
        self.width = RECT_WIDTH
        self.height = height

    def set_color(self, color):
        self.color = color

class Button:
    def __init__(self, text, x, y, width, height, color, font_size=24):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.font = pygame.font.SysFont('Arial', font_size)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, BLACK, self.rect, 2)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def create_rectangles():
    num_rectangles = WINDOW_WIDTH // RECT_WIDTH - 5
    rectangles = []
    heights = []

    for i in range(5, num_rectangles):
        height = random.randint(20, 500)
        while height in heights:
            height = random.randint(20, 500)
        heights.append(height)
        rect = Rectangle(PURPLE, i * RECT_WIDTH, height)
        rectangles.append(rect)
    return rectangles

def draw_rectangles(rectangles):
    WINDOW.fill(GREY)
    for rect in rectangles:
        pygame.draw.rect(WINDOW, rect.color, (rect.x, WINDOW_HEIGHT - rect.height, rect.width, rect.height))
        pygame.draw.line(WINDOW, BLACK, (rect.x, WINDOW_HEIGHT), (rect.x, WINDOW_HEIGHT - rect.height))
    pygame.display.update()

def selection_sort(rectangles):
    num_rectangles = len(rectangles)
    for i in range(num_rectangles):
        min_index = i
        rectangles[min_index].set_color(LIGHT_BLUE)

        for j in range(i + 1, num_rectangles):
            rectangles[j].set_color(BLUE)
            draw_rectangles(rectangles)
            if rectangles[j].height < rectangles[min_index].height:
                rectangles[min_index].set_color(PURPLE)
                min_index = j
                rectangles[min_index].set_color(LIGHT_BLUE)
            draw_rectangles(rectangles)
            rectangles[j].set_color(PURPLE)

            yield
        rectangles[i].x, rectangles[min_index].x = rectangles[min_index].x, rectangles[i].x
        rectangles[i], rectangles[min_index] = rectangles[min_index], rectangles[i]
        rectangles[i].set_color(GREEN)
        draw_rectangles(rectangles)

def bubble_sort(rectangles):
    num_rectangles = len(rectangles)
    for i in range(num_rectangles):
        for j in range(num_rectangles - i - 1):
            rectangles[j].set_color(BLUE)
            rectangles[j + 1].set_color(BLUE)
            draw_rectangles(rectangles)

            if rectangles[j].height > rectangles[j + 1].height:
                rectangles[j].x, rectangles[j + 1].x = rectangles[j + 1].x, rectangles[j].x
                rectangles[j], rectangles[j + 1] = rectangles[j + 1], rectangles[j]
            draw_rectangles(rectangles)

            rectangles[j].set_color(PURPLE)
            rectangles[j + 1].set_color(PURPLE)

            yield
        rectangles[num_rectangles - i - 1].set_color(GREEN)
    draw_rectangles(rectangles)

def merge_sort(rectangles, start, end):
    if end - start > 1:
        mid = (start + end) // 2
        yield from merge_sort(rectangles, start, mid)
        yield from merge_sort(rectangles, mid, end)
        left = rectangles[start:mid]
        right = rectangles[mid:end]
        i = j = 0
        for k in range(start, end):
            draw_rectangles(rectangles)
            if i < len(left) and (j >= len(right) or left[i].height < right[j].height):
                rectangles[k] = left[i]
                i += 1
            else:
                rectangles[k] = right[j]
                j += 1
            yield

def quick_sort(rectangles, low, high):
    if low < high:
        pivot_index = yield from partition(rectangles, low, high)
        yield from quick_sort(rectangles, low, pivot_index)
        yield from quick_sort(rectangles, pivot_index + 1, high)

def partition(rectangles, low, high):
    pivot = rectangles[low].height
    left = low + 1
    right = high
    done = False
    while not done:
        while left <= right and rectangles[left].height <= pivot:
            left += 1
        while rectangles[right].height >= pivot and right >= left:
            right -= 1
        if right < left:
            done = True
        else:
            rectangles[left].x, rectangles[right].x = rectangles[right].x, rectangles[left].x
            rectangles[left], rectangles[right] = rectangles[right], rectangles[left]
        yield
    rectangles[low].x, rectangles[right].x = rectangles[right].x, rectangles[low].x
    rectangles[low], rectangles[right] = rectangles[right], rectangles[low]
    yield
    return right

def insertion_sort(rectangles):
    for i in range(1, len(rectangles)):
        key = rectangles[i]
        j = i - 1
        while j >= 0 and key.height < rectangles[j].height:
            rectangles[j + 1] = rectangles[j]
            j -= 1
            draw_rectangles(rectangles)
            yield
        rectangles[j + 1] = key
        draw_rectangles(rectangles)
        yield

def display_text(txt, x, y, size=24):
    font = pygame.font.SysFont('Arial', size)
    text = font.render(txt, True, BLACK)
    text_rect = text.get_rect(center=(x, y))
    WINDOW.blit(text, text_rect)

def create_buttons():
    button_width, button_height = 180, 50
    start_button = Button('Start Sorting', WINDOW_WIDTH // 2 - button_width // 2, 600, button_width, button_height, LIGHT_BLUE)
    buttons = [
        Button('Selection Sort', 50, 50, button_width, button_height, WHITE),
        Button('Bubble Sort', 50, 120, button_width, button_height, WHITE),
        Button('Merge Sort', 50, 190, button_width, button_height, WHITE),
        Button('Quick Sort', 50, 260, button_width, button_height, WHITE),
        Button('Insertion Sort', 50, 330, button_width, button_height, WHITE)
    ]
    return start_button, buttons

def main():
    rectangles = create_rectangles()
    sorting = False
    sorting_generator = None
    start_button, buttons = create_buttons()

    run = True
    while run:
        WINDOW.fill(GREY)
        draw_rectangles(rectangles)
        start_button.draw(WINDOW)
        for button in buttons:
            button.draw(WINDOW)
        display_text('Press SPACE to pause/resume sorting.', WINDOW_WIDTH // 2, 700, 24)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and sorting_generator:
                    sorting = not sorting

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, button in enumerate(buttons):
                    if button.is_clicked(pos):
                        sort_function = list(sorting_algorithms.values())[i]
                        if sort_function == 'merge_sort':
                            sorting_generator = merge_sort(rectangles, 0, len(rectangles))
                        elif sort_function == 'quick_sort':
                            sorting_generator = quick_sort(rectangles, 0, len(rectangles) - 1)
                        else:
                            sorting_generator = globals()[sort_function](rectangles)

                        for b in buttons:
                            b.color = WHITE
                        button.color = RED

                if start_button.is_clicked(pos):
                    sorting = True

        if sorting and sorting_generator:
            try:
                next(sorting_generator)
            except StopIteration:
                sorting = False

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

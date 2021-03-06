# 천장 충돌 처리
import math
import os
import random

import pygame


# Bubble Class
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position=(0, 0)):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
        self.radius = 18        # Bubble 발사했을때 나아가는 정도

    def set_rect(self, position):
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_angle(self, angle):
        self.angle = angle
        self.rad_angle = math.radians(angle)

    def move(self):
        to_x = self.radius * math.cos(self.rad_angle)
        to_y = self.radius * math.sin(self.rad_angle) * -1

        self.rect.x += to_x
        self.rect.y += to_y

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.set_angle(180 - self.angle)

class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position, angle):
        super().__init__()
        self.original_image = image
        self.image = image
        self.position = position
        self.rect = image.get_rect(center=position)
        self.angle = angle

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)

    def rotate(self, angle):
        self.angle += angle

        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.position)


# Map
def setup():
    global bubble_map
    bubble_map = [
        list("RRYYBBGG"),
        list("RRYYBBG/"),
        list("BBGGRRYY"),
        list("BGGRRYY/"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
    ]
    # bubble_map = [
    #     list("....R..."),
    #     list("......./"),
    #     list("........"),
    #     list("......./"),
    #     list("........"),
    #     list("......./"),
    #     list("........"),
    #     list("......./"),
    #     list("........"),
    #     list("......./"),
    #     list("........"),
    # ]

    for row_idx, row in enumerate(bubble_map):
        for col_idx, col in enumerate(row):
            if col in [".", "/"]:
                continue

            position = get_bubble_position(row_idx, col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image, col, position))


def get_bubble_position(row_idx, col_idx):
    pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH // 2)
    pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT // 2)

    if row_idx % 2 == 1:
        pos_x += CELL_SIZE // 2

    return pos_x, pos_y


def get_bubble_image(color):
    if color == "R":
        return bubble_images[0]
    elif color == "Y":
        return bubble_images[1]
    elif color == "B":
        return bubble_images[2]
    elif color == "G":
        return bubble_images[3]
    elif color == "P":
        return bubble_images[4]
    else:  # BLACK
        return bubble_images[-1]


def prepare_bubbles():
    global current_bubble, next_bubble

    if next_bubble:
        current_bubble = next_bubble
    else:
        current_bubble = create_bubble()

    current_bubble.set_rect((screen_width // 2, 624))
    next_bubble = create_bubble()
    next_bubble.set_rect((screen_width // 4, 688))


def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    return Bubble(image, color)


def get_random_bubble_color():
    color_list = []
    for row in bubble_map:
        for col in row:
            if col not in color_list and col not in [".", "/"]:
                color_list.append(col)
    return random.choice(color_list)


def process_collision():
    global current_bubble, bubble_group, is_fire

    is_hit_bubble = pygame.sprite.spritecollideany(current_bubble, bubble_group, pygame.sprite.collide_mask)

    if is_hit_bubble or current_bubble.rect.top <= 0:
        row_idx, col_idx = get_map_index(*current_bubble.rect.center)   # Tupple (x,y)
        place_bubble(current_bubble, row_idx, col_idx)
        current_bubble = None
        is_fire = False



def get_map_index(x, y):
    row_idx = y // CELL_SIZE
    col_idx = x // CELL_SIZE

    if row_idx % 2 == 1:
        col_idx = (x - (CELL_SIZE // 2)) // CELL_SIZE

        if col_idx < 0:
            col_idx = 0
        elif col_idx > MAP_COL_COUNT - 2:
            col_idx = MAP_COL_COUNT - 2

    return row_idx, col_idx


def place_bubble(bubble, row_idx, col_idx):
    global bubble_map, bubble_group
    bubble_map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble_group.add(bubble)

#######################################################################

pygame.init()
screen_width = 432
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Puzzle Bobble")

clock = pygame.time.Clock()

# Background Image Load
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "resource/background/background.png"))

# Bubble Images Load
bubble_images = [
    pygame.image.load(os.path.join(current_path, "resource/bubble/red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "resource/bubble/yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "resource/bubble/blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "resource/bubble/green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "resource/bubble/purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "resource/bubble/black.png")).convert_alpha(),
]

# Pointer Image Load
pointer_image = pygame.image.load(os.path.join(current_path, "resource/pointer/pointer.png"))
pointer = Pointer(pointer_image, (screen_width // 2, 624), 90)

#########################
# Game Global Variable
#########################
CELL_SIZE = 54
BUBBLE_WIDTH = 54
BUBBLE_HEIGHT = 62
RED = (255, 0, 0)
MAP_ROW_COUNT = 11
MAP_COL_COUNT = 8

to_angle_left = 0
to_angle_right = 0
angle_speed = 1.5

current_bubble = None
next_bubble = None
is_fire = False

bubble_map = []
bubble_group = pygame.sprite.Group()

# Setup
setup()

running = True

###############
# Game Loop
###############
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_angle_left += angle_speed
            elif event.key == pygame.K_RIGHT:
                to_angle_right -= angle_speed
            elif event.key == pygame.K_SPACE:
                if current_bubble and not is_fire:
                    is_fire = True
                    current_bubble.set_angle(pointer.angle)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0

    if not current_bubble:
        prepare_bubbles()

    if is_fire:
        process_collision()     # 충돌 처리

    screen.blit(background, (0, 0))
    bubble_group.draw(screen)
    pointer.rotate(to_angle_left + to_angle_right)
    pointer.draw(screen)
    if current_bubble:
        if is_fire:
            current_bubble.move()
        current_bubble.draw(screen)

        # if current_bubble.rect.top <= 0:
        #     current_bubble = None
        #     is_fire = False

    if next_bubble:
        next_bubble.draw(screen)

    pygame.display.update()

pygame.quit()

# 화면 흔들기
# pointer에서 발사된 횟수만큼 화면이 흔들림
# 벽내리기 주어진 기회에 따라
# 기회가 2번 남으면 화면이 조금 흔들림
# 기회가 1번 남으면 화면이 많이 흔들림
# 기회가 없으면 벽이 내려옴

import os, random, math
import pygame

class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position=(0, 0), row_idx=-1, col_idx=-1):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
        self.radius = 18
        self.row_idx = row_idx
        self.col_idx = col_idx

    def set_rect(self, position):
        self.rect = self.image.get_rect(center=position)

    # to_x 를 받기 값이 3이상일 수도 있으니 기본 None 으로
    def draw(self, screen, to_x=None):
        if to_x:
            # rect 정보에 맞춰 x, y 함께 가야하기때문에 y 추가
            screen.blit(self.image, (self.rect.x + to_x, self.rect.y))
        else:
            screen.blit(self.image, self.rect)
        # screen.blit(self.image, self.rect)

    def set_angle(self, angle):
        self.angle = angle
        self.rad_angle = math.radians(self.angle)
    def move(self):
        to_x = self.radius * math.cos(self.rad_angle)
        to_y = self.radius * math.sin(self.rad_angle) * -1
        self.rect.x += to_x
        self.rect.y += to_y
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.set_angle(180 - self.angle)

    def set_map_index(self, row_idx, col_idx):
        self.row_idx = row_idx
        self.col_idx = col_idx


class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position, angle):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.angle = angle
        self.original_image = image
        self.position = position

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

def setup():
    global map
    map = [
        list("RRYYBBGG"),
        list("RRYYBBG/"),
        list("BBGGRRYY"),
        list("RGGRRYY/"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
    ]

    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in [".", "/"]:
                continue
            position = get_bubble_position(row_idx, col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image, col, position, row_idx, col_idx))
            
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
    elif color == "B":
        return bubble_images[-1]

def prepare_bubbles():
    global curr_bubble, next_bubble
    if next_bubble:
        curr_bubble = next_bubble
    else:
        curr_bubble = create_bubble()
    curr_bubble.set_rect((screen_width // 2, 624))
    next_bubble = create_bubble()
    next_bubble.set_rect((screen_width // 4, 688))

def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    return Bubble(image, color)

def get_random_bubble_color():
    colors = []
    for row in map:
        for col in row:
            if col not in colors and col not in [".", "/"]:
                colors.append(col)
        return random.choice(colors)

def process_collision():
    #
    global curr_bubble, fire, curr_fire_count
    hit_bubble = pygame.sprite.spritecollideany(curr_bubble, bubble_group, pygame.sprite.collide_mask)
    if hit_bubble or curr_bubble.rect.top <= 0:
        row_idx, col_idx = get_map_index(*curr_bubble.rect.center)
        place_bubble(curr_bubble, row_idx, col_idx)
        remove_adjacent_bubbles(row_idx, col_idx, curr_bubble.color)
        curr_bubble = None
        fire = False
    # 충돌처리 이후 횟수 감소
        curr_fire_count -= 1

def get_map_index(x, y):
    row_idx = y // CELL_SIZE
    col_idx = x // CELL_SIZE
    if row_idx % 2 == 1:
        col_idx = (x- (CELL_SIZE // 2)) // CELL_SIZE
        if col_idx < 0:
            col_idx = 0
        elif col_idx > MAP_COLUMN_COUNT - 2:
            col_idx = MAP_COLUMN_COUNT - 2    
    return row_idx, col_idx
def place_bubble(bubble, row_idx, col_idx):
    map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble.set_map_index(row_idx, col_idx)
    bubble_group.add(bubble)
def remove_adjacent_bubbles(row_idx, col_idx, color):
    visited.clear()
    visit(row_idx, col_idx, color)
    if len(visited) >= 3:
        remove_visited_bubbles()
        remove_hanging_bubbles()

def visit(row_idx, col_idx, color=None):
    if row_idx < 0 or row_idx >= MAP_ROW_COUNT or col_idx < 0 or col_idx >= MAP_COLUMN_COUNT:
        return
    if color and map[row_idx][col_idx] != color:
        return
    if map[row_idx][col_idx] in [".", "/"]: 
        return
    if (row_idx, col_idx) in visited:
        return
    visited.append((row_idx, col_idx))

    rows = [0, -1, -1, 0, 1, 1]
    cols = [-1, -1, 0 , 1, 0, -1]
    if row_idx % 2 == 1:
        rows = [0, -1, -1, 0, 1, 1]
        cols = [-1, 0, 1 , 1, 1, 0]

    for i in range(len(rows)):
        visit(row_idx + rows[i], col_idx + cols[i], color)

def remove_visited_bubbles():
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)
def remove_not_visited_bubbles():
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) not in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)

def remove_hanging_bubbles():
    visited.clear()
    for col_idx in range(MAP_COLUMN_COUNT):
        if map[0][col_idx] != ".":
            visit(0, col_idx)
    remove_not_visited_bubbles()

# 모든 버블 그리기
def draw_bubbles():
    global curr_fire_count
    to_x = None
    if curr_fire_count == 2:
        # -1 ~ 1 사이의 값이 나옴, (-1, 1)도 가능
        to_x = random.randint(0, 2) -1 
    elif curr_fire_count == 1:
        # (-4, 4) 도 가능
        to_x = random.randint(0, 8) -4
    
    for bubble in bubble_group:
        # 그려줄때 to_x 값에 따라서 rect 정보를 더해주는 처리할 것
        bubble.draw(screen, to_x)

pygame.init()
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Puzzle Bobble")
clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

bubble_images = [
    pygame.image.load(os.path.join(current_path, "red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "black.png")).convert_alpha()
]

pointer_image = pygame.image.load(os.path.join(current_path, "pointer.png"))
pointer = Pointer(pointer_image, (screen_width // 2, 624), 90) # 최초 90도 각도로 

CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62
RED = (255, 0, 0)

MAP_ROW_COUNT = 11
MAP_COLUMN_COUNT = 8

# 사용 가능한 횟수
# 버블을 쏘고 버블의 충돌 이후 충돌처리하고 횟수 감소
FIRE_COUNT = 7

to_angle_left = 0
to_angle_right = 0
angle_speed = 1.5

curr_bubble = None
next_bubble = None

fire = False
# 게임 시작시 기회
curr_fire_count = FIRE_COUNT

map = []
visited = []
bubble_group = pygame.sprite.Group()
setup()

running = True
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
                if curr_bubble and not fire:
                    fire = True
                    curr_bubble.set_angle(pointer.angle)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0

        
    if not curr_bubble:
        prepare_bubbles()
    if fire:
        process_collision()

    screen.blit(background, (0, 0))
    # bubble_group 을 curr_fire_count로 확인해서 x좌표를 흔들기
    # bubble_group.draw(screen)
    draw_bubbles()
    pointer.rotate(to_angle_left + to_angle_right)
    pointer.draw(screen)
    if curr_bubble:
        if fire:
            curr_bubble.move()
        curr_bubble.draw(screen)
    if next_bubble:
        next_bubble.draw(screen)    

    pygame.display.update()

pygame.quit()
# fire bubble
# 발사용 버블 추가, pointer 각도에 따른 버블 발사 조정
# 양옆에 부딪히면 튕겨나가는작업까지

import os, random
import pygame

class Bubble(pygame.sprite.Sprite):
    # 생성되는 버블 내 Bubble 클래스 객체 pos 을 위해 값부여
    def __init__(self, image, color, position=(0, 0)):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
    # 발사용 버블 set_rect
    def set_rect(self, position):
        self.rect = self.image.get_rect(center=position)
    # 발사용버블 draw
    def draw(self, screen):
        screen.blit(self.image, self.rect)

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
    elif color == "B":
        return bubble_images[-1]

# 발사대 준비용 버블들
def prepare_bubbles():
    global curr_bubble
    # class 이미지, 컬러 등등 
    # curr_bubble = Bubble(...)
    curr_bubble = create_bubble()
    # 좌표 정의
    curr_bubble.set_rect((screen_width // 2, 624))

def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    # 클래스 객체, pos 따로 
    return Bubble(image, color)

# 랜덤하게 버블 색 import random
# 램덤이더라도 클리어를 위한 남은 버블색안에서 램덤
def get_random_bubble_color():
    # 빈 리스트
    colors = []
    # 맵 순회하면서 정의된 글자
    for row in map:
        for col in row:
            if col not in colors and col not in [".", "/"]:
                colors.append(col)
        return random.choice(colors)

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
to_angle_left = 0
to_angle_right = 0
angle_speed = 1.5

# 발사대 버블
curr_bubble = None

map = []
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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0

        

    # 발사대 버블 그리기 버블이 없다면 그려주기
    if not curr_bubble:
        # 함수
        prepare_bubbles()

    screen.blit(background, (0, 0))
    bubble_group.draw(screen)
    pointer.rotate(to_angle_left + to_angle_right)
    pointer.draw(screen)
    # 버블 그리기
    if curr_bubble:
        curr_bubble.draw(screen)

    pygame.display.update()

pygame.quit()
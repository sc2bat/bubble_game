# user 의 input 에 따라 화살표 이동


import os
import pygame

class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)

class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position, angle):
        super().__init__()
        # 각도가 바뀔때마다 새로운 이미지
        self.image = image
        self.rect = image.get_rect(center=position)
        # 
        self.angle = angle
        # 항상 0도를 바라보는 이미지
        self.original_image = image
        # position 멤버변수
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # 확인
        pygame.draw.circle(screen, RED, self.position, 3)

    # 회전
    def rotate(self, angle):
        self.angle += angle

    # 화살표 회전 제한
        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10
    # 기본 이미지, 변한 이미지, 크기
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
# 좌우로 움직일 각도
# to_angle = 0
# 방향키 좌우 동시에 입력이 충돌현상 해결
to_angle_left = 0
to_angle_right = 0
# 1.5씩 움직임
angle_speed = 1.5

map = []
bubble_group = pygame.sprite.Group()
setup()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 키보드 이벤트 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
            # 키 충돌 방지
                # to_angle += angle_speed
                to_angle_left += angle_speed
            elif event.key == pygame.K_RIGHT:
                # to_angle -= angle_speed
                to_angle_right -= angle_speed
        if event.type == pygame.KEYUP:
            # if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0

    screen.blit(background, (0, 0))
    bubble_group.draw(screen)
    # 회전하는 메소드 # 키충돌 방지
    pointer.rotate(to_angle_left + to_angle_right)
    pointer.draw(screen)
    pygame.display.update()

pygame.quit()
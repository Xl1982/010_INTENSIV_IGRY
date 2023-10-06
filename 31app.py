import pygame
import random

pygame.init()
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
font = pygame.font.Font(None, 36)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect Items Game")
target_count = 10


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def decrease_life(self):
        self.lives -= 1


class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 20)
        self.rect.y = random.randint(0, HEIGHT - 20)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(0, HEIGHT - 30)


all_sprites = pygame.sprite.Group()
items = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


for _ in range(target_count):
    item = Item()
    all_sprites.add(item)
    items.add(item)

for _ in range(5):
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    collected_items = pygame.spritecollide(player, items, True)
    if len(collected_items) > 0:
        target_count -= len(collected_items)

    collided_obstacles = pygame.spritecollide(player, obstacles, True)
    if len(collided_obstacles) > 0:
        player.decrease_life()
        if player.lives == 0:
            running = False

    window.fill((0, 0, 0))
    all_sprites.draw(window)

    text = font.render(f"Items left: {target_count} Lives: {player.lives}", True, WHITE)
    window.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

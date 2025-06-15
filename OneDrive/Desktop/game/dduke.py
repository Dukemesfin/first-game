import pygame
import time
import random

pygame.font.init()
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 700
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
STAR_WIDTH = 50
STAR_HEIGHT = 50
STAR_VAL = 6
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_VAL = 4
FONT = pygame.font.SysFont("pixle", 30)

# Game Setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space KILL")

# Background
background = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))

# Load images
player_image = pygame.transform.scale(pygame.image.load("spaceship.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
star_image = pygame.transform.scale(pygame.image.load("asteroid.png"), (STAR_WIDTH, STAR_HEIGHT))
enemy_image = pygame.transform.scale(pygame.image.load("ufo.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
boss_img = pygame.transform.scale(pygame.image.load("ufo.png"), (150, 100))  # separate variable

# Player setup
player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
screen_shake = 0

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.color = (255, 0, 0)
        self.speed = 30

    def move(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Boss class
class Boss:
    def __init__(self):
        self.image = boss_img
        self.rect = self.image.get_rect(midtop=(WIDTH // 2, -100))
        self.health = 5
        self.speed = 1
        self.direction = 1

    def move(self):
        self.rect.y += self.speed
        self.rect.x += self.direction * 3
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

    def draw(self, surface, offset):
        surface.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

def draw(player, elapsed_time, stars, bullets, score, enemies, render_offset, boss):
    WIN.fill((0, 0, 0))
    WIN.blit(background, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    score_text = FONT.render(f"Score: {score}", 1, "yellow")
    WIN.blit(score_text, (WIDTH - 150, 10))

    WIN.blit(player_image, (player.x + render_offset[0], player.y + render_offset[1]))

    for star in stars:
        WIN.blit(star_image, (star["rect"].x + render_offset[0], star["rect"].y + render_offset[1]))

    for enemy in enemies:
        WIN.blit(enemy_image, (enemy["rect"].x + render_offset[0], enemy["rect"].y + render_offset[1]))

    for bullet in bullets:
        bullet.draw(WIN)

    if boss:
        boss.draw(WIN, render_offset)

def game_over_screen(score):
    game_over_text = FONT.render(f"LOSER. Your Score: {score}", False, "white")
    WIN.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
    pygame.display.update()
    time.sleep(2)

def dduke():
    global screen_shake
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()

    score = 0
    star_add_increment = 2000
    star_count = 0

    enemy_add_increment = 4000
    enemy_count = 0

    boss = None
    boss_spawn_timer = 0

    stars = []
    enemies = []
    bullets = []
    game_over = False

    while run:
        dt = clock.tick(60)
        elapsed_time = time.time() - start_time
        star_count += dt
        enemy_count += dt
        boss_spawn_timer += dt

        if star_count > star_add_increment:
            for _ in range(2):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                dx = random.choice([-2, -1, 0, 1, 2])
                star = {"rect": pygame.Rect(star_x, STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT), "dx": dx}
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 20)
            star_count = 0

        if enemy_count > enemy_add_increment:
            for _ in range(1):
                enemy_x = random.randint(0, WIDTH - ENEMY_WIDTH)
                dx = random.choice([-2, -1, 0, 1, 2])
                enemy = {"rect": pygame.Rect(enemy_x, ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT), "dx": dx}
                enemies.append(enemy)
            enemy_add_increment = max(200, enemy_add_increment - 20)
            enemy_count = 0

        if boss_spawn_timer > 20000 and boss is None:
            boss = Boss()
            boss_spawn_timer = 0

        render_offset = [0, 0]
        if screen_shake > 0:
            render_offset[0] = random.randint(-4, 4)
            render_offset[1] = random.randint(-4, 4)
            screen_shake -= 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = Bullet(player.x + PLAYER_WIDTH // 2 - 2, player.y)
                bullets.append(bullet)
                screen_shake = 10

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.x -= 10
        if keys[pygame.K_d]:
            player.x += 10
        if keys[pygame.K_w]:
            player.y -= 10
        if keys[pygame.K_s]:
            player.y += 10

        player.x = max(0, min(WIDTH - PLAYER_WIDTH, player.x))
        player.y = max(0, min(HEIGHT - PLAYER_HEIGHT, player.y))

        for star in stars[:]:
            star["rect"].y += STAR_VAL
            star["rect"].x += star["dx"]
            if star["rect"].colliderect(player):
                stars.remove(star)
                game_over = True
                break

        for enemy in enemies[:]:
            enemy["rect"].y += ENEMY_VAL
            enemy["rect"].x += enemy["dx"]
            if enemy["rect"].colliderect(player):
                enemies.remove(enemy)
                game_over = True
                break

        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.y < 0:
                bullets.remove(bullet)
                continue

            for star in stars[:]:
                if bullet.rect.colliderect(star["rect"]):
                    bullets.remove(bullet)
                    stars.remove(star)
                    score += 1
                    break

            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy["rect"]):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 2
                    break

            if boss and bullet.rect.colliderect(boss.rect):
                bullets.remove(bullet)
                boss.health -= 1
                if boss.health <= 0:
                    boss = None
                    score += 10

        if boss:
            boss.move()
            if boss.rect.colliderect(player):
                game_over = True

        if game_over:
            game_over_screen(score)
            break

        draw(player, elapsed_time, stars, bullets, score, enemies, render_offset, boss)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    dduke()

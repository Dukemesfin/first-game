import pygame
import time
import random

pygame.font.init()
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 700
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
STAR_WIDTH = 50  # Adjusted size for stars
STAR_HEIGHT = 50  # Adjusted size for stars
STAR_VAL = 6
ENEMY_WIDTH = 50  # Adjusted size for stars
ENEMY_HEIGHT = 50  # Adjusted size for stars
ENEMY_VAL = 4
SCORE_VAL = 0
FONT = pygame.font.SysFont("pixle", 30)

# Game Setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space KILL")

# Background
background = pygame.transform.scale(pygame.image.load("Downloads/background.jpg"), (WIDTH, HEIGHT))

# Load the spaceship image (ensure the file is in the correct path)
player_image = pygame.image.load("Downloads/spaceship.png")  # Replace with your image file name
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))  # Scale image to fit player size

# Load the star (asteroid) image only once
star_image = pygame.image.load("Downloads/asteroid.png")  # Replace with your star image file name
star_image = pygame.transform.scale(star_image, (STAR_WIDTH, STAR_HEIGHT))  # Scale to fit star size

enemy_image = pygame.image.load("Downloads/ufo.png")  # Replace with your enemy image file name
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_WIDTH, ENEMY_HEIGHT))  # Scale to fit enemy size

# Player setup
player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
screen_shake = 0  # Initialize screen_shake variable

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)  # Small rectangle for the bullet
        self.color = (255, 0, 0)  # Red color
        self.speed = 30  # Bullet speed
    
    def move(self):
        self.rect.y -= self.speed  # Move the bullet upward
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)  # Draw the bullet


def draw(player, elapsed_time, stars, bullets, score, enemies, render_offset):
    WIN.fill((0, 0, 0))  # Fill the screen with black

    WIN.blit(background, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))  # Display time on screen
    
    score_text = FONT.render(f"Score: {score}", 1, "yellow")
    WIN.blit(score_text, (WIDTH - 150, 10))

    # Draw the player (spaceship image)
    WIN.blit(player_image, (player.x + render_offset[0], player.y + render_offset[1]))  # Apply screen shake offset to player
    
    # Draw all stars
    for star in stars:
        WIN.blit(star_image, (star.x + render_offset[0], star.y + render_offset[1]))  # Apply shake offset to stars

    # Draw all enemies
    for enemy in enemies:
        WIN.blit(enemy_image, (enemy.x + render_offset[0], enemy.y + render_offset[1]))  # Apply shake offset to enemies

    # Draw all bullets
    for bullet in bullets:
        bullet.draw(WIN)


def game_over_screen(score):
    game_over_text = FONT.render(f"LOSER. Your Score: {score}", False, "white")
    WIN.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
    pygame.display.update()
    time.sleep(2)  # Show game over text for 2 seconds


def dduke():
    global screen_shake  # Ensure screen_shake is recognized as a global variable
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    score = 0

    # Star and enemy generation variables
    star_add_increment = 2000  # Initial star spawn time
    star_count = 0

    enemy_add_increment = 4000  
    enemy_count = 0

    stars = []
    enemies = []  # Rename this to avoid confusion with enemy variable name
    bullets = []
    game_over = False  # Use this flag to track if the game is over

    while run:
        star_count += clock.tick(60)  # Limit to 60 FPS
        
        if star_count > star_add_increment:
            for _ in range(2):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 20)
            star_count = 0

        enemy_count += clock.tick(60)  # Limit to 60 FPS
        
        if enemy_count > enemy_add_increment:
            for _ in range(1):
                enemy_x = random.randint(0, WIDTH - ENEMY_WIDTH)
                enemy_rect = pygame.Rect(enemy_x, ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
                enemies.append(enemy_rect)
            enemy_add_increment = max(200, enemy_add_increment - 20)
            enemy_count = 0

        render_offset = [0, 0]  # Reset render offset each frame
        if screen_shake > 0:
            render_offset[0] = random.randint(-4, 4)  # Random horizontal shake offset
            render_offset[1] = random.randint(-4, 4)  # Random vertical shake offset
            screen_shake -= 2  # Decrease screen shake counter each frame
        else:
            render_offset = [0, 0]  # Reset the offset once the screen shake effect is over

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                run = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # If the spacebar is pressed, shoot
                    bullet = Bullet(player.x + PLAYER_WIDTH // 2 - 2, player.y)
                    bullets.append(bullet)
                    screen_shake =  10  # Start screen shake effect

        # Player movement
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_a]:
            player.x -= 10  
        if keys[pygame.K_d]:
            player.x += 10 
        if keys[pygame.K_w]:
            player.y -= 10  
        if keys[pygame.K_s]:
            player.y += 10 

        # Keep the player inside the screen bounds
        if player.x < 0:
            player.x = 0
        if player.x > WIDTH - PLAYER_WIDTH:
            player.x = WIDTH - PLAYER_WIDTH
        if player.y < 0:
            player.y = 0
        if player.y > HEIGHT - PLAYER_HEIGHT:
            player.y = HEIGHT - PLAYER_HEIGHT

        # Move stars
        for star in stars[:]:
            star.y += STAR_VAL
            if star.y > HEIGHT:
                game_over = True
                stars.remove(star)
            elif star.y >= player.y and star.colliderect(player):
                stars.remove(star)
                game_over = True
                break  # Stop further checking, player hit a star

        # Move enemies
        for enemy_rect in enemies[:]:
            enemy_rect.y += ENEMY_VAL
            if enemy_rect.y > HEIGHT:
                game_over = True
                enemies.remove(enemy_rect)
            elif enemy_rect.y >= player.y and enemy_rect.colliderect(player):
                enemies.remove(enemy_rect)
                game_over = True
                break  # Stop further checking, player hit an enemy

        # Move bullets and check collisions
        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.y < 0:
                bullets.remove(bullet)

            # Bullet collision with stars
            for star in stars[:]:
                if bullet.rect.colliderect(star):
                    bullets.remove(bullet)
                    stars.remove(star)
                    score += 1
                    break  # Stop further checking for this bullet

            # Bullet collision with enemies
            for enemy_rect in enemies[:]:
                if bullet.rect.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy_rect)
                    score += 2
                    break  # Stop further checking for this bullet

        if game_over:
            game_over_screen(score)
            break  # End the game loop after game over screen

        draw(player, elapsed_time, stars, bullets, score, enemies, render_offset)  # Draw everything
        pygame.display.update()

        elapsed_time = time.time() - start_time  # Update elapsed time

    pygame.quit()

if __name__ == "__main__":
    dduke()

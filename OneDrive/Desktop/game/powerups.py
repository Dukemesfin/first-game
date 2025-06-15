import pygame
import random

class PowerUp:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.type = random.choice(["double_bullet"])
        self.speed = 2
        if self.type == "double_bullet":
            self.image = pygame.transform.scale(pygame.image.load("powerup1.png"), (self.width, self.height))
        else:
            self.image = pygame.transform.scale(pygame.image.load("powerup3.png"), (self.width, self.height))

        

    def move(self):
        self.rect.y += self.speed


    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
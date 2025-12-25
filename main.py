import pygame
import sys
from game import Game
from settings import WIDTH, HEIGHT, TITLE

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

game = Game(screen)
game.run()

pygame.quit()
sys.exit()
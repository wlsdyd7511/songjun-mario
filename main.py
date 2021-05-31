import pygame
import sys

pygame.init()
pygame.display.set_caption('Sexy Songjun')
MAX_WIDTH = 800
MAX_HEIGHT = 400


def main():
    screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHIT))
    fps - pygame.time.Clock()

    char = pygame.image.load('image/')
    char_height = img1.get_size()[1]
    char_bottom = MAX_HEIGHT - char_height
    position = (50, dino_bottom)
    spd = (0, 0)
    jump_spd = 400
    is_bottom = True

    spike = pygame.image.load('image/')

    screen.blit(char, position)



if __name__ == '__main__':
    main()

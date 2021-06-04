import pygame
import sys

pygame.init()
pygame.display.set_caption('Songjun')
MAX_WIDTH = 800
MAX_HEIGHT = 400
bg_color = [2, 64, 77]

def main():
    screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    fps = pygame.time.Clock()

    char = [pygame.image.load('image/player/right1.png'), pygame.image.load('image/player/right2.png'), pygame.image.load('image/player/left1.png'), pygame.image.load('image/player/left2.png')]
    for i in range(len(char)):
        char[i] = pygame.transform.scale(char[i], (32, 32))
    char_height = char[0].get_size()[1]
    char_bottom = MAX_HEIGHT - char_height
    position = [50, char_bottom]
    spd = [0, 0]
    jump_spd = -10
    gravity = 0.4
    is_bottom = True
    is_right = False
    is_left = False

    spike = [pygame.image.load('image/spike/up.png'), pygame.image.load('image/spike/down.png'), pygame.image.load('image/spike/right.png'), pygame.image.load('image/spike/left.png')]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    is_left = True
                elif event.key == pygame.K_RIGHT:
                    is_right = True
                elif event.key == pygame.K_UP:
                    spd[1] = jump_spd
                    is_bottom = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    is_left = False
                elif event.key == pygame.K_RIGHT:
                    is_right = False


        if not is_bottom:
            spd[1] += gravity
        if position[1] > char_bottom:
            is_bottom = True
            spd[1] = 0
            position[1] = char_bottom
        position[0] += spd[0]
        position[1] += spd[1]
        screen.fill(tuple(bg_color))
        screen.blit(char[0], tuple(position))
        
        pygame.display.update()
        fps.tick(60)



if __name__ == '__main__':
    main()

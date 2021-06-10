import pygame
import sys

pygame.init()
pygame.display.set_caption('Songjun')
bg_color = [2, 64, 77]
END_LEVEL = 2


def main():
    level = 1
    current_level = 1
    with open('map/map1 숫자.txt', 'r') as f:
        map = [list(n.rstrip('\n')) for n in f.readlines()]
    width = len(map[0])
    height = len(map)
    screen = pygame.display.set_mode((width*16, height*16))
    fps = pygame.time.Clock()

    char = [pygame.image.load('image/player/right1.png'), pygame.image.load('image/player/right2.png'), pygame.image.load('image/player/left1.png'), pygame.image.load('image/player/left2.png')]
#     for i in range(len(char)):
#         char[i] = pygame.transform.scale(char[i], (32, 32))
    char_height = char[0].get_size()[1]
    position = [50, 50]
    spd = [0, 0]
    jump_spd = -7
    MAX_SPD = 1.5
    gravity = 0.4
    is_bottom = False
    is_right = False
    is_left = False
    direction = 0  # 0: stop, -1: left, 1: right

    grass = pygame.image.load('image/grass/grass.png')
    onlydirt = pygame.image.load('image/grass/grass2.png')
    chest = pygame.image.load('보물상지/보물상자.png')
    chest = pygame.transform.scale(chest, (32, 32))
    darkgrass = pygame.image.load('image/grass/grass3.png')
    block = pygame.image.load('image/block/block.png')
    spike = [pygame.image.load('image/spike/up.png'), pygame.image.load('image/spike/down.png'), pygame.image.load('image/spike/right.png'), pygame.image.load('image/spike/left.png')]
    flag = pygame.image.load('image/flag/flag.png')
    flag = pygame.transform.scale(flag, (16, 32))
    fake = pygame.image.load('image/flag/flag fake/flag fake.png')
    fake = pygame.transform.scale(fake, (16, 32))
    portal = pygame.image.load('image/portal/portal.png')
    portal = pygame.transform.scale(portal, (32, 32))
    position = spawn(height, width, map)


    while True:
        if level != current_level:
            if current_level == END_LEVEL:
                with open('map/clear.txt', 'r') as f:
                    map = [list(n.rstrip('\n')) for n in f.readlines()]
            else:
                with open(f'map/map{level} 숫자.txt', 'r') as f:
                    map = [list(n.rstrip('\n')) for n in f.readlines()]
            position = spawn(height, width, map)
            current_level = level

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
                    if is_bottom:
                        spd[1] = jump_spd
                        is_bottom = False
                elif event.key == pygame.K_LSHIFT:
                    MAX_SPD = 4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    is_left = False
                elif event.key == pygame.K_RIGHT:
                    is_right = False
                elif event.key == pygame.K_LSHIFT:
                    MAX_SPD = 2
        if not is_bottom:
            spd[1] += gravity

        direction = 0
        if is_right:
            direction += 1
        if is_left:
            direction -= 1
        if direction == 0:
            if spd[0] < -0.3:
                spd[0] += 0.3
            elif spd[0] > 0.3:
                spd[0] -= 0.3
            else:
                spd[0] = 0
        elif direction < 0:
            if spd[0] > 0:
                spd[0] -= 0.4
            elif spd[0] > -MAX_SPD+0.2:
                spd[0] -= 0.2
            else:
                spd[0] = -MAX_SPD
        else:
            if spd[0] < 0:
                spd[0] += 0.4
            elif spd[0] < MAX_SPD-0.2:
                spd[0] += 0.2
            else:
                spd[0] = MAX_SPD

        position[0] += spd[0]
        position[1] += spd[1]
        print(position)
        print(width)
        print()

        if position[0] <= 1:
            position[0] = 1
            if spd[0] < 0:
                spd[0] = 0
        elif position[0] >= (width * 16) - 31:
            position[0] = (width * 16) - 31
            if spd[0] > 0:
                spd[0] = 0

        if position[1] > (height * 16) - 16:
            spawn(height, width, map)

        screen.fill(tuple(bg_color))
        for h in range(height):
            for w in range(width):
                if map[h][w] == '1':
                    screen.blit(grass, (w*16, h*16))
                elif map[h][w] == '2':
                    screen.blit(block, (w*16, h*16))
                elif map[h][w] == '3':
                    screen.blit(spike[1], (w*16, h*16))
                elif map[h][w] == '5':
                    screen.blit(flag, (w*16, h*16))
                elif map[h][w] == '6':
                    screen.blit(fake, (w*16, h*16))
                elif map[h][w] == '7':
                    screen.blit(portal, (w*16, h*16))
                elif map[h][w] == '8':
                    screen.blit(darkgrass, (w*16, h*16))
                elif map[h][w] == '9':
                    screen.blit(onlydirt, (w*16, h*16))
                elif map[h][w] == '4':
                    screen.blit(chest, (w*16, h*16))
        screen.blit(char[0], tuple(position))

        char_block = [int(n//16) for n in position]
        if position[0]%16:
            under_block = [map[char_block[1]+1][char_block[0]], map[char_block[1]+1][char_block[0]+1]]
        else:
            under_block = [map[char_block[1]+1][char_block[0]]]
        if ('1' in under_block or '2' in under_block or '8' in under_block or '9' in under_block):
            is_bottom = True
            spd[1] = 0
            position[1] = char_block[1]*16
        else:
            is_bottom = False

        if position[1]%16 == 0:
            right_block = [map[char_block[1]][char_block[0]+1]]
            if position[0]%16 == 0:
                left_block = [map[char_block[1]][char_block[0]-1]]
            else:
                left_block = [map[char_block[1]][char_block[0]]]
        else:
            right_block = [map[char_block[1]][char_block[0]+1], map[char_block[1]+1][char_block[0]+1]]
            if position[0]%16 == 0:
                left_block = [map[char_block[1]][char_block[0]-1], map[char_block[1]+1][char_block[0]-1]]
            else:
                left_block = [map[char_block[1]][char_block[0]], map[char_block[1]+1][char_block[0]]]

        if '1' in right_block or '2' in right_block or '8' in right_block or '9' in right_block:
            if direction > 0:
                direction = 0
            if spd[0] > 0:
                spd[0] = 0
                position[0] = char_block[0] * 16
        if '1' in left_block or '2' in left_block or '8' in left_block or '9' in left_block:
            if direction < 0:
                direction = 0
            if spd[0] < 0:
                spd[0] = 0
                position[0] = (char_block[0]+1) * 16

        touched_block = []
        touched_block.append(map[int(position[1]/16)][int(position[0]/16)])
        touched_block.append(map[int((position[1]+15)/16)][int(position[0]/16)])
        touched_block.append(map[int(position[1]/16)][int(((position[0]+15)+15)/16)])
        touched_block.append(map[int((position[1]+15)/16)][int(((position[0]+15)+15)/16)])

        touched_spike = []
        touched_spike.append(map[int(position[1]/16)][int(position[0]/16)])
        touched_spike.append(map[int((position[1]+2)/16)][int(position[0]/16)])
        touched_spike.append(map[int(position[1]/16)][int(((position[0]+15)+15)/16)])
        touched_spike.append(map[int((position[1]+2)/16)][int(((position[0]+15)+15)/16)])

        if '5' in touched_block:
            level += 1
        
        if '4' in touched_block or '6' in touched_block or '3' in touched_spike:
            position = spawn(height, width, map)

        pygame.display.update()
        fps.tick(60)

def level():
    print('level')
    with open('map/map2 숫자.txt', 'r') as f:
            map = [list(n.rstrip('\n')) for n in f.readlines()]


def death():
    print('death')

def spawn(height, width, map):
    porition = [0, 0]
    for h in range(height):
        for w in range(width):
            if map[h][w] == '7':
                position = [w*16, h*16]
    return position



if __name__ == '__main__':
    main()

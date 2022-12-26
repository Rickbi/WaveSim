import pygame
from pygame.locals import *
from math import sin, pi

def apply_test(buff1, buff2):
    dam = 1
    n = len(buff1[0])
    re = [[0 for i in range(n)] for j in range(n)]
    for x in range(1,n-1):
        for y in range(1,n-1):
            re[y][x] = dam*(( buff1[y-1][x] + buff1[y+1][x] + buff1[y][x-1] + buff1[y][x+1])/2 - buff2[y][x])

    buff2[:] = buff1
    buff1[:] = re

def apply(buff1, buff2):
    dam = 1
    n = len(buff1[0])
    re = [[0 for i in range(n)] for j in range(n)]
    for x in range(1,n-1):
        for y in range(1,n-1):
            com = (buff1[y-1][x-1] + buff1[y+1][x-1] + buff1[y+1][x+1] + buff1[y-1][x+1])/2
            k = 3
            re[y][x] = dam*(( buff1[y-1][x] + buff1[y+1][x] + buff1[y][x-1] + buff1[y][x+1] + com )/k - buff2[y][x])

    buff2[:] = buff1
    buff1[:] = re

def apply_pressure(buff1, buff2):
    # buff1 -> Pressure
    # buff2 -> Velocity
    dam = 0.9
    n = len(buff1[0])

    # Update Velocity

    for y in range(1, n-1):
        for x in range(1, n-1):
            p = buff1[y][x]
            buff2[y][x][0] = buff2[y][x][0] + p - buff1[y - 1][x]
            buff2[y][x][1] = buff2[y][x][1] + p - buff1[y][x + 1]
            buff2[y][x][2] = buff2[y][x][2] + p - buff1[y + 1][x]
            buff2[y][x][3] = buff2[y][x][3] + p - buff1[y][x - 1]

    # Update Pressure
    for y in range(1,n-1):
        for x in range(1,n-1):
            buff1[y][x] -= 0.5*dam*sum(buff2[y][x])
    


def draw(screen, mat, wall, size, px, py, sep):
    for x in range(len(mat)):
        for y in range(len(mat[0])):
            if wall[x][y]:
                rect = pygame.Rect(px + x*(size + sep), py + y*(size + sep), size, size)
                pygame.draw.rect(screen, (255,0,0), rect)
            else:
                #c = int(127.5 + abs(mat[x][y])*127.5)
                c = int(127.5 + mat[x][y]*127.5)
                if 0 <= c <= 255:
                    rect = pygame.Rect(px + x*(size + sep), py + y*(size + sep), size, size)
                    pygame.draw.rect(screen, (c,c,c), rect)

def clickedPos(size, px, py, sep):
    x, y = pygame.mouse.get_pos()
    relPosx = x - px
    relPosy = y - py
    nx = relPosx//(size + sep)
    ny = relPosy//(size + sep)
    return nx, ny


def main():
    n = 100
    px = 10
    py = 10
    sep = 0
    tileSize = 8
    buff1 = [[0 for i in range(n)] for j in range(n)]
    buff2 = [[0 for i in range(n)] for j in range(n)]
    buff3 = [[[0,0,0,0] for i in range(n)] for j in range(n)]

    wall = [[0 for i in range(n)] for j in range(n)]
    for i in range(len(wall)):
        wall[0][i] = 1
        wall[-1][i] = 1
        wall[i][0] = 1
        wall[i][-1] = 1
    # De mayor a menor
    for i in range(0, len(wall)-57):
        wall[10][i] = 1
    for i in range(len(wall)-55, len(wall)-45):
        wall[10][i] = 1
    for i in range(len(wall)-43, len(wall)):
        wall[10][i] = 1

    size = (1500,900)
    run = True
    fps = 60

    wave = 1
    pulse = False
    pulse_t = 0
    pulse_a = 0
    pulse_p = (0,0)
    pulse_limit = 10#20
    pulse_w = 2*pi/pulse_limit

    pygame.init()
    pygame.display.set_caption(f'Wave Sim')
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    applyEvent = pygame.event.Event(USEREVENT + 1)
    pygame.time.set_timer(applyEvent, 1)

    while run:
        if pygame.event.get(QUIT):
            run = False
        for event in pygame.event.get(KEYUP):
            if event.key == K_1:
                wave = 1
            elif event.key == K_2:
                wave = 2
            elif event.key == K_3:
                wave = 3
            elif event.key == K_a:
                pulse = True
                pulse_p = 90, 50
            elif event.key == K_SPACE:
                buff1 = [[0 for i in range(n)] for j in range(n)]
                buff2 = [[0 for i in range(n)] for j in range(n)]
                buff3 = [[[0,0,0,0] for i in range(n)] for j in range(n)]
        for event in pygame.event.get(MOUSEBUTTONUP):
            if event.button == 3:
                cx, cy = clickedPos(tileSize, px, py, sep)
                pulse = True
                pulse_p = cx, cy
            if event.button == 1:
                cx, cy = clickedPos(tileSize, px, py, sep)
                if wall[cx][cy]:
                    wall[cx][cy] = 0
                else:
                    wall[cx][cy] = 1

        if pygame.event.get(USEREVENT + 1):
            if wave == 1:
                apply_test(buff1, buff2)
            elif wave == 2:
                apply(buff1, buff2)
            elif wave == 3:
                apply_pressure(buff1, buff3)

            for y in range(len(wall)):
                for x in range(len(wall[0])):
                    if wall[y][x]:
                        buff1[y][x] = 0
            
            #print(buff1[50][50])
            
            if pulse and pulse_t <= pulse_limit:
                pulse_a = sin(pulse_t*pulse_w)
                buff1[pulse_p[0]][pulse_p[1]] = pulse_a
                pulse_t += 1
                #print(pulse_a)
            elif pulse_t > pulse_limit:
                pulse = False
                pulse_t = 0
        
        #Region screen
        screen.fill((10,10,10))

        draw(screen, buff1, wall, tileSize, px, py, sep)
        #apply(buff1, buff2)

        pygame.display.flip()
        clock.tick(fps)
        pygame.display.set_caption(f'fps: {clock.get_fps()}')
        #end


if __name__ == '__main__':
    main()
import pygame
from pygame.locals import *

def apply(buff1, buff2):
    dam = 0.999
    n = len(buff1[0])
    re = [[0 for i in range(n)] for j in range(n)]
    for x in range(1,n-1):
        for y in range(1,n-1):
            re[y][x] = dam*(( buff1[y-1][x] + buff1[y+1][x] + buff1[y][x-1] + buff1[y][x+1] )/2 - buff2[y][x])
            if re[y][x] > 1:
                #print(re[y][x])
                re[y][x] = 1
            elif re[y][x] < 0:
                #print(re[y][x])
                re[y][x] = 0

    buff2[:] = buff1
    buff1[:] = re
    


def draw(screen, mat, size, px, py, sep):
    for x in range(len(mat)):
        for y in range(len(mat[0])):
            c = mat[x][y]*255
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
    buff1 = [[0 for i in range(n)] for j in range(n)]
    buff2 = [[0 for i in range(n)] for j in range(n)]
    buff1[10][10] = 1
    buff1[11][10] = 1
    buff1[12][10] = 1
    buff1[10][11] = 1
    buff1[11][11] = 1
    buff1[12][11] = 1
    buff1[10][12] = 1
    buff1[11][12] = 1
    buff1[12][12] = 1
    buff1[20][20] = 1
    buff1[21][20] = 1
    buff1[20][21] = 1
    buff1[21][21] = 1
    #buff2[20][10] = 1
    tileSize = 5

    size = (1500,900)
    run = True
    fps = 60

    pygame.init()
    pygame.display.set_caption(f'Wave Sim')
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    applyEvent = pygame.event.Event(USEREVENT + 1)
    pygame.time.set_timer(applyEvent, 60)

    while run:
        if pygame.event.get(QUIT):
            run = False
        for event in pygame.event.get(KEYUP):
            if event.key == K_a:
                apply(buff1, buff2)
        for event in pygame.event.get(MOUSEBUTTONUP):
            cx, cy = clickedPos(tileSize, px, py, sep)
            #print(cx, cy)
            buff1[cx][cy] = 1
            buff1[cx+1][cy] = 1
            buff1[cx-1][cy] = 1
            buff1[cx][cy+1] = 1
            buff1[cx][cy-1] = 1
            buff1[cx+1][cy+1] = 1
            buff1[cx+1][cy-1] = 1
            buff1[cx-1][cy-1] = 1
            buff1[cx-1][cy+1] = 1
        if pygame.event.get(USEREVENT + 1):
            apply(buff1, buff2)
        screen.fill((50,50,100))

        draw(screen, buff1, tileSize, px, py, sep)
        #apply(buff1, buff2)

        pygame.display.flip()
        clock.tick(fps)
        pygame.display.set_caption(f'fps: {clock.get_fps()}')



if __name__ == '__main__':
    main()
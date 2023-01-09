import pygame
from pygame.locals import *
from math import cos, sin, pi

def draw(screen, data, moveTo, scale):
    new_data = []
    for n, p in enumerate(data):
        x = n*scale[0] + moveTo[0]
        y = p*scale[1] + moveTo[1]
        new_data.append([x,y])

    pygame.draw.lines(screen, (255,255,255), False, new_data)

def step(data, dataPre, dt, dx, n, t, c):
    newData = [0 for i in range(n)]
    newData[0] = 0
    #newData[0] = -dataPre[0] + 2*data[0] + 2*c*(data[1] - data[0])
    for i in range(1,n-1):
        newData[i] = -dataPre[i] + 2*data[i] + c*(data[i+1] - 2*data[i] + data[i-1])
    newData[n-1] = 0
    #newData[n-1] = -dataPre[n-1] + 2*data[n-1] + 2*c*(data[n-2] - data[n-1])
    dataPre[:] = data
    data[:] = newData

def step2(data, dataPre, dataVel, dt, dx, n, t, c):
    # With a change of medium.
    newData = [0 for i in range(n)]
    newData[0] = 0
    #newData[0] = -dataPre[0] + 2*data[0] + 2*c*(data[1] - data[0])
    for i in range(1,n-1):
        #newData[i] = -dataPre[i] + 2*data[i] + 0.5*(dt/dx)**2*((dataVel[i] + dataVel[i+1])*(data[i+1] - data[i]) - (dataVel[i] + dataVel[i-1])*(data[i] - data[i-1]))
        newData[i] = -dataPre[i] + 2*data[i] + 2*(dt/dx)**2*((1/dataVel[i] + 1/dataVel[i+1])**-1*(data[i+1] - data[i]) - (1/dataVel[i] + 1/dataVel[i-1])**-1*(data[i] - data[i-1]))
    newData[n-1] = 0
    #newData[n-1] = -dataPre[n-1] + 2*data[n-1] + 2*c*(data[n-2] - data[n-1])
    dataPre[:] = data
    data[:] = newData

def step3(data, dataPre, dataVel, dt, dx, n, t, c):
    # With a change of medium.
    newData = [0 for i in range(n)]
    newData[0] = 0
    #newData[0] = -dataPre[0] + 2*data[0] + 2*c*(data[1] - data[0])
    for i in range(1,n-1):
        newData[i] = -dataPre[i] + 2*data[i] + dataVel[i]*(data[i+1] - 2*data[i] + data[i-1])
    newData[n-1] = 0
    #newData[n-1] = -dataPre[n-1] + 2*data[n-1] + 2*c*(data[n-2] - data[n-1])
    dataPre[:] = data
    data[:] = newData

def step4(data, dataPre, dt, dx, n, t, c, b):
    # Damped wave
    newData = [0 for i in range(n)]
    newData[0] = 0
    #newData[0] = -dataPre[0] + 2*data[0] + 2*c*(data[1] - data[0])
    for i in range(1,n-1):
        newData[i] = ((0.5*b*dt-1)*dataPre[i] + 2*data[i] + c*(data[i+1] - 2*data[i] + data[i-1]))/(1+0.5*b*dt)
    newData[n-1] = 0
    #newData[n-1] = -dataPre[n-1] + 2*data[n-1] + 2*c*(data[n-2] - data[n-1])
    dataPre[:] = data
    data[:] = newData

def main():
    size = (1500,900)
    run = True
    fps = 60

    L = 100
    dt = 0.1
    dx = 1
    n = int(L/dx)
    t = 0
    c = 1
    w = 1
    b = 0.1

    runSim = True

    data = [0 for i in range(n)]
    dataPre = [0 for i in range(n)]
    dataVel = [c - c*i/(2*n) for i in range(n)]
    dataVel = [c if i < L/2 else c/2 for i in range(n)]

    pulseSin = lambda t : -sin(pi*t/w)
    pulseTri = lambda t : -t if t < w/2 else -w + t
    pulseSqr = lambda t : 1 if t <= w else 0

    moveTo = [100, size[1]//2]
    scale = [10,100]

    pygame.init()
    pygame.display.set_caption('1D Wave Sim')
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    applyEvent = pygame.event.Event(USEREVENT + 1)
    pygame.time.set_timer(applyEvent, 10)

    while run:
        if pygame.event.get(QUIT):
            run = False
        for e in  pygame.event.get(KEYUP):
            if e.key == K_SPACE:
                runSim = not runSim
        if pygame.event.get(USEREVENT + 1):
            if runSim:
                #step(data, dataPre, dt, dx, n, t, c)
                #step2(data, dataPre, dataVel, dt, dx, n, t, c)
                #step3(data, dataPre, dataVel, dt, dx, n, t, c)
                step4(data, dataPre, dt, dx, n, t, c, b)
                if t <= w:
                    data[0] = pulseSin(t)
                t += dt
        #Region screen
        screen.fill((10,10,10))

        draw(screen, data, moveTo, scale)

        pygame.display.flip()
        clock.tick(fps)
        pygame.display.set_caption(f'fps: {clock.get_fps()}')
        #end    
        



if __name__ == "__main__":
    main()
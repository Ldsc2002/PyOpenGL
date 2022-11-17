import pygame
from pygame import *
from PyGL.gl import Renderer
import PyGL.shaders as shaders

deltaTime = 0.0

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((960, 540), DOUBLEBUF | OPENGL)

R = Renderer(screen)
R.setShaders(shaders.vertexShader, shaders.fragmentShader)
R.createObjects()

cubeX = 0
cubeZ = 0

running = True
while running:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        R.xCoord -= 2 * deltaTime
    if keys[pygame.K_RIGHT]:
        R.xCoord += 2 * deltaTime
    if keys[pygame.K_UP]:
        R.zCoord -= 2 * deltaTime
    if keys[pygame.K_DOWN]:
        R.zCoord += 2 * deltaTime

    if keys[pygame.K_e]:
        R.rotateZ(True)
    if keys[pygame.K_q]:
        R.rotateZ()

    if keys[pygame.K_w]:
        R.rotateX(True)
    if keys[pygame.K_s]:
        R.rotateX()

    if keys[pygame.K_a]:
        R.rotateY(True)
    if keys[pygame.K_d]:
        R.rotateY()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

    R.render()

    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time()/1000

pygame.quit()

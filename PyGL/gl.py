from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm
import numpy as np

rectVerts = np.array([ 
        0.5,  0.5,  0.5, 1, 0, 0, 
        0.5, -0.5,  0.5, 0, 1, 0, 
       -0.5, -0.5,  0.5, 0, 0, 1, 
       -0.5,  0.5,  0.5, 1, 1, 0,
        0.5,  0.5, -0.5, 1, 0, 1,
        0.5, -0.5, -0.5, 0, 1, 1,
       -0.5, -0.5, -0.5, 1, 1, 1,
       -0.5,  0.5, -0.5, 0, 0, 0 
    ], dtype = np.float32)

rectIndices = np.array([
        0, 1, 3,
        1, 2, 3,
        4, 5, 0,
        5, 1, 0,
        7, 6, 4,
        6, 5, 4,
        3, 2, 7,
        2, 6, 7,
        1, 5, 2,
        5, 6, 2,
        4, 0, 7,
        0, 3, 7
    ], dtype = np.uint32)

class Renderer(object):
    def __init__(this, screen):
        this.screen = screen
        _, _, this.width, this.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, this.width, this.height)

        this.projection = glm.perspective(glm.radians(60), this.width / this.height, 0.1, 1000)
        this.cubePos = glm.vec3(0,0,0)

        this.yaw = 0
        this.pitch = 0
        this.roll = 0

        this.xCoord = 0
        this.yCoord = 0
        this.zCoord = 0

    def translateCube(this):
        this.cubePos = glm.vec3(this.xCoord, this.yCoord, this.zCoord)

    def rotateX(this, reverse = False):
        if reverse:
            this.pitch -=5
        else:
            this.pitch += 5

    def rotateY(this, reverse = False):
        if reverse:
            this.yaw -=5
        else:
            this.yaw += 5

    def rotateZ(this, reverse = False):
        if reverse:
            this.roll -= 5
        else:
            this.roll += 5

    def setShaders(this, vertexShader, fragShader):
        if vertexShader is not None or fragShader is not None:
            this.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER), compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            this.activeShader = None

        glUseProgram(this.activeShader)

    def createObjects(this):
        this.VBO = glGenBuffers(1)
        this.EBO = glGenBuffers(1)
        this.VAO = glGenVertexArrays(1)

        glBindVertexArray(this.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, this.VBO)
        glBufferData(GL_ARRAY_BUFFER, rectVerts.nbytes, rectVerts, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, this.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, rectIndices.nbytes, rectIndices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)

    def calcObjMatrix(this, i):
        translate = glm.translate(i, this.cubePos)
        pitch = glm.rotate(i, glm.radians( this.pitch ), glm.vec3(1,0,0))
        yaw = glm.rotate(i, glm.radians( this.yaw ), glm.vec3(0,1,0))
        roll = glm.rotate(i, glm.radians( this.roll ), glm.vec3(0,0,1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, glm.vec3(1,1,1))
        model = translate * rotate * scale

        return model

    def calcViewMatrix(this, i):
        camTranslate = glm.translate(i, glm.vec3( 0, 0, 3))
        camPitch = glm.rotate(i, glm.radians(0), glm.vec3(1,0,0))
        camYaw = glm.rotate(i, glm.radians(0), glm.vec3(0,1,0))
        camRoll = glm.rotate(i, glm.radians(0), glm.vec3(0,0,1))
        camRotate = camPitch * camYaw * camRoll
        view = glm.inverse( camTranslate * camRotate )

        return view

    def render(this):
        this.translateCube()
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        i = glm.mat4(1)

        model = this.calcObjMatrix(i)
        view = this.calcViewMatrix(i)

        if this.activeShader:
            glUniformMatrix4fv(glGetUniformLocation(this.activeShader, "model"), 1, GL_FALSE, glm.value_ptr(model))
            glUniformMatrix4fv(glGetUniformLocation(this.activeShader, "view"), 1, GL_FALSE, glm.value_ptr(view))
            glUniformMatrix4fv(glGetUniformLocation(this.activeShader, "projection"), 1, GL_FALSE, glm.value_ptr(this.projection))

        glBindVertexArray(this.VAO)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

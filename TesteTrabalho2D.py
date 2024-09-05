from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import glm

# Variáveis globais para a câmera
camera_pos = np.array([0.0, 0.0, 5.0], dtype=np.float32)

def mat2list(M):
    matrix = []
    for i in range(0,4):
        matrix.append(list(M[i]))
    return matrix

def init():
    glEnable(GL_DEPTH_TEST)

def draw_skybox():
    glBegin(GL_QUADS)
    # Desenho simplificado do skybox (como antes)
    glEnd()

def draw_fixed_bar():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 0, 600, -1, 1)  # Configuração da projeção ortográfica

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1.0, 0.0, 0.0)  # Cor da barra
    glBegin(GL_QUADS)
    glVertex2f(10, 10)
    glVertex2f(200, 10)
    glVertex2f(200, 60)
    glVertex2f(10, 60)
    glEnd()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuração da visão da câmera
    glFrustum(-1, 1, -1, 1, 2, 100)
    matrizCamera = glm.lookAt(glm.vec3(camera_pos[0], camera_pos[1], camera_pos[2]), glm.vec3(-15, 0, 0), glm.vec3(0, 0, 1))
    glLoadMatrixf(mat2list(matrizCamera))

    draw_skybox()

    # Desenho da barra fixa
    draw_fixed_bar()

    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Skybox with Fixed Bar")

    init()
    glutDisplayFunc(display)
    
    glutMainLoop()

if __name__ == "__main__":
    main()

from OpenGL.GL import *
from OpenGL.GLUT import *

widthWindow = 500
heigthWindow = 500
FPS = 60

def inicio():
    glClearColor(1, 1, 1, 1)
    glPointSize(5)
    glLineWidth(3)

def redimensionaJanela(w, h):
    global widthWindow, heigthWindow
    widthWindow = w
    heigthWindow = h
    glViewport(0, 0, w, h)
    glutPostRedisplay()

def timer(v):

    glutTimerFunc(int(1000/FPS), timer, 0)

    # restante do código

    glutPostRedisplay()

def cubo(fill=False):

    if(fill):
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        glColor3f(1, 0, 0)
    else:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        glColor3f(0, 0, 0)

    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(0, 1)
    glVertex2f(1, 1)
    glVertex2f(1, 0)
    glEnd()

def triangulo(fill=False):

    if(fill):
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        glColor3f(1, 0, 0)
    else:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        glColor3f(0, 0, 0)

    glBegin(GL_TRIANGLES)
    glVertex2f(0, 0)
    glVertex2f(1, 0)
    glVertex2f(0, 1)
    glEnd()

def desenha():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 17, 0, 17, -1, 1)

    # cubo(True)
    # cubo()

    # triangulo(True)
    # triangulo()

    glColor3f(1, 0, 0)
    glBegin(GL_POINTS)
    glVertex2f(2, 2)
    glEnd()

    glFlush()

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(widthWindow, heigthWindow)
glutInitWindowPosition(0,0)
glutCreateWindow('Primitivas')
inicio()
glutTimerFunc(int(1000/FPS), timer, 0)
glutReshapeFunc(redimensionaJanela)
glutDisplayFunc(desenha)
glutMainLoop()
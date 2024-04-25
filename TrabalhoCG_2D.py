from OpenGL.GL import *
from OpenGL.GLUT import *

widthWindow = 500
heigthWindow = 500
FPS = 60

def inicio():
    glClearColor(0, 0, 0, 1)
    glPointSize(3)
    glLineWidth(3)
    glEnable(GL_MULTISAMPLE)

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

def cubo(r, g, b, fill=False):

    if(fill):
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        glColor3f(r, g, b)
    else:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        glColor3f(r, g, b)

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

class Campo:

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    def desenha(self):
        glPushMatrix()
        glTranslatef(2, 2, 0)

        glPushMatrix()
        glScalef(self.largura, self.altura, 1)
        cubo(0, 1, 0, True)
        cubo(1, 1, 1)
        glPopMatrix()

        
        glPushMatrix()
        glTranslatef(self.largura/4, 0, 0)
        glScalef(self.largura/2, self.altura/8, 1)
        cubo(1, 1, 1)
        glPopMatrix()
                
        glPushMatrix()
        glTranslatef(self.largura/4, self.altura, 0)
        glScalef(self.largura/2, -self.altura/8, 1)
        cubo(1, 1, 1)
        glPopMatrix()

        glPointSize(70)
        glColor3f(1, 1, 1)
        glBegin(GL_POINTS)
        glVertex2f(self.largura/2, self.altura/2)
        glEnd()
        
        glPointSize(65)
        glColor3f(0, 1, 0)
        glBegin(GL_POINTS)
        glVertex2f(self.largura/2, self.altura/2)
        glEnd()

        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        glVertex2f(           0, self.altura/2)
        glVertex2f(self.largura, self.altura/2)
        glEnd()

        glPopMatrix()

def desenha():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 17, 0, 17, -1, 1)

    # cubo(True)
    # cubo()

    # triangulo(True)
    # triangulo()

    # glColor3f(1, 0, 0)
    # glBegin(GL_POINTS)
    # glVertex2f(2, 2)
    # glEnd()

    campo = Campo(5, 10)
    campo.desenha()

    glFlush()

glutInit()
glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(widthWindow, heigthWindow)
glutInitWindowPosition(0,0)
glutCreateWindow('Primitivas')
inicio()
glutTimerFunc(int(1000/FPS), timer, 0)
glutReshapeFunc(redimensionaJanela)
glutDisplayFunc(desenha)
glutMainLoop()
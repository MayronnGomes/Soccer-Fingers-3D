import CONSTS
from Cube import *

class Formation:

    def __init__(self):
        self.option = 1

    def desenha(self, tela):
        cube = Cube()

        glPushMatrix()
        glTranslatef(-CONSTS.mundoLar, -CONSTS.mundoAlt, 0)
        glScalef(2 * CONSTS.mundoLar, 2 * CONSTS.mundoAlt, 1)
        glBindTexture(GL_TEXTURE_2D, CONSTS.TELAS[tela])
        glColor3f(1, 1, 1)
        cube.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

        if self.option == 1:
            glPushMatrix()
            glScalef(-1, 1, 1)
            glColor3f(0, 0, 1)
            glTranslatef(10.9, -1.2, 0)
            self.desenhaContorno()
            glPopMatrix()
        elif self.option == 2:
            glPushMatrix()
            glScalef(-1, 1, 1)
            glColor3f(0, 0, 1)
            glTranslatef(0.75, -1.2, 0)
            self.desenhaContorno()
            glPopMatrix()
        elif self.option == 3:
            glPushMatrix()
            glColor3f(0, 0, 1)
            glTranslatef(0.75, -1.2, 0)
            self.desenhaContorno()
            glPopMatrix()
        elif self.option == 4:
            glPushMatrix()
            glColor3f(0, 0, 1)
            glTranslatef(10.9, -1.2, 0)
            self.desenhaContorno()
            glPopMatrix()
        elif self.option == 5:
            glPushMatrix()
            glScalef(-1, -1, 1)
            glColor3f(0, 0, 1)
            glTranslatef(10.9, 2.25, 0)
            self.desenhaContorno()
            glPopMatrix()
        elif self.option == 6:
            glPushMatrix()
            glScalef(-1, -1, 1)
            glColor3f(0, 0, 1)
            glTranslatef(0.75, 2.25, 0)
            self.desenhaContorno()
            glPopMatrix()
        elif self.option == 7:
            glPushMatrix()
            glScalef(1, -1, 1)
            glColor3f(0, 0, 1)
            glTranslatef(0.75, 2.25, 0)
            self.desenhaContorno()
            glPopMatrix()
        elif self.option == 8:
            glPushMatrix()
            glScalef(1, -1, 1)
            glColor3f(0, 0, 1)
            glTranslatef(10.9, 2.25, 0)
            self.desenhaContorno()
            glPopMatrix()

    def desenhaContorno(self):
        cube = Cube()
        glPushMatrix()
        glScalef(8.7, 8.6, 1)
        cube.desenha()
        glPopMatrix()
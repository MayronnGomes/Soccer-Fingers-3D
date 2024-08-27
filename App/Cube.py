from OpenGL.GL import *

class Cube:

    def __init__(self) -> None:
        pass

    def desenha(self, fill=False, invertido=False):

        if fill:
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        else:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

        if invertido:
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex2f(1, 0)
            glTexCoord2f(0, 1); glVertex2f(1, 1)
            glTexCoord2f(1, 1); glVertex2f(0, 1)
            glTexCoord2f(1, 0); glVertex2f(0, 0)
            glEnd()
        else:
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex2f(0, 0)
            glTexCoord2f(0, 1); glVertex2f(0, 1)
            glTexCoord2f(1, 1); glVertex2f(1, 1)
            glTexCoord2f(1, 0); glVertex2f(1, 0)
            glEnd()
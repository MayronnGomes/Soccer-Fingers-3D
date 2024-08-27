import glm
import CONSTS
from Cube import *

class Bola:

    def __init__(self, raio):
        self.raio = raio
        self.pos = glm.vec3(0, 0, 0)

    def desenha(self):
        bola = Cube()
        
        glBindTexture(GL_TEXTURE_2D, CONSTS.texBola)
        bola.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)

    def desenha_progressbar(self):
        bar = Cube()

        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, self.pos.z)
        glRotatef(CONSTS.angleProgressbar + 90, 0, 0, 1)
        glTranslatef(-1/4, -3/2, 0)
        glScalef(1/2, 3, 1)
        glBindTexture(GL_TEXTURE_2D, CONSTS.texProgBar)
        bar.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

    def move(self):

        self.pos.x += CONSTS.velocidade.x
        self.pos.y += CONSTS.velocidade.y

        CONSTS.deslocamento.x += CONSTS.velocidade.x
        CONSTS.deslocamento.y += CONSTS.velocidade.y
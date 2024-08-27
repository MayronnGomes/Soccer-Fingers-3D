import CONSTS
import glm
from Cube import *

class Jogador:

    def __init__(self, raio, time, posicao):
        self.raio = raio
        self.time = time
        self.posicao = posicao

    def desenha(self):
        jogador = Cube()
        glBindTexture(GL_TEXTURE_2D, self.time)
        glPushMatrix()
        glTranslatef(self.posicao.x - self.raio/2, self.posicao.y - self.raio/2, self.posicao.z)
        glScalef(self.raio, self.raio, 1)
        jogador.desenha(True)
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)     

    def verifica_colisao(self, bola):
        if CONSTS.bolaRaio/2 + self.raio/2 > glm.distance(self.posicao, bola.pos):
            C = self.posicao - bola.pos
            CONSTS.normal = glm.normalize(C)
            return True
        CONSTS.normal = glm.vec3(0, 0, 0)
        return False

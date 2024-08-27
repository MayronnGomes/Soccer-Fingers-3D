import CONSTS
from Cube import *
from Jogador import *

class Placar:

    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        self.score1 = 0
        self.score2 = 0

    def desenha(self):
        cubo = Cube()

        glPushMatrix()
        glTranslatef(0,3,0)
        glScalef(1,1/1.5,1)
        
        glPushMatrix() #desenha o fundo cinza
        glColor3f(0.188, 0.184, 0.176) # vermelho, verde, azul
        glTranslatef(-12, 8.3, 0)
        glScalef(24, 4.2, 1)
        cubo.desenha(True)
        glPopMatrix()
        
        glPushMatrix() #desenha lado brando dir
        glColor3f(0.933,0.933,0.933) # vermelho, verde, azul
        glTranslatef(0, 10.1, 0)
        glScalef(12, 2.4, 1)
        cubo.desenha(True)
        glPopMatrix()
        
        glPushMatrix() #desenha lado brando esq
        glColor3f(0.933,0.933,0.933) # vermelho, verde, azul
        glTranslatef(0, 10.1, 0)
        glScalef(-12, 2.4, 1)
        cubo.desenha(True)
        glPopMatrix()

        glPushMatrix() #desenha lado cinza dir
        glColor3f(0.753,0.753,0.753) # vermelho, verde, azul
        glTranslatef(0,9.7,0)
        glScalef(5, 2.8, 1)
        cubo.desenha(True)
        glPopMatrix()

        glPushMatrix() #desenha lado cinza esq
        glColor3f(0.753,0.753,0.753) # vermelho, verde, azul
        glTranslatef(0,9.7,0)
        glScalef(-5, 2.8, 1)
        cubo.desenha(True)
        glPopMatrix()

        glPushMatrix() # desenha o quadrado do meio
        glColor3f(0.290, 0.290, 0.282) # vermelho, verde, azul
        glTranslatef(-1.5,8.8,0)
        glScalef(3, 3.7, 1)
        cubo.desenha(True)
        glPopMatrix()

        glPopMatrix()
        
        glPushMatrix() # times
        jogador1 = Jogador(1.5, CONSTS.TIME[self.time1], glm.vec3(-11, 10.52, 0))
        jogador2 = Jogador(1.5, CONSTS.TIME[self.time2], glm.vec3(11, 10.52, 0))

        jogador1.desenha()
        jogador2.desenha()
        glPopMatrix()

        glPushMatrix() #desenha o nome esq
        glTranslatef(-9, 9.9, 0)
        glScalef(2.4, 1.35, 1)
        glBindTexture(GL_TEXTURE_2D, CONSTS.SIGLAS[self.time1])
        cubo.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

        glPushMatrix() #desenha o nome direito
        glTranslatef(6, 9.9, 0)
        glScalef(2.4, 1.35, 1)
        glBindTexture(GL_TEXTURE_2D, CONSTS.SIGLAS[self.time2])
        cubo.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

        glPushMatrix() #desenha a logo
        glColor(1, 1, 1)
        glTranslatef(-1, 9.1, 0)
        glScalef(2, 2, 1)
        cubo.desenha(True)
        glPopMatrix()

        glPushMatrix() #desenha o placar esq
        glColor(1, 1, 1)
        glTranslatef(-4, 9.65, 0)
        glScalef(1.5, 1.5, 1)
        glBindTexture(GL_TEXTURE_2D, CONSTS.PLACAR[str(self.score1)])
        cubo.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

        glPushMatrix() #desenha o placar dir
        glColor(1, 1, 1)
        glTranslatef(2.5, 9.65, 0)
        glScalef(1.5, 1.5, 1)
        glBindTexture(GL_TEXTURE_2D, CONSTS.PLACAR[str(self.score2)])
        cubo.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()
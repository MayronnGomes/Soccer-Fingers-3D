import glm
import CONSTS
from Cube import *
from Util import *

class Campo:
    
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.lightDiffuse = glm.vec3(1.0)      # Id               
        self.surfaceDiffuse = glm.vec3(1.0)    # Kd       
        self.lightSpecular = glm.vec3(1.0)     # Is
        self.surfaceSpecular = glm.vec3(0.5)   # Ks               
        self.surfaceShine = 250                # e

    def desenha(self):
        gramado = Cube()

        glPushMatrix()
        glScalef(self.largura, self.altura, 1)
        glBindTexture(GL_TEXTURE_2D, CONSTS.texCampo)
        gramado.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

    def desenha_gol(self):
        filename = "../Texturas/Soccergoal.obj"
        vertices, _, normals, faces = load_obj_gol(filename)
        
        glPushMatrix()
        glTranslatef(-1, self.altura/2, 1.5)
        glScalef(1, 1.2, 1.5)
    
        for face in faces:
            if len(face) == 3:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_POLYGON)
            
            for vertex, _, normal in face:
                cor = shading(vertices[vertex], normals[normal], self)
                glColor3f(cor.x, cor.y, cor.z)
                glVertex3f(*vertices[vertex])
            
            glEnd()

        glPopMatrix()

    def verifica_colisao(self, bola):
        if (bola.pos.y + CONSTS.bolaRaio/2 >= CONSTS.campoAlt/2) and (CONSTS.velocidade.y > 0):        # A POSITIVO
            CONSTS.normal = glm.vec3(0, 1, 0)
            return True
        elif (bola.pos.y - CONSTS.bolaRaio/2 <= -CONSTS.campoAlt/2) and (CONSTS.velocidade.y < 0):     # A NEGATIVO
            CONSTS.normal = glm.vec3(0, 1, 0)
            return True
        elif (bola.pos.x + CONSTS.bolaRaio/2 >= CONSTS.campoLar/2 + 2) and (CONSTS.velocidade.x > 0):  # B POSITIVO
            CONSTS.normal = glm.vec3(1, 0, 0)
            return True
        elif (bola.pos.x - CONSTS.bolaRaio/2 <= -CONSTS.campoLar/2 - 2) and (CONSTS.velocidade.x < 0): # B NEGATIVO
            CONSTS.normal = glm.vec3(1, 0, 0)
            return True
        elif (bola.pos.x + CONSTS.bolaRaio/2 > CONSTS.campoLar/2) and (bola.pos.y + CONSTS.bolaRaio/2 >= 2.4) and (bola.pos.y + CONSTS.bolaRaio/2 - CONSTS.velocidade.y < 2.4) and (CONSTS.velocidade.y > 0):     # E POSITIVO
            CONSTS.normal = glm.vec3(0, 1, 0)
            return True
        elif (bola.pos.x - CONSTS.bolaRaio/2 < -CONSTS.campoLar/2) and (bola.pos.y + CONSTS.bolaRaio/2 >= 2.4) and (bola.pos.y + CONSTS.bolaRaio/2 - CONSTS.velocidade.y < 2.4) and (CONSTS.velocidade.y > 0):    # E NEGATIVO
            CONSTS.normal = glm.vec3(0, 1, 0)
            return True
        elif (bola.pos.x + CONSTS.bolaRaio/2 >= CONSTS.campoLar/2) and (bola.pos.y + CONSTS.bolaRaio/2 >= 2.4) and (CONSTS.velocidade.x > 0):    # C POSITIVO
            CONSTS.normal = glm.vec3(1, 0, 0)
            return True
        elif (bola.pos.x - CONSTS.bolaRaio/2 <= -CONSTS.campoLar/2) and (bola.pos.y + CONSTS.bolaRaio/2 >= 2.4) and (CONSTS.velocidade.x < 0):   # C NEGATIVO
            CONSTS.normal = glm.vec3(1, 0, 0)
            return True
        elif (bola.pos.x + CONSTS.bolaRaio/2 > CONSTS.campoLar/2) and (bola.pos.y - CONSTS.bolaRaio/2 <= -2.4) and (bola.pos.y - CONSTS.bolaRaio/2 - CONSTS.velocidade.y > -2.4) and (CONSTS.velocidade.y < 0):    # F POSITIVO
            CONSTS.normal = glm.vec3(0, 1, 0)
            return True
        elif (bola.pos.x - CONSTS.bolaRaio/2 < -CONSTS.campoLar/2) and (bola.pos.y - CONSTS.bolaRaio/2 <= -2.4) and (bola.pos.y - CONSTS.bolaRaio/2 - CONSTS.velocidade.y > -2.4) and (CONSTS.velocidade.y < 0):   # F NEGATIVO
            CONSTS.normal = glm.vec3(0, 1, 0)
            return True
        elif (bola.pos.x + CONSTS.bolaRaio/2 >= CONSTS.campoLar/2) and (bola.pos.y - CONSTS.bolaRaio/2 <= -2.4) and (CONSTS.velocidade.x > 0):   # D POSITIVO
            CONSTS.normal = glm.vec3(1, 0, 0)
            return True
        elif (bola.pos.x - CONSTS.bolaRaio/2 <= -CONSTS.campoLar/2) and (bola.pos.y - CONSTS.bolaRaio/2 <= -2.4) and (CONSTS.velocidade.x < 0):  # D NEGATIVO
            CONSTS.normal = glm.vec3(1, 0, 0)
            return True
        else:
            CONSTS.normal = glm.vec3(0, 0, 0)
            return False
        
    def colisao_gol(self, bola, placar):
        if (bola.pos.x - CONSTS.bolaRaio/2 > 15) and (abs(bola.pos.y) + CONSTS.bolaRaio/2 <= 2.4): # gol direito
            placar.score1 += 1
            return True
        elif (bola.pos.x + CONSTS.bolaRaio/2 < -15) and (abs(bola.pos.y) + CONSTS.bolaRaio/2 <= 2.4): # gol esquerdo
            placar.score2 += 1
            return True
        else:
            return False

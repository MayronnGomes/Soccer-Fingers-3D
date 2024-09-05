import CONSTS
from Util import *
from OpenGL.GL import *

class Cilindro:

    def __init__(self, altura, raio, textura):
        self.altura = altura
        self.raio = raio
        self.textura = textura
        self.camisa = CONSTS.CAMISAS_TIME[self.textura]
        self.lightDiffuse = glm.vec3(1.0)      # Id               
        self.surfaceDiffuse = glm.vec3(1,1,1)  # Kd       
        self.lightSpecular = glm.vec3(1.0)     # Is
        self.surfaceSpecular = glm.vec3(0.5)   # Ks               
        self.surfaceShine = 128                # e

    def desenha(self):
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

        glColor3f(self.camisa.x, self.camisa.y, self.camisa.z)
        
        # Divisões ao longo da altura e circunferência
        altura_div = self.altura / CONSTS.divisaoCilindro
        angulo_div = (360 / CONSTS.divisaoCilindro)  # Divisões angulares em graus

        glBegin(GL_QUADS)
        
        for i in range(CONSTS.divisaoCilindro):
            for j in range(CONSTS.divisaoCilindro):
                # Calcula os ângulos para os vértices ao redor da circunferência
                angle1 = i * angulo_div
                angle2 = (i + 1) * angulo_div
                
                # Calcula as alturas para os vértices ao longo do cilindro
                z1 = j * altura_div
                z2 = (j + 1) * altura_div

                # Vértices para o quadrado na superfície do cilindro
                v1 = computeCylinderCoord(z1, angle1, self.raio)
                v2 = computeCylinderCoord(z1, angle2, self.raio)
                v3 = computeCylinderCoord(z2, angle2, self.raio)
                v4 = computeCylinderCoord(z2, angle1, self.raio)
                
                # Coordenadas de textura baseadas na altura e ângulo
                tex_coord1 = (i / CONSTS.divisaoCilindro, j / CONSTS.divisaoCilindro)
                tex_coord2 = ((i + 1) / CONSTS.divisaoCilindro, j / CONSTS.divisaoCilindro)
                tex_coord3 = ((i + 1) / CONSTS.divisaoCilindro, (j + 1) / CONSTS.divisaoCilindro)
                tex_coord4 = (i / CONSTS.divisaoCilindro, (j + 1) / CONSTS.divisaoCilindro)
                
                # Vértices e coordenadas de textura para o quadrado
                glTexCoord2f(*tex_coord1)
                glVertex3f(v1.x, v1.y, v1.z)
                
                glTexCoord2f(*tex_coord2)
                glVertex3f(v2.x, v2.y, v2.z)
                
                glTexCoord2f(*tex_coord3)
                glVertex3f(v3.x, v3.y, v3.z)
                
                glTexCoord2f(*tex_coord4)
                glVertex3f(v4.x, v4.y, v4.z)
        
        glEnd()

        # Desenhar a tampa superior
        glBindTexture(GL_TEXTURE_2D, CONSTS.TIME[self.textura])
        self.desenha_tampa(self.raio, self.altura, CONSTS.divisaoCilindro)
        glBindTexture(GL_TEXTURE_2D, 0)

    def desenha_tampa(self, raio, z, divisao):
        """Função para desenhar a tampa (topo ou base) do cilindro"""
        angulo_div = (360 / divisao)  # Divisões angulares em graus

        glBegin(GL_TRIANGLE_FAN)
        glTexCoord2f(0.5, 0.5)  # Coordenada de textura para o centro
        glVertex3f(0, 0, z)  # Centro da tampa

        for i in range(divisao + 1):
            angle = i * angulo_div
            v = computeCylinderCoord(0, angle, raio)
            
            # Coordenada de textura baseada no ângulo
            tex_coord = (0.5 + 0.5 * math.cos(math.radians(angle)), 0.5 + 0.5 * math.sin(math.radians(angle)))

            glTexCoord2f(*tex_coord)
            glVertex3f(v.x, v.y, z)
        
        glEnd()

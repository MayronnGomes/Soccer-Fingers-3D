import glm
import CONSTS
from Util import *

class Bola:

    def __init__(self, raio):
        self.raio = raio
        self.pos = glm.vec3(0, 0, 0)
        self.lightDiffuse = glm.vec3(1.0)      # Id               
        self.surfaceDiffuse = glm.vec3(1.0)    # Kd       
        self.lightSpecular = glm.vec3(1.0)     # Is
        self.surfaceSpecular = glm.vec3(0.5)   # Ks               
        self.surfaceShine = 250                # e

    def desenha(self):
        vertices, faces, normals, face_materials = load_obj('../Texturas/Ball.obj')
        # Definir cores com base no material
        color_map = {
            'Bianco': (1.0, 1.0, 1.0),  # Branco
            'Nero.001': (0.0, 0.0, 0.0)    # Preto
        }

        glPushMatrix()

        for i, face in enumerate(faces):
            if len(face) == 3:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_POLYGON)

            material_name = face_materials[i]
            color = color_map.get(material_name, (1.0, 1.0, 1.0))  # Default to white if material not found

            for vertex in face:
                cor = shading(vertices[vertex], normals[vertex], self) * color
                glColor3f(cor.x, cor.y, cor.z)
                glVertex3f(*vertices[vertex])

            glEnd()
        
        glPopMatrix()

    def move(self):

        # self.pos += CONSTS.t * CONSTS.forca
        # print(f'pos {self.pos}')
        # print(f'forca {CONSTS.forca}')
        # print(f'deslocamento {CONSTS.deslocamento}')
        # print()
        # CONSTS.deslocamento += CONSTS.t * CONSTS.forca

        # if CONSTS.deslocamento.x >= CONSTS.forca.x * 3/4:
        #     CONSTS.t = max(0.3, CONSTS.t - CONSTS.aceleracao)

        self.pos.x += CONSTS.velocidade.x
        self.pos.y += CONSTS.velocidade.y

        CONSTS.deslocamento.x += CONSTS.velocidade.x
        CONSTS.deslocamento.y += CONSTS.velocidade.y
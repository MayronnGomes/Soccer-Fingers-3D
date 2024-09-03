import glm
import CONSTS
from Util import *

class Bola:

    def __init__(self, raio):
        self.raio = raio
        self.pos = glm.vec3(0, 0, 0)

    def desenha(self):
        vertices, faces, face_materials = load_obj('../Texturas/Ball.obj')
        # Definir cores com base no material
        color_map = {
            'Bianco': (1.0, 1.0, 1.0),  # Branco
            'Nero.001': (0.0, 0.0, 0.0)    # Preto
        }

        glPushMatrix()
        # glTranslatef(0, 0, CONSTS.bolaRaio)

        for i, face in enumerate(faces):
            if len(face) == 3:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_POLYGON)

            material_name = face_materials[i]
            color = color_map.get(material_name, (1.0, 1.0, 1.0))  # Default to white if material not found
            glColor3fv(color)

            for vertex in face:
                glVertex3fv(vertices[vertex])

            glEnd()
        
        glPopMatrix()

    def move(self):

        self.pos.x += CONSTS.velocidade.x
        self.pos.y += CONSTS.velocidade.y

        CONSTS.deslocamento.x += CONSTS.velocidade.x
        CONSTS.deslocamento.y += CONSTS.velocidade.y
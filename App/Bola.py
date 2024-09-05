import glm
import CONSTS
from Util import *

class Bola:

    def __init__(self, raio):
        self.raio = raio
        self.pos = glm.vec3(0, 0, 0)
        self.lightPosition = glm.vec3(0, 0, 30)
        self.lightAmbient = glm.vec3(0.1)    
        self.lightDiffuse = glm.vec3(1.0)                    
        self.lightSpecular = glm.vec3(1.0)  
        self.surfaceAmbient = glm.vec3(0.1)         
        self.surfaceDiffuse = glm.vec3(1,1,1)              
        self.surfaceSpecular = glm.vec3(0.5)                      
        self.surfaceShine = 128


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

        self.pos.x += CONSTS.velocidade.x
        self.pos.y += CONSTS.velocidade.y

        CONSTS.deslocamento.x += CONSTS.velocidade.x
        CONSTS.deslocamento.y += CONSTS.velocidade.y
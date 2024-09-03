from OpenGL.GL import *
from OpenGL.GLUT import *
import glm
from PIL import Image
import math

def load_obj(filename):
    vertices = []
    textures = []
    normals = []
    faces = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Linha de vértice
                parts = line.split()
                vertex = list(map(float, parts[1:4]))
                vertices.append(vertex)
            elif line.startswith('vt '):  # Linha de textura
                parts = line.split()
                texture = list(map(float, parts[1:3]))
                textures.append(texture)
            elif line.startswith('vn '):  # Linha de normal
                parts = line.split()
                normal = list(map(float, parts[1:4]))
                normals.append(normal)
            elif line.startswith('f '):  # Linha de face
                parts = line.split()
                face = []
                for part in parts[1:]:
                    vals = part.split('/')
                    vertex_index = int(vals[0]) - 1
                    texture_index = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else None
                    normal_index = int(vals[2]) - 1 if len(vals) > 2 and vals[2] else None
                    face.append((vertex_index, texture_index, normal_index))
                faces.append(face)

    return vertices, textures, normals, faces

def draw_obj(vertices, textures, normals, faces):
    for face in faces:
        if len(face) == 3:
            glBegin(GL_TRIANGLES)
        else:
            glBegin(GL_POLYGON)
        
        for vertex, texture, normal in face:
            if texture is not None:
                glTexCoord2fv(textures[texture])
            if normal is not None:
                glNormal3fv(normals[normal])
            glVertex3fv(vertices[vertex])
        
        glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Posicionando a câmera
    glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 0, 1))

    glScalef(0.1, 0.1, 0.1)

    draw_obj(vertices, textures, normals, faces)

    glutSwapBuffers()

def init_gl():
    # glDisable(GL_LIGHTING)  # Desabilita iluminação
    # glDisable(GL_COLOR_MATERIAL)  # Desabilita materiais
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LEQUAL)

if __name__ == "__main__":
    # Carregando o arquivo OBJ
    filename = "goal.obj"
    vertices, textures, normals, faces = load_obj(filename)

    # Inicializando a janela OpenGL
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OBJ Viewer")
    glutDisplayFunc(display)

    init_gl()

    glutMainLoop()

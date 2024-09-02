from OpenGL.GL import *
from OpenGL.GLUT import *
import glm 
from PIL import Image
import math

def load_obj(filename):
    vertices = []
    normals = []
    faces = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Linha de vértice
                parts = line.split()
                vertex = list(map(float, parts[1:4]))
                vertices.append(vertex)
            elif line.startswith('vn '):  # Linha de normal
                parts = line.split()
                normal = list(map(float, parts[1:4]))
                normals.append(normal)
            elif line.startswith('f '):  # Linha de face
                parts = line.split()
                face = []
                for part in parts[1:]:
                    vals = part.split('//')
                    vertex_index = int(vals[0]) - 1  # Convertendo para índice 0-based
                    normal_index = int(vals[1]) - 1 if len(vals) > 1 else None
                    face.append((vertex_index, normal_index))
                faces.append(face)

    return vertices, normals, faces

def draw_obj(vertices, normals, faces):
    for face in faces:
        if len(face) == 3:
            glBegin(GL_TRIANGLES)
        else:
            glBegin(GL_POLYGON)
        
        for vertex, normal in face:
            if normal is not None:
                glNormal3fv(normals[normal])
            glVertex3fv(vertices[vertex])
        
        glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Posicionando a câmera
    glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

    # Rotacionar o objeto para melhor visualização
    glRotatef(25, 1, 0, 0)
    glRotatef(25, 0, 1, 0)

    draw_obj(vertices, normals, faces)

    glutSwapBuffers()

def init_gl():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LEQUAL)

if __name__ == "__main__":
    # Carregando o arquivo OBJ
    filename = "Ball.obj"
    vertices, normals, faces = load_obj(filename)

    # Inicializando a janela OpenGL
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OBJ Viewer")
    glutDisplayFunc(display)

    init_gl()

    glutMainLoop()

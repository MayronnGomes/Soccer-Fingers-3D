from OpenGL.GL import *
from OpenGL.GLUT import *
import glm

def load_obj(filename):
    vertices = []
    faces = []
    face_materials = []
    current_material = None

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Linha de vértice
                parts = line.split()
                vertex = list(map(float, parts[1:4]))
                vertices.append(vertex)
            elif line.startswith('usemtl'):  # Linha de material
                current_material = line.split()[1]
            elif line.startswith('f '):  # Linha de face
                parts = line.split()
                face = []
                for part in parts[1:]:
                    vertex_index = int(part.split('//')[0]) - 1
                    face.append(vertex_index)
                faces.append(face)
                face_materials.append(current_material)

    return vertices, faces, face_materials

def draw_obj(vertices, faces, face_materials):
    # Definir cores com base no material
    color_map = {
        'Bianco': (1.0, 1.0, 1.0),  # Branco
        'Nero.001': (0.0, 0.0, 0.0)    # Preto
    }

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

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Posicionando a câmera
    glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

    # Rotacionar o objeto para melhor visualização
    glRotatef(25, 1, 0, 0)
    glRotatef(25, 0, 1, 0)

    draw_obj(vertices, faces, face_materials)

    glutSwapBuffers()

def init_gl():
    glDisable(GL_LIGHTING)  # Desabilita iluminação
    glDisable(GL_COLOR_MATERIAL)  # Desabilita materiais
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LEQUAL)

if __name__ == "__main__":
    # Carregando o arquivo OBJ
    filename = "Ball.obj"
    vertices, faces, face_materials = load_obj(filename)

    # Inicializando a janela OpenGL
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OBJ Viewer")
    glutDisplayFunc(display)

    init_gl()

    glutMainLoop()

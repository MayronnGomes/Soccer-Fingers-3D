from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Variáveis globais para o GIF e as texturas
gif = None
textures = []
current_frame = 0

def load_gif(filename):
    global gif, textures

    # Carregar o GIF usando Pillow
    gif = Image.open(filename)
    
    # Criar texturas para cada frame do GIF
    for frame in range(gif.n_frames):
        gif.seek(frame)
        image_data = gif.convert("RGBA").tobytes()  # Converter para formato RGBA
        width, height = gif.size

        # Gerar uma textura OpenGL
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Adicionar a textura à lista
        textures.append(texture)

def init():
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 1.0)

def display():
    global current_frame

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Selecionar a textura do frame atual
    glBindTexture(GL_TEXTURE_2D, textures[current_frame])

    # Desenhar um quadrado texturizado
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(-1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(-1.0, 1.0)
    glEnd()

    glutSwapBuffers()

    # Atualizar o frame atual para animação
    current_frame = (current_frame + 1) % len(textures)

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(100, timer, 0)  # Controlar a velocidade de atualização dos frames

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"GIF Animation with OpenGL")

    init()
    load_gif("exemplo.gif")  # Substitua pelo seu arquivo GIF

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(100, timer, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()

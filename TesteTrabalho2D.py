import numpy as np
import glm
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

# Variáveis Globais
FPS = 30
campoLar = 30
campoAlt = 15
bolaRaio = 1
mundoLar  = 10
mundoAlt  = 10
janelaLar = 960
janelaAlt = 540
pos = glm.vec3(0, 0, 0)
dir = glm.vec3(0, bolaRaio, 0)
lat = glm.vec3(bolaRaio, 0, 0)
M = glm.mat4(1)
texCampo   = 0
texBola    = 0
texProgBar = 0
texGol = 0
progressbar = False
mov = False
angleProgressbar = 0.0
forca = glm.vec3(0.0, 0.0, 0.0)
deslocamento = glm.vec3(0.0, 0.0, 0.0)
velocidade = 0.05
TIME = {
    "belgica": 0,
    "brasil": 0,
    "inglaterra": 0,
    "italia": 0
}

FORMATION = {
    "1-2-2":   [glm.vec3(3, campoAlt/2, 0), glm.vec3(campoLar/4, campoAlt/2 - 5, 0), glm.vec3(campoLar/4, campoAlt/2 + 5, 0), glm.vec3(campoLar/2 - 3, campoAlt/2 - 2, 0), glm.vec3(campoLar/2 - 3, campoAlt/2 + 2, 0)],
    "1-2-1-1": [glm.vec3(3, campoAlt/2, 0), glm.vec3(campoLar/4 - 1, campoAlt/2 - 4, 0), glm.vec3(campoLar/4 - 1, campoAlt/2 + 4, 0), glm.vec3(campoLar/2 - 3, campoAlt/2, 0), glm.vec3(campoLar/2 - 6, campoAlt/2, 0)]
}

def calcForca():
    global forca, deslocamento

    # fazer Barra de força multiplicadores 1, 1.25, 1.5, 1.75, 2

    forca *= (-1)

    deslocamento = forca * velocidade


def calcMatrix():
    global pos, dir, lat, M
    M[0] = glm.vec4(lat,0)   # 1ª coluna é igual ao vetor i (vetor que aponta pra lateral direita do carro)
    M[1] = glm.vec4(dir,0)   # 2ª coluna é igual ao vetor j (vetor que aponta pra frente do carro)
    M[2] = glm.vec4(0,0,1,0) # 3ª coluna é igual ao vetor k (vetor que aponta para o topo do carro (direção do eixo z))
    M[3] = glm.vec4(pos,1)   # 4ª coluna é igual ao ponto O (posição do carro)

def carregaTextura(filename):
    # carregamento da textura feita pelo módulo PIL
    img = Image.open(filename)                  # abrindo o arquivo da textura
    img = img.transpose(Image.FLIP_TOP_BOTTOM)  # espelhando verticalmente a textura (normalmente, a coordenada y das imagens cresce de cima para baixo)
    imgData = img.convert("RGBA").tobytes()     # convertendo a imagem carregada em bytes que serão lidos pelo OpenGL

    # criando o objeto textura dentro da máquina OpenGL
    texId = glGenTextures(1)                                                                                # criando um objeto textura
    glBindTexture(GL_TEXTURE_2D, texId)                                                                     # tornando o objeto textura recém criado ativo
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)                                        # suavização quando um texel ocupa vários pixels
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)                                        # suavização quanto vários texels ocupam um único pixel
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)                                              # definindo que a cor da textura substituirá a cor do polígono
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,  img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)  # enviando os dados lidos pelo módulo PIL para a OpenGL
    glBindTexture(GL_TEXTURE_2D, 0)                                                                         # tornando o objeto textura inativo por enquanto

    #retornando o identificador da textura recém-criada
    return texId

class Circle:

    def __init__(self, raio):
        self.raio = raio

    def desenha(self, fill=False):

        if (fill):
            glBegin(GL_POLYGON)
        else:
            print('teste')
            glBegin(GL_LINE_LOOP)

        for i in range(36):
            theta = 2.0 * math.pi * i / 36
            x = self.raio * math.cos(theta)
            y = self.raio * math.sin(theta)
            glVertex2f(x, y)
        glEnd()

class Cube:

    def __init__(self) -> None:
        pass

    def desenha(self, fill=False):

        if (fill):
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        else:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(0, 0)
        glTexCoord2f(0, 1); glVertex2f(0, 1)
        glTexCoord2f(1, 1); glVertex2f(1, 1)
        glTexCoord2f(1, 0); glVertex2f(1, 0)
        glEnd()

class Triangle:

    def __init__(self) -> None:
        pass

    def desenha(self, fill=False):

        if (fill):
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        else:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

        glBegin(GL_TRIANGLES)
        glVertex2f(0, 0)
        glVertex2f(1, 0)
        glVertex2f(0, 1)
        glEnd()

class Campo:
    
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    def desenha(self):
        gramado = Cube()

        glPushMatrix()
        glScalef(self.largura, self.altura, 1)
        glBindTexture(GL_TEXTURE_2D, texCampo)
        gramado.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

    def desenha_gol(self):
        gol = Cube()

        glPushMatrix()
        glTranslatef(-3, self.altura/2 - 2.5, 0)
        glScalef(3, 5, 1)
        glBindTexture(GL_TEXTURE_2D, texGol)
        gol.desenha(True)
        glTranslatef(12, 0, 0)
        glScalef(-1, 1, 1)
        gol.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

    def verifica_colisao(self):
        # Colisão com as linha horizontais
        if (abs(pos.y) + bolaRaio/2 > campoAlt/2) and (abs(pos.x) + bolaRaio/2 > campoLar/2):
            return glm.vec3(0, 0, 0), True
        elif abs(pos.y) + bolaRaio/2 > campoAlt/2:
            return glm.vec3(0, 1, 0), True
        elif abs(pos.x) + bolaRaio/2 > campoLar/2:
            return glm.vec3(1, 0, 0), True
        else:
            return glm.vec3(0, 0, 0), False
        
class Jogador:

    def __init__(self, raio, time, posicao):
        self.raio = raio
        self.time = time
        self.posicao = posicao

    def desenha(self):
        jogador = Cube()
        glBindTexture(GL_TEXTURE_2D, self.time)
        glPushMatrix()
        glTranslatef(self.posicao.x - self.raio/2, self.posicao.y - self.raio/2, self.posicao.z)
        glScalef(self.raio, self.raio, 1)
        jogador.desenha(True)
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)     

    def verifica_colisao(self):
        # Colisão com as linha horizontais
        if (abs(pos.y) + bolaRaio/2 > campoAlt/2) and (abs(pos.x) + bolaRaio/2 > campoLar/2):
            return glm.vec3(0, 0, 0), True
        elif abs(pos.y) + bolaRaio/2 > campoAlt/2:
            return glm.vec3(0, 1, 0), True
        elif abs(pos.x) + bolaRaio/2 > campoLar/2:
            return glm.vec3(1, 0, 0), True
        else:
            return glm.vec3(0, 0, 0), False

class Time:

    def __init__(self, escudo, formacao, visitante):
        self.escudo = escudo
        self.formacao = formacao
        self.jogadores = [Jogador(2, self.escudo, self.formacao[i]) for i in range(5)]
        self.visitante = visitante

    def desenha(self):
        for i in self.jogadores:
            glPushMatrix()
            if self.visitante:
                glTranslatef(campoLar, 0, 0)
                glScalef(-1, 1, 1)
            i.desenha()
            glPopMatrix()

class Bola:

    def __init__(self, raio):
        self.raio = raio

    def desenha(self):
        bola = Cube()
        
        glBindTexture(GL_TEXTURE_2D, texBola)
        bola.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)

    def desenha_progressbar(self):
        bar = Cube()

        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glRotatef(angleProgressbar + 90, 0, 0, 1)
        glTranslatef(-1/4, -3/2, 0)
        glScalef(1/2, 3, 1)
        glBindTexture(GL_TEXTURE_2D, texProgBar)
        bar.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

    def move(self):
        global pos, forca

        pos.x = pos.x + velocidade * forca.x
        pos.y = pos.y + velocidade * forca.y

        forca.x -= deslocamento.x # decrementando a forca
        forca.y -= deslocamento.y # decrementando a forca

        calcMatrix()

# Objetos
campo = Campo(campoLar, campoAlt)
bola = Bola(bolaRaio)

class Game:

    def __init__(self):
        
        glutInit()
        glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(janelaLar, janelaAlt)
        glutInitWindowPosition(0,0)
        glutCreateWindow('FullScreen')
        self.inicio()
        glutTimerFunc(int(1000/FPS), self.timer, 0)      
        # glutFullScreen()
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.desenha)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutMainLoop()

    def inicio(self):
        global texCampo, texBola, texProgBar, texGol
        glClearColor(0, 0.3, 0, 1)
        glLineWidth(5)
        glEnable(GL_MULTISAMPLE)                    
        glEnable(GL_TEXTURE_2D)                      
        glEnable(GL_BLEND);                         
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        texCampo = carregaTextura('Texturas/campo.jpg')
        texBola = carregaTextura('Texturas/bola.png')
        texProgBar = carregaTextura('Texturas/arrow.png')
        texGol = carregaTextura('Texturas/gol.jpg')
        for i in TIME:
            TIME[i] = carregaTextura(f'TIMES PNG/{i}.png')
        calcMatrix()

    def desenha(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-mundoLar, mundoLar, -mundoAlt + 2, mundoAlt + 2, -1, 1)

        glPushMatrix()
        glTranslatef(-(campo.largura/2), -(campo.altura/2), 0)
        campo.desenha()
        campo.desenha_gol()

        glPushMatrix()
        glTranslatef((campo.largura - bola.raio)/2, (campo.altura - bola.raio)/2, 0)
        glMultMatrixf(np.asarray(glm.transpose(M)))
        bola.desenha()
        glPopMatrix()

        timeA = Time(TIME['inglaterra'], FORMATION['1-2-2'], False)
        timeA.desenha()

        timeB = Time(TIME['italia'], FORMATION['1-2-1-1'], True)
        timeB.desenha()

        glPopMatrix()

        if(progressbar):
            bola.desenha_progressbar()

        glutSwapBuffers()

    def reshape(self, w, h):
        global mundoLar, janelaAlt, janelaLar
        janelaLar = w
        janelaAlt = h
        mundoLar  = mundoAlt*w/h
        glViewport(0,0,w,h) 

    def timer(self, v):
        global mov, forca, pos, angleProgressbar, deslocamento
        glutTimerFunc(int(1000/FPS), self.timer, 0)

        if mov:
            normal, col_campo = campo.verifica_colisao()
            normal, col_jogador = False
            if col_campo:
                if normal == glm.vec3(0, 0, 0):
                    # print(f'forca ant: {forca}')
                    forca *= (-1)
                    # print(f'forca dps: {forca}')
                    deslocamento *= (-1)
                    # print('canto\n\n\n\n\n\n')
                else:
                    # print(normal)
                    # print(f'forca ant: {forca}')
                    forca = glm.reflect(forca, normal)
                    # print(f'forca dps: {forca}')
                    deslocamento = glm.reflect(deslocamento, normal)
            elif col_jogador:
                pass

            bola.move()

            if not(abs(forca.x) >= abs(deslocamento.x) or abs(forca.y) >= abs(deslocamento.y)):
                print('Movimento parou')
                mov = False
                forca.x = forca.y = forca.z = 0
                deslocamento.x = deslocamento.y = deslocamento.z = 0
                angleProgressbar = 0.0

        glutPostRedisplay()

    def mouse(self, button, state, x, y):
        global progressbar, forca, mov, angleProgressbar

        model_view = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)

        win_x = float(x)
        win_y = float(viewport[3] - y)
        win_z = 0.0

        normalized_x, normalized_y, _ = gluUnProject(win_x, win_y, win_z, model_view, projection, viewport)
        normalized_x = round(normalized_x, 3)
        normalized_y = round(normalized_y, 3)

        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            if (pos[0] - bolaRaio) <= normalized_x <= (pos[0] + bolaRaio) and (pos[1] - bolaRaio) <= normalized_y <= (pos[1] + bolaRaio) and not mov:
                progressbar = True
                forca.x = normalized_x - pos.x
                forca.y = normalized_y - pos.y
                angleProgressbar = math.degrees(math.atan2(forca.y, forca.x))

        elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            progressbar = False
            if (abs(forca.x) > 0 or abs(forca.y) > 0 or abs(forca.z) > 0) and not mov:
                mov = True
                calcForca()
    
    def motion(self, x, y):
        global forca, angleProgressbar

        if progressbar:
            
            model_view = glGetDoublev(GL_MODELVIEW_MATRIX)
            projection = glGetDoublev(GL_PROJECTION_MATRIX)
            viewport = glGetIntegerv(GL_VIEWPORT)

            win_x = float(x)
            win_y = float(viewport[3] - y)  # Inverte a coordenada Y da janela
            win_z = 0.0  # Para 2D, a profundidade é geralmente 0

            normalized_x, normalized_y, _ = gluUnProject(win_x, win_y, win_z, model_view, projection, viewport)
            normalized_x = round(normalized_x, 3)
            normalized_y = round(normalized_y, 3)
            forca.x = normalized_x - pos.x
            forca.y = normalized_y - pos.y
            angleProgressbar = math.degrees(math.atan2(forca.y, forca.x))

if __name__ == "__main__":
    game = Game()

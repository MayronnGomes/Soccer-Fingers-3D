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
velocidade = glm.vec3(0.0, 0.0, 0.0)

TIME = {
    "belgica": 0,
    "brasil": 0,
    "inglaterra": 0,
    "italia": 0
}

FORMATION = {
    "1-2-2":   [glm.vec3(-campoLar/2 + 3, 0, 0), glm.vec3(-campoLar/4, -5, 0), glm.vec3(-campoLar/4, 5, 0), glm.vec3(-3, -2, 0), glm.vec3(-3, 2, 0)],
    "1-2-1-1": [glm.vec3(-campoLar/2 + 3, 0, 0), glm.vec3(-campoLar/4 - 1, -4, 0), glm.vec3(-campoLar/4 - 1, 4, 0), glm.vec3(-3, 0, 0), glm.vec3(-7, 0, 0)]
}

def recalcMov(normal):
    global deslocamento, forca, velocidade

    forca = glm.reflect(forca, normal)
    deslocamento = glm.reflect(deslocamento, normal)
    velocidade = glm.reflect(velocidade, normal)

    # fazer Barra de força multiplicadores 1, 1.25, 1.5, 1.75, 2

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
        glTranslatef(-2, self.altura/2 - 2.7, 0)
        glScalef(2, 6, 1)
        glBindTexture(GL_TEXTURE_2D, texGol)
        gol.desenha(True)
        glTranslatef(17, 0, 0)
        glScalef(-1, 1, 1)
        gol.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

    def verifica_colisao(self, bola):
        if (bola.pos.y + bolaRaio/2 >= campoAlt/2) and (velocidade.y > 0):        # A POSITIVO
            print(f'a+ {bola.pos} {velocidade}')
            return glm.vec3(0, 1, 0), True
        elif (bola.pos.y - bolaRaio/2 <= -campoAlt/2) and (velocidade.y < 0):     # A NEGATIVO
            print(f'a- {bola.pos} {velocidade}')
            return glm.vec3(0, 1, 0), True
        elif (bola.pos.x + bolaRaio/2 >= campoLar/2 + 2) and (velocidade.x > 0):  # B POSITIVO
            print(f'b+ {bola.pos} {velocidade}')
            return glm.vec3(1, 0, 0), True
        elif (bola.pos.x - bolaRaio/2 <= -campoLar/2 - 2) and (velocidade.x < 0): # B NEGATIVO
            print(f'b- {bola.pos} {velocidade}')
            return glm.vec3(1, 0, 0), True
        elif (bola.pos.x + bolaRaio/2 > campoLar/2) and (bola.pos.y + bolaRaio/2 >= 2.4) and (bola.pos.y + bolaRaio/2 - velocidade.y < 2.4) and (velocidade.y > 0):     # E POSITIVO
            print(f'e+ {bola.pos} {velocidade}')
            return glm.vec3(0, 1, 0), True
        elif (bola.pos.x - bolaRaio/2 < -campoLar/2) and (bola.pos.y + bolaRaio/2 >= 2.4) and (bola.pos.y + bolaRaio/2 - velocidade.y < 2.4) and (velocidade.y > 0):    # E NEGATIVO
            print(f'e- {bola.pos} {velocidade}')
            return glm.vec3(0, 1, 0), True
        elif (bola.pos.x + bolaRaio/2 >= campoLar/2) and (bola.pos.y + bolaRaio/2 >= 2.4) and (velocidade.x > 0):    # C POSITIVO
            print(f'c+ {bola.pos} {velocidade}')
            return glm.vec3(1, 0, 0), True
        elif (bola.pos.x - bolaRaio/2 <= -campoLar/2) and (bola.pos.y + bolaRaio/2 >= 2.4) and (velocidade.x < 0):   # C NEGATIVO
            print(f'c- {bola.pos} {velocidade}')
            return glm.vec3(1, 0, 0), True
        elif (bola.pos.x + bolaRaio/2 > campoLar/2) and (bola.pos.y - bolaRaio/2 <= -2.4) and (bola.pos.y - bolaRaio/2 - velocidade.y > -2.4) and (velocidade.y < 0):    # F POSITIVO
            print(f'f+ {bola.pos} {velocidade}')
            return glm.vec3(0, 1, 0), True
        elif (bola.pos.x - bolaRaio/2 < -campoLar/2) and (bola.pos.y - bolaRaio/2 <= -2.4) and (bola.pos.y - bolaRaio/2 - velocidade.y > -2.4) and (velocidade.y < 0):   # F NEGATIVO
            print(f'f- {bola.pos} {velocidade}')
            return glm.vec3(0, 1, 0), True
        elif (bola.pos.x + bolaRaio/2 >= campoLar/2) and (bola.pos.y - bolaRaio/2 <= -2.4) and (velocidade.x > 0):   # D POSITIVO
            print(f'd+ {bola.pos} {velocidade}')
            return glm.vec3(1, 0, 0), True
        elif (bola.pos.x - bolaRaio/2 <= -campoLar/2) and (bola.pos.y - bolaRaio/2 <= -2.4) and (velocidade.x < 0):  # D NEGATIVO
            print(f'd- {bola.pos} {velocidade}')
            return glm.vec3(1, 0, 0), True
        else:
            return glm.vec3(0, 0, 0), False
        
    def colisao_gol(self, bola): # ERRO
        global mov
        if (abs(bola.pos.x) + bolaRaio/2 >= campoLar/2):
            # if (2.4 > bola.pos.y + bolaRaio/2) and (bola.pos.y - bolaRaio/2 > -2.4):
            if abs(bola.pos.x) - bolaRaio/2 > campoLar/2:
                print('gol')
                # stop move
                # mov = False
                return True
            else:
                return False
            """if (2.4 <= bola.pos.y + bolaRaio/2) or (-2.4 >= bola.pos.y - bolaRaio/2): #CORRETO
                recalcMov(glm.vec3(0, 1, 0))
                return True"""
        else: 
            return False  

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

    def verifica_colisao(self, bola):
        if bolaRaio/2 + self.raio/2 > glm.distance(self.posicao, bola.pos):
            C = self.posicao - bola.pos
            normal = glm.normalize(C)
            return normal, True
        return glm.vec3(0, 0, 0), False

class Time:

    def __init__(self, escudo, formacao, visitante):
        self.escudo = escudo
        self.formacao = formacao
        self.visitante = visitante
        self.jogadores = [Jogador(2, self.escudo, (self.formacao[i]*(-1) if self.visitante else self.formacao[i])) for i in range(5)]

    def desenha(self):
        for i in self.jogadores:
            glPushMatrix()
            i.desenha()
            glPopMatrix()

class Bola:

    def __init__(self, raio):
        self.raio = raio
        self.pos = glm.vec3(0, 0, 0)

    def desenha(self):
        bola = Cube()
        
        glBindTexture(GL_TEXTURE_2D, texBola)
        bola.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)

    def desenha_progressbar(self):
        bar = Cube()

        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, self.pos.z)
        glRotatef(angleProgressbar + 90, 0, 0, 1)
        glTranslatef(-1/4, -3/2, 0)
        glScalef(1/2, 3, 1)
        glBindTexture(GL_TEXTURE_2D, texProgBar)
        bar.desenha(True)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

    def move(self):
        global deslocamento

        self.pos.x += velocidade.x
        self.pos.y += velocidade.y

        deslocamento.x += velocidade.x # incrementando o deslocamento
        deslocamento.y += velocidade.y # incrementando o deslocamento

class Placar:

    def __init__(self, time1, time2):
        self.time1 = time1
        self.time2 = time2
        self.score1 = 0
        self.score2 = 0
        self.timeSec = 30

    def desenha(self):
        cubo = Cube()

        glPushMatrix()
        glTranslatef(0,3,0)
        glScalef(1,1/1.5,1)
        
        glPushMatrix() #desenha o fundo cinza
        glColor3f(0.188, 0.184, 0.176) # vermelho, verde, azul
        glTranslatef(-15, 8.3, 0)
        glScalef(30,4.2,1)
        cubo.desenha(True)
        glPopMatrix()
        

        glPushMatrix() #desenha lado brando dir
        glColor3f(0.933,0.933,0.933) # vermelho, verde, azul
        glTranslatef(0, 10.3, 0)
        glScalef(15,2.2,1)
        cubo.desenha(True)
        glPopMatrix()
        
        glPushMatrix() #desenha lado brando esq
        glColor3f(0.933,0.933,0.933) # vermelho, verde, azul
        glTranslatef(0, 10.3, 0)
        glScalef(-15,2.2,1)
        cubo.desenha(True)
        glPopMatrix()

        glPushMatrix() #desenha lado cinza dir
        glColor3f(0.753,0.753,0.753) # vermelho, verde, azul
        glTranslatef(0,9.7,0)
        glScalef(5,2.8, 1)
        cubo.desenha(True)
        glPopMatrix()

        glPushMatrix() #desenha lado cinza dir
        glColor3f(0.753,0.753,0.753) # vermelho, verde, azul
        glTranslatef(0,9.7,0)
        glScalef(-5,2.8, 1)
        cubo.desenha(True)
        glPopMatrix()

        glPushMatrix() # desenha o quadrado do meio
        glColor3f(0.290, 0.290, 0.282) # vermelho, verde, azul
        glTranslatef(-1.5,8.8,0)
        glScalef(3, 3.7, 1)
        cubo.desenha(True)
        glPopMatrix()

        glPopMatrix()
        
        glPushMatrix() # 
        jogador1 = Jogador(1.5, self.time1, glm.vec3(-14, 10.6, 0))
        jogador2 = Jogador(1.5, self.time2, glm.vec3(14, 10.6, 0))

        jogador1.desenha()
        jogador2.desenha()
        glPopMatrix()

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
        texGol = carregaTextura('Texturas/trave.png') 
        for i in TIME:
            TIME[i] = carregaTextura(f'TIMES PNG/{i}.png')
        self.campo = Campo(campoLar, campoAlt)
        self.bola = Bola(bolaRaio)
        self.timeA = Time(TIME['belgica'], FORMATION['1-2-1-1'], False)
        self.timeB = Time(TIME['brasil'], FORMATION['1-2-2'], True)
        self.placar = Placar(self.timeA.escudo, self.timeB.escudo)

    def desenha(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-mundoLar, mundoLar, -mundoAlt + 2, mundoAlt + 2, -1, 1)

        glPushMatrix()
        glTranslatef(-(self.campo.largura/2), -(self.campo.altura/2), 0)
        self.campo.desenha()
        self.campo.desenha_gol()

        glPushMatrix()
        glTranslatef(self.campo.largura/2, self.campo.altura/2, 0)
        
        glPushMatrix()
        glTranslatef(-self.bola.raio/2, -self.bola.raio/2, 0)
        glTranslatef(self.bola.pos.x, self.bola.pos.y, self.bola.pos.z)
        glScalef(self.bola.raio, self.bola.raio, 1)
        self.bola.desenha()
        glPopMatrix()

        self.timeA.desenha()
        self.timeB.desenha()

        glPopMatrix()
        glPopMatrix()

        if(progressbar):
            self.bola.desenha_progressbar()

        self.placar.desenha()

        glutSwapBuffers()

    def reshape(self, w, h):
        global mundoLar, janelaAlt, janelaLar
        janelaLar = w
        janelaAlt = h
        mundoLar  = mundoAlt*w/h
        glViewport(0,0,w,h) 

    def timer(self, v):
        global mov, forca, angleProgressbar, deslocamento
        glutTimerFunc(int(1000/FPS), self.timer, 0)

        if mov:

            # movimento da bola parou
            if (abs(deslocamento.x + velocidade.x) > abs(forca.x) or abs(deslocamento.y + velocidade.y) > abs(forca.y)):
                
                print('Movimento parou')
                # troca jogador
                mov = False
                forca.x = forca.y = forca.z = 0
                deslocamento.x = deslocamento.y = deslocamento.z = 0
                angleProgressbar = 0.0

            # tratamento de colisão e movimento da bola
            else:

                normal, colisao_campo = self.campo.verifica_colisao(self.bola)
                colisao_jogador = False
                if colisao_campo: # colisão no campo
                    recalcMov(normal)
                # elif self.campo.colisao_gol(self.bola):
                #     # print('colisão gol')
                #     pass
                '''elif (self.bola.pos.x < 0): # colisão time A
                    for i in self.timeA.jogadores:
                        normal, colisao_jogador = i.verifica_colisao(self.bola)

                        if colisao_jogador:
                            forca
                            recalcMov(normal)
                            break
                elif (self.bola.pos.x > 0): # colisão time B
                    for i in self.timeB.jogadores:
                        normal, colisao_jogador = i.verifica_colisao(self.bola)

                        if colisao_jogador:
                            recalcMov(normal)
                            break'''

                self.bola.move()

        glutPostRedisplay()

    def mouse(self, button, state, x, y):
        global progressbar, forca, mov, angleProgressbar, velocidade

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
            if (self.bola.pos.x - bolaRaio) <= normalized_x <= (self.bola.pos.x + bolaRaio) and (self.bola.pos.y - bolaRaio) <= normalized_y <= (self.bola.pos.y + bolaRaio) and not mov:
                progressbar = True
                forca.x = normalized_x - self.bola.pos.x
                forca.y = normalized_y - self.bola.pos.y
                angleProgressbar = math.degrees(math.atan2(forca.y, forca.x))

        elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            progressbar = False
            if (abs(forca.x) > 0 or abs(forca.y) > 0 or abs(forca.z) > 0) and not mov:
                mov = True
                forca *= -1
                velocidade = forca * 0.05
    
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
            forca.x = normalized_x - self.bola.pos.x
            forca.y = normalized_y - self.bola.pos.y
            angleProgressbar = math.degrees(math.atan2(forca.y, forca.x))

if __name__ == "__main__":
    game = Game()

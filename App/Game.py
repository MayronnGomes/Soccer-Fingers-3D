import pygame
import CONSTS
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Time import *
from Formation import *
from Bola import *
from Campo import *
from Triangule import *
from Placar import *
from Util import *

class Game:

    def __init__(self):

        glutInit()
        glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(CONSTS.janelaLar, CONSTS.janelaAlt)
        glutInitWindowPosition(0,0)
        glutCreateWindow('FullScreen')
        self.inicio()
        glutTimerFunc(int(1000/CONSTS.FPS), self.timer, 0)      
        glutFullScreen()
        glutKeyboardFunc(self.tecladoASCII)
        glutSpecialFunc(self.tecladoEspecial)
        glutSpecialUpFunc(self.tecladoEspecialUp)
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.desenha)
        glutMainLoop()

    def inicio(self):
        glClearColor(0, 0.3, 0, 1)
        glClearDepth(1.0)
        glLineWidth(5)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)                    
        glEnable(GL_TEXTURE_2D)                      
        glEnable(GL_BLEND);       
        glDepthFunc(GL_LEQUAL)                  
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        pygame.mixer.init()
        CONSTS.somChute = pygame.mixer.Sound('../Sons/chute.wav')
        CONSTS.somChute.set_volume(1)
        CONSTS.somVoltar = pygame.mixer.Sound('../Sons/voltar.mp3')
        CONSTS.somVoltar.set_volume(1)
        CONSTS.somSelecionar = pygame.mixer.Sound('../Sons/selecionar.mp3')
        CONSTS.somSelecionar.set_volume(1)
        CONSTS.somOpcao = pygame.mixer.Sound('../Sons/opcao.mp3')
        CONSTS.somOpcao.set_volume(1)
        CONSTS.texCampo = carregaTextura('../Texturas/campo.jpg')
        CONSTS.texLogo = carregaTextura('../Texturas/logo.png')

        for i in range(1, 6):
            CONSTS.texBar.append(carregaTextura(f'../Texturas/Barra/{i}.png'))

        for i in CONSTS.TIME:
            CONSTS.TIME[i] = carregaTextura(f'../Texturas/TIMES PNG/{i}.png')
            CONSTS.SIGLAS[i] = carregaTextura(f'../Texturas/Siglas/{i}.png')

        for i in range(0, 6):
            CONSTS.PLACAR[f'{i}'] = carregaTextura(f'../Texturas/Placar/{i}.png')
        
        for i in CONSTS.TELAS.keys():
            if i != "vencedor1" and i != "vencedor2" and i != "gol":
                CONSTS.TELAS[i] = carregaTextura(f'../Texturas/Telas/{i}.png') 
            else:
                load_gif(i)

        self.campo = Campo(CONSTS.campoLar, CONSTS.campoAlt)
        self.bola = Bola(CONSTS.bolaDiametro)
        self.formation = Formation()
        self.nomeA = ''
        self.nomeB = ''
        self.timeA = None
        self.timeB = None
        self.placar = None
        self.option = 0
        self.optionTimeA = 0
        self.optionTimeB = 0
        self.tela = "inicial"

    def desenha(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        if self.tela == "jogo":
            glFrustum(-1, 1, -1, 1, 2, 100)

            glMatrixMode(GL_MODELVIEW)
            CONSTS.cameraPosition = self.bola.pos + computeSphereCoord(CONSTS.camLong, CONSTS.camLat, 10)
            matrizCamera = glm.lookAt(CONSTS.cameraPosition, self.bola.pos, glm.vec3(0, 0, 1))
            glLoadMatrixf(mat2list(matrizCamera))

            glPushMatrix()
            glTranslatef(-(self.campo.largura/2), -(self.campo.altura/2), 0)
            self.campo.desenha()
            # gol esquerdo
            self.campo.desenha_gol()

            # gol direito
            glPushMatrix()
            glTranslatef(CONSTS.campoLar, 0, 0)
            glScalef(-1, 1, 1)
            self.campo.desenha_gol()
            glPopMatrix()

            glPushMatrix()
            glTranslatef(self.campo.largura/2, self.campo.altura/2, 0)
            
            glPushMatrix()
            glTranslatef(self.bola.pos.x, self.bola.pos.y, self.bola.raio/2)
            glRotatef(CONSTS.ang_rot, CONSTS.vetor_rot.y, CONSTS.vetor_rot.x, CONSTS.vetor_rot.z)
            glScalef(self.bola.raio/2, self.bola.raio/2, self.bola.raio/2)
            self.bola.desenha()
            glPopMatrix()

            self.timeA.desenha()
            self.timeB.desenha()

            glPopMatrix()
            glPopMatrix()

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(-CONSTS.mundoLar, CONSTS.mundoLar, -CONSTS.mundoAlt, CONSTS.mundoAlt, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glDisable(GL_DEPTH_TEST)

            glPushMatrix()
            self.placar.desenha()
            glPopMatrix()

            glPushMatrix()
            cube = Cube()
            glTranslatef(-CONSTS.mundoLar, -CONSTS.mundoAlt, 0)
            glScalef(6, 3, 1)
            glBindTexture(GL_TEXTURE_2D, CONSTS.texBar[CONSTS.currentBar])
            cube.desenha(True)
            glBindTexture(GL_TEXTURE_2D, 0)
            glPopMatrix()

            glEnable(GL_DEPTH_TEST)

        else:
            glOrtho(-CONSTS.mundoLar, CONSTS.mundoLar, -CONSTS.mundoAlt, CONSTS.mundoAlt, -1, 1)

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            if self.tela == "inicial":
                cube = Cube()
                triangule = Triangle()

                glPushMatrix()
                glTranslatef(-CONSTS.mundoLar, -CONSTS.mundoAlt, 0)
                glScalef(2 * CONSTS.mundoLar, 2 * CONSTS.mundoAlt, 1)
                glBindTexture(GL_TEXTURE_2D, CONSTS.TELAS[self.tela])
                cube.desenha(True)
                glBindTexture(GL_TEXTURE_2D, 0)
                glPopMatrix()

                glPushMatrix()
                glTranslatef(CONSTS.OPTIONS[self.option].x, CONSTS.OPTIONS[self.option].y, CONSTS.OPTIONS[self.option].z)
                glRotatef(135, 0, 0, 1)
                triangule.desenha(True)
                glPopMatrix()
                
            elif self.tela == "times":
                cube = Cube()
                triangule = Triangle()

                glPushMatrix() # tela
                glTranslatef(-CONSTS.mundoLar, -CONSTS.mundoAlt, 0)
                glScalef(2 * CONSTS.mundoLar, 2 * CONSTS.mundoAlt, 1)
                glBindTexture(GL_TEXTURE_2D, CONSTS.TELAS[self.tela])
                cube.desenha(True)
                glBindTexture(GL_TEXTURE_2D, 0)
                glPopMatrix()

                glPushMatrix() # Seleção
                if self.nomeA != "":
                    glScalef(-1, 1, 1)

                glTranslatef(-12.35, 0, 0)
                
                glPushMatrix()
                glTranslatef(CONSTS.OPTIONS[self.option].x, CONSTS.OPTIONS[self.option].y, CONSTS.OPTIONS[self.option].z)
                glRotatef(135, 0, 0, 1)
                triangule.desenha(True)
                glPopMatrix()
                
                glPushMatrix()
                glScale(-1, 1, 1)
                glTranslatef(CONSTS.OPTIONS[self.option].x, CONSTS.OPTIONS[self.option].y, CONSTS.OPTIONS[self.option].z)
                glRotatef(135, 0, 0, 1)
                triangule.desenha(True)
                glPopMatrix()
                glPopMatrix()

                glPushMatrix() # time esquerdo
                glTranslatef(-CONSTS.mundoLar * 0.72, -3, 0)
                glScalef(6, 6, 1)
                glBindTexture(GL_TEXTURE_2D, CONSTS.TIME[CONSTS.OPTIONSTIMES[self.optionTimeA]])
                cube.desenha(True)
                glBindTexture(GL_TEXTURE_2D, 0)
                glPopMatrix()
                
                glPushMatrix() # time direito
                glScalef(-1, 1, 1)
                glTranslatef(-CONSTS.mundoLar * 0.72, -3, 0)
                glScalef(6, 6, 1)
                glBindTexture(GL_TEXTURE_2D, CONSTS.TIME[CONSTS.OPTIONSTIMES[self.optionTimeB]])
                cube.desenha(True)
                glBindTexture(GL_TEXTURE_2D, 0)
                glPopMatrix()

                glPushMatrix() # nome time esquerdo
                glTranslatef(-CONSTS.mundoLar * 0.65, 5.35, 0)
                glScalef(3.2, 1.8, 1)
                glBindTexture(GL_TEXTURE_2D, CONSTS.SIGLAS[CONSTS.OPTIONSTIMES[self.optionTimeA]])
                cube.desenha(True)
                glBindTexture(GL_TEXTURE_2D, 0)
                glPopMatrix()
                
                glPushMatrix() # nome time direito
                glScalef(-1, 1, 1)
                glTranslatef(-CONSTS.mundoLar * 0.65, 5.35, 0)
                glScalef(3.2, 1.8, 1)
                glBindTexture(GL_TEXTURE_2D, CONSTS.SIGLAS[CONSTS.OPTIONSTIMES[self.optionTimeB]])
                cube.desenha(True, invertido=True)
                glBindTexture(GL_TEXTURE_2D, 0)
                glPopMatrix()

                # escolhendo - escolhido

            elif self.tela == "formação1" or self.tela == "formação2":
                self.formation.desenha(self.tela)

            elif self.tela == "vencedor1" or self.tela == "vencedor2" or self.tela == "gol":
                cube = Cube()

                glPushMatrix()
                glScalef(1, -1, 1)
                glTranslatef(-CONSTS.mundoLar, -CONSTS.mundoAlt, 0)
                glScalef(2 * CONSTS.mundoLar, 2 * CONSTS.mundoAlt, 1)
                glBindTexture(GL_TEXTURE_2D, CONSTS.TELAS[self.tela][CONSTS.frame])
                cube.desenha(True)
                glBindTexture(GL_TEXTURE_2D, 0)
                glPopMatrix()

        glutSwapBuffers()

        if self.tela == "vencedor1" or self.tela == "vencedor2" or self.tela == "gol":
            CONSTS.frame = (CONSTS.frame + 1) % len(CONSTS.TELAS[self.tela])

    def reshape(self, w, h):
        CONSTS.janelaLar = w
        CONSTS.janelaAlt = h
        CONSTS.mundoLar  = CONSTS.mundoAlt*w/h
        glViewport(0,0,w,h) 

    def timer(self, v):
        glutTimerFunc(int(1000/CONSTS.FPS), self.timer, 0)

        if CONSTS.mov:

            # movimento da bola parou
            if abs(CONSTS.deslocamento.x) > abs(CONSTS.forca.x) or abs(CONSTS.deslocamento.y) > abs(CONSTS.forca.y):
                
                if self.campo.colisao_gol(self.bola, self.placar):
                    self.gameover()
                    self.bola.pos = glm.vec3(0, 0, 0)
                    self.timeA.alterarFormacao()
                    self.timeB.alterarFormacao()

                    if self.placar.score1 == 5:
                        self.tela = "vencedor1"
                    elif self.placar.score2 == 5:
                        self.tela = "vencedor2"
                    else:
                        self.tela = "gol"
                
                # Movimento parou
                self.gameover()

            # tratamento de colisão e movimento da bola
            else:

                if self.campo.colisao_gol(self.bola, self.placar):
                    self.gameover()
                    self.bola.pos = glm.vec3(0, 0, 0)
                    self.timeA.alterarFormacao()
                    self.timeB.alterarFormacao()

                    if self.placar.score1 == 5:
                        self.tela = "vencedor1"
                    elif self.placar.score2 == 5:
                        self.tela = "vencedor2"
                    else:
                        self.tela = "gol"

                elif self.campo.verifica_colisao(self.bola): # colisão no campo
                    recalcMov(CONSTS.normal)
                elif self.bola.pos.x < 0 and self.timeA.colisao(self.bola): # colisão time A
                    recalcMov(CONSTS.normal)
                elif self.bola.pos.x > 0 and self.timeB.colisao(self.bola): # colisão time B
                    recalcMov(CONSTS.normal)

                self.bola.move()

        glutPostRedisplay()

    def tecladoASCII(self, key, x, y):
        if key == b'\r':
            if self.tela == "inicial":
                CONSTS.somSelecionar.play()
                if self.option == 0:
                    self.tela = "times"
                    self.option = 3
                    self.optionTimeA = 0
                    self.optionTimeB = 0
                elif self.option == 1:
                    print("options")
                elif self.option == 2:
                    glutLeaveMainLoop()
            elif self.tela == "times":
                CONSTS.somSelecionar.play()
                if self.nomeA == "":
                    self.nomeA = CONSTS.OPTIONSTIMES[self.optionTimeA]
                    self.timeA = Time(self.nomeA, CONSTS.FORMATION['1'], False)
                else:
                    self.nomeB = CONSTS.OPTIONSTIMES[self.optionTimeB]
                    self.timeB = Time(self.nomeB, CONSTS.FORMATION['1'], True)
                    self.placar = Placar(self.nomeA, self.nomeB)
                    self.tela = "jogo"
            elif self.tela == "formação1":
                CONSTS.somSelecionar.play()
                self.timeA.formacao = CONSTS.FORMATION[str(self.formation.option)]
                self.tela = "formação2"
            elif self.tela == "formação2":
                CONSTS.somSelecionar.play()
                self.timeB.formacao = CONSTS.FORMATION[str(self.formation.option)]
                self.tela = "jogo"
            elif self.tela == "jogo" and not CONSTS.mov:
                CONSTS.somChute.play()
                CONSTS.forca =  self.bola.pos - CONSTS.cameraPosition
                CONSTS.forca.x = round(CONSTS.forca.x, 3)
                CONSTS.forca.y = round(CONSTS.forca.y, 3)
                CONSTS.forca.z = 0
                forcaBar()
                CONSTS.vetor_rot = glm.normalize(CONSTS.forca)
                CONSTS.velocidade = glm.normalize(CONSTS.forca) * 0.3
                CONSTS.mov = True
            elif self.tela == "vencedor1" or self.tela == "vencedor2":
                CONSTS.somSelecionar.play()
                self.nomeA = ''
                self.nomeB = ''
                self.timeA = None
                self.timeB = None
                self.placar = None
                self.option = 3
                self.optionTimeA = 0
                self.optionTimeB = 0
                CONSTS.camLat = 25
                CONSTS.camLong = 180
                CONSTS.frame = 0
                CONSTS.currentBar = 0
                CONSTS.vetor_rot = glm.vec3(0)
                self.tela = "times"
            elif self.tela == "gol":
                CONSTS.camLat = 25
                CONSTS.camLong = 180
                CONSTS.frame = 0
                CONSTS.currentBar = 0
                CONSTS.vetor_rot = glm.vec3(0)
                self.tela = "jogo"
        elif key.lower() == b'f' and self.tela == "jogo":
            self.tela = "formação1"
            glutPostRedisplay()
        elif key.lower() == b'q':
            if self.tela == "formação1":
                CONSTS.somVoltar.play()
                self.tela = "formação2"
                glutPostRedisplay()
            elif self.tela == "formação2":
                CONSTS.somVoltar.play()
                self.tela = "jogo"
                glutPostRedisplay()
            elif self.tela == "times":
                CONSTS.somVoltar.play()
                if self.nomeA == "":
                    self.option = 0
                    self.tela = "inicial"
                else:
                    self.nomeA = ''
                    self.timeA = None
        elif key.lower() == b's' and self.tela == "jogo":
            CONSTS.camLat = glm.clamp(CONSTS.camLat - CONSTS.inc_ang, 7, 89)
        elif key.lower() == b'w' and self.tela == "jogo":
            CONSTS.camLat = glm.clamp(CONSTS.camLat + CONSTS.inc_ang, 7, 89)

    def tecladoEspecial(self, key, x, y):
        if self.tela == "inicial":
            if key == GLUT_KEY_DOWN:
                CONSTS.somOpcao.play()
                self.option += 1 if self.option < 2 else 0
            elif key == GLUT_KEY_UP:
                CONSTS.somOpcao.play()
                self.option -= 1 if self.option > 0 else 0
        elif self.tela == "times":
            if self.nomeA == "":
                if key == GLUT_KEY_RIGHT:
                    CONSTS.somOpcao.play()
                    self.optionTimeA += 1 if self.optionTimeA < (len(CONSTS.OPTIONSTIMES) - 1) else 0
                elif key == GLUT_KEY_LEFT:
                    CONSTS.somOpcao.play()
                    self.optionTimeA -= 1 if self.optionTimeA > 0 else 0
            else:
                if key == GLUT_KEY_RIGHT:
                    CONSTS.somOpcao.play()
                    self.optionTimeB += 1 if self.optionTimeB < (len(CONSTS.OPTIONSTIMES) - 1) else 0
                elif key == GLUT_KEY_LEFT:
                    CONSTS.somOpcao.play()
                    self.optionTimeB -= 1 if self.optionTimeB > 0 else 0
        elif self.tela == "formação1" or self.tela == "formação2":
            if key == GLUT_KEY_RIGHT:
                CONSTS.somOpcao.play()
                self.formation.option += 1 if self.formation.option < 8 else 0
            elif key == GLUT_KEY_LEFT:
                CONSTS.somOpcao.play()
                self.formation.option -= 1 if self.formation.option > 1 else 0
            elif key == GLUT_KEY_DOWN:
                CONSTS.somOpcao.play()
                self.formation.option += 4 if self.formation.option < 5 else 0
            elif key == GLUT_KEY_UP:
                CONSTS.somOpcao.play()
                self.formation.option -= 4 if self.formation.option > 4 else 0
        elif self.tela == "jogo":
            if key == GLUT_KEY_RIGHT:
                if (CONSTS.camLong - CONSTS.inc_ang) < 0:
                    CONSTS.camLong = 360
                elif (CONSTS.camLong - CONSTS.inc_ang) > 360:
                    CONSTS.camLong = 0
                else:
                    CONSTS.camLong -= CONSTS.inc_ang
            elif key == GLUT_KEY_LEFT:
                if (CONSTS.camLong + CONSTS.inc_ang) < 0:
                    CONSTS.camLong = 360
                elif (CONSTS.camLong + CONSTS.inc_ang) > 360:
                    CONSTS.camLong = 0
                else:
                    CONSTS.camLong += CONSTS.inc_ang
            elif key == GLUT_KEY_DOWN:
                CONSTS.currentBar = glm.clamp(CONSTS.currentBar - 1, 0, 4)
            elif key == GLUT_KEY_UP:
                CONSTS.currentBar = glm.clamp(CONSTS.currentBar + 1, 0, 4)
        
    def tecladoEspecialUp(self, key, x, y):
        if (key == GLUT_KEY_DOWN or key == GLUT_KEY_UP) and self.tela == "inicial":
            glutPostRedisplay()
        elif (key == GLUT_KEY_RIGHT or key == GLUT_KEY_LEFT) and self.tela == "times":
            glutPostRedisplay()
        elif (key == GLUT_KEY_RIGHT or key == GLUT_KEY_LEFT or key == GLUT_KEY_DOWN or key == GLUT_KEY_UP) and (self.tela == "formação1" or self.tela == "formação2"):
            glutPostRedisplay()

    def gameover(self):

        CONSTS.mov = False
        CONSTS.forca.x = CONSTS.forca.y = CONSTS.forca.z = 0
        CONSTS.deslocamento.x = CONSTS.deslocamento.y = CONSTS.deslocamento.z = 0
        CONSTS.velocidade.x = CONSTS.velocidade.y = CONSTS.velocidade.z = 0

if __name__ == "__main__":
    game = Game()

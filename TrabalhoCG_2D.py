from OpenGL.GL import *
from OpenGL.GLUT import *
import glm 

#variÃ¡veis globais
FPS = 30
camPos = glm.vec4(6,6,6,1);                                                 # posiÃ§Ã£o inicial da cÃ¢mera
camRotacao = glm.rotate(glm.mat4(1.0), glm.radians(1.0), glm.vec3(0,1,0))   # matriz de rotaÃ§Ã£o para girar a cÃ¢mera
gira = True                                                                 # variÃ¡vel que determina se a cÃ¢mera estÃ¡ ou nÃ£o girando
janelaLargura = 500                                                         # largura da janela em pixels
janelaAltura = 500                                                          # altura da janela em pixels
aspectRatio = 1                                                             # aspect ratio da janela (largura dividida pela altura)

#FunÃ§Ã£o contendo configuraÃ§Ãµes iniciais
def inicio():
    glClearColor(0.5,0.5,0.5,1)
    glLineWidth(1)           # altera a largura das linhas para 1 pixel
    glEnable(GL_DEPTH_TEST)  # habilitando a remoÃ§Ã£o de faces que estejam atrÃ¡s de outras (remoÃ§Ã£o de faces traseiras)
    glEnable(GL_MULTISAMPLE) # habilita um tipo de antialiasing (melhora serrilhado de linhas e bordas de polÃ­gonos)

#FunÃ§Ã£o que converte glm.mat4 em list<float>
def mat2list(M):
    matrix = []
    for i in range(0,4):
        matrix.append(list(M[i]))
    return matrix

#FunÃ§Ã£o chamada sempre que a janela sofre alteraÃ§Ã£o sem seu tamanho
def alteraJanela(largura, altura):
    global janelaLargura, janelaAltura, aspectRatio
    janelaLargura = largura
    janelaAltura = altura
    aspectRatio = largura/altura   # calculando o aspect ratio da janela
    glViewport(0,0,largura,altura) # reserva a Ã¡rea inteira da janela para desenhar (serÃ¡ explicado melhor no prÃ³ximo cÃ³digo)

def teclado(key, x, y):
    global gira, camPos, camAbertura
    if key == b' ':    
        gira = not gira                         # liga ou desliga a variÃ¡vel gira que realiza a rotaÃ§Ã£o da posiÃ§Ã£o da cÃ¢mera a cada frame

#FunÃ§Ã£o que altera variÃ¡veis de translaÃ§Ã£o, escala e rotaÃ§Ã£o a cada frame e manda redesenhar a tela
def timer(v):
    global camPos
    
    #agendando a execuÃ§Ã£o da funÃ§Ã£o timer para daqui a 1000/FPS milissegundos (executa a funÃ§Ã£o a 60 frames por segundo)
    glutTimerFunc(int(1000/FPS), timer, 0) 

    if gira:                          # posicÃ£o da cÃ¢mera Ã© modificada apenas se o giro estiver habilitado
        camPos = camRotacao * camPos  # aplicando a matriz de rotaÃ§Ã£o apenas na posiÃ§Ã£o da cÃ¢mera

    glutPostRedisplay()

#FunÃ§Ã£o usada para redesenhar o conteÃºdo do frame buffer
def desenha():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # GL_DEPTH_BUFFER_BIT: a remoÃ§Ã£o de faces traseiras utiliza um depth buffer que precisa ser limpo a cada frame

    glMatrixMode(GL_PROJECTION)  # habilitando definiÃ§Ã£o da projeÃ§Ã£o
    glLoadIdentity()             # carregando matriz identidade
    glFrustum(-1,1,-1,1,2,100)   # criando frustum de visualizaÃ§Ã£o (projeÃ§Ã£o em perspectiva)

    glMatrixMode(GL_MODELVIEW)                                          # habilitando definiÃ§Ã£o da cÃ¢mera e das matrizes de transformaÃ§Ã£o geomÃ©trica
    matrizCamera = glm.lookAt(camPos.xyz, glm.vec3(0), glm.vec3(0,1,0)) # criando matriz de cÃ¢mera com GLM e funÃ§Ã£o look-at(pos, at, up)
    glLoadMatrixf(mat2list(matrizCamera))                               # aplicando matriz de cÃ¢mera no OpenGL

    #desenhando um bule (usando funÃ§Ãµes prontas da biblioteca GLUT)
    glPushMatrix()
    glTranslatef(0,0.5,0)   # originalmente o bule Ã© centralizado na origem, entÃ£o precisa ser deslocado pra cima pra ficar sobre o chÃ£o (um quadrado no plano xz)
    glColor3f(1,1,1)        # a cor do bule serÃ¡ branca
    glutSolidTeapot(1)      # desenha o preenchimento de um bule
    glColor3f(0.5,0.5,0.5)  # a cor do wireframe do bule serÃ¡ cinza
    glutWireTeapot(1.01)    # desenha o wireframe (as arestas das faces) de um bule (sem iluminaÃ§Ã£o, Ã© uma maneira de dar aparÃªncia 3d ao objeto)
    glPopMatrix()

    #desenhando o chÃ£o no plano xz
    glPushMatrix()
    glColor3f(0.3,0.0,0.0)
    glScalef(3,1,3)
    glBegin(GL_QUADS)
    glVertex3f(-1, 0,-1)
    glVertex3f( 1, 0,-1)
    glVertex3f( 1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()
    glPopMatrix()

    glutSwapBuffers() 

#Corpo principal do cÃ³digo
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA) #utilizando Double Buffering atravÃ©s da opÃ§Ã£o GLUT_DOUBLE
glutInitWindowSize(int(janelaLargura),int(janelaAltura))
glutInitWindowPosition(0,0)
glutCreateWindow("Visualizacao 3D - Camera e Projecao em Perspectiva")
inicio()
glutDisplayFunc(desenha)
glutReshapeFunc(alteraJanela)
glutKeyboardFunc(teclado)
glutTimerFunc(int(1000/FPS), timer, 0)
glutMainLoop()



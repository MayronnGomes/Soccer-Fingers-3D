from OpenGL.GL import *
from OpenGL.GLUT import *
import glm

class Objeto:
    # Construtor
    def __init__(self,posicao,direcao,cor):
        self.posicao = posicao      # posição do objeto
        self.direcao = direcao      # vetor de direção de movimento
        self.cor = cor              # cor do objeto

    # Método responsável por mover o objeto uma certa distância na direção atual
    def move(self):
        global deslocamento, t
        self.posicao = self.posicao + t * forca
        deslocamento += t * forca
        if deslocamento.x >= forca.x/2:
            t = max(0.01, t - aceleracao)

    # Método responsável por desenhar o objeto na tela (um simples ponto neste caso)
    def desenha(self):
        glColor3f(self.cor.r, self.cor.g, self.cor.b)
        glBegin(GL_POINTS)
        glVertex2f(self.posicao.x, self.posicao.y)
        glEnd()

# Q = P + t * v

# Variáveis globais
FPS = 60          # quantidade de frames por segundo que deseja-se atualizar a aplicação
cenarioTam = 10   # coordenada máxima em x e em y nas dimensões do mundo exibido na janela
forca = glm.vec2(4, 5)
deslocamento = glm.vec2(0, 0)
aceleracao = 0.003
t = 0.03
objA = Objeto(glm.vec2(0,0),   # posição inicial do objeto (origem)
              glm.vec2(1,0),   # direção inicial de movimento do objeto (eixo x positivo = horizontal pra direita)
              glm.vec3(1,0,0)) # cor do objeto (vermelho)

# Função para agrupar as configurações iniciais do OpenGL
def inicio():
    glClearColor(1,1,1,1)       # função que define a cor de fundo usada pelo OpenGL para limpar a tela
    glPointSize(30)             # altera o tamanho dos pontos (por padrão, o tamanho é igual a 1 pixel)
    glLineWidth(3)              # altera a largura dos segmentos de reta (por padrão, a largura é de 1 pixel)
    glEnable(GL_MULTISAMPLE)    # habilita anti-aliasing (fará o ponto parecer arredondado)

# Função que será chamada a cada 1000/FPS milissegundos
def timer(v):
    global objA, forca
    
    # a cada frame é necessário chamar essa função para 'agendar' a sua próxima execução
    glutTimerFunc(int(1000/FPS), timer, 0)  
    
    #ações a serem realizadas a cada frame
    if (deslocamento.x >= forca.x) and (deslocamento.y >= forca.y):
        print("movimento parou")
        forca = glm.vec2(0)
    else:
        objA.move()
        

        
    # atualiza o frame buffer
    glutPostRedisplay()                     

# Função que será chamada cada vez que o conteúdo da janela precisar ser redesenhado
def desenha():
    # Limpa o conteúdo do frame buffer aplicando a cor usada em glClearColor em toda a imagem
    glClear(GL_COLOR_BUFFER_BIT) 

    # definindo a área de visualização
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-cenarioTam, cenarioTam, -cenarioTam, cenarioTam, -1, 1)
    
    # desenhando os objetos
    objA.desenha()

    # Mostrar a desenho feito no framebuffer na janela
    glFlush() 

# Corpo inicial do código
glutInit()                                                        
glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_SINGLE | GLUT_RGB) # configurações do frame buffer (GLUT_MULTISAMPLE = várias amostras por pixel (anti-aliasing))
glutInitWindowSize(500,500)                                    
glutInitWindowPosition(0,0)                                    
glutCreateWindow('Evento de timer')                            
inicio()                                                       
glutTimerFunc(int(1000/FPS), timer, 0) # função 'timer' será chamada daqui a 1000/FPS milissegundos
glutDisplayFunc(desenha)                                       
glutMainLoop()                                                 

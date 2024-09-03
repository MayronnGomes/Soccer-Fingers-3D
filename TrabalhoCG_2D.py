from OpenGL.GL import *
from OpenGL.GLUT import *
import glm 
from PIL import Image
import math

#variÃ¡veis globais
tex1 = 0
tex2 = 0
FPS = 30
camPos = glm.vec4(1.5,1.5,1.5,1);                                                 # posiÃ§Ã£o inicial da cÃ¢mera
camRotacao = glm.rotate(glm.mat4(1.0), glm.radians(1.0), glm.vec3(0,0,1))   # matriz de rotaÃ§Ã£o para girar a cÃ¢mera
gira = True                                                                 # variÃ¡vel que determina se a cÃ¢mera estÃ¡ ou nÃ£o girando
janelaLargura = 500                                                         # largura da janela em pixels
janelaAltura = 500                                                          # altura da janela em pixels
aspectRatio = 1                                                             # aspect ratio da janela (largura dividida pela altura)


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



def draw_grid(l, a, divisoes):
    glColor3f(1, 1, 1)  # Branco (não necessário se estiver mapeando texturas)

    canto = glm.vec3(0, 0, 0)
    linha = l / divisoes
    coluna = a / divisoes
    linhaTex = 1 / divisoes
    colunaTex = 1 / divisoes

    glBegin(GL_QUADS)
    for i in range(divisoes):
        for j in range(divisoes):
            # Vértice inferior esquerdo
            glTexCoord2f(canto.x + i * linhaTex, canto.y + j * colunaTex)
            glVertex3f(canto.x + i * linha, canto.y + j * coluna, canto.z)

            # Vértice superior esquerdo
            glTexCoord2f(canto.x + i * linhaTex, canto.y + (j + 1) * colunaTex)
            glVertex3f(canto.x + i * linha, canto.y + (j + 1) * coluna, canto.z)

            # Vértice superior direito
            glTexCoord2f(canto.x + (i + 1) * linhaTex, canto.y + (j + 1) * colunaTex)
            glVertex3f(canto.x + (i + 1) * linha, canto.y + (j + 1) * coluna, canto.z)

            # Vértice inferior direito
            glTexCoord2f(canto.x + (i + 1) * linhaTex, canto.y + j * colunaTex)
            glVertex3f(canto.x + (i + 1) * linha, canto.y + j * coluna, canto.z)
    glEnd()

# def draw_cylinder(radius, height, divisoes):
#     glColor3f(1, 1, 1)  # Branco (não necessário se estiver mapeando texturas)

#     # Divisões ao longo da altura e circunferência
#     altura_div = height / divisoes
#     angulo_div = (2 * math.pi) / divisoes
#     tex_div_h = 1 / divisoes
#     tex_div_a = 1 / divisoes

#     glBegin(GL_QUADS)
#     for i in range(divisoes):
#         for j in range(divisoes):
#             # Calcula os ângulos para os vértices ao redor da circunferência
#             theta1 = i * angulo_div
#             theta2 = (i + 1) * angulo_div
            
#             # Calcula as alturas para os vértices ao longo do cilindro
#             z1 = j * altura_div
#             z2 = (j + 1) * altura_div

#             # Vértice inferior esquerdo
#             glTexCoord2f(i * tex_div_a, j * tex_div_h)
#             glVertex3f(radius * math.cos(theta1), radius * math.sin(theta1), z1)

#             # Vértice superior esquerdo
#             glTexCoord2f(i * tex_div_a, (j + 1) * tex_div_h)
#             glVertex3f(radius * math.cos(theta1), radius * math.sin(theta1), z2)

#             # Vértice superior direito
#             glTexCoord2f((i + 1) * tex_div_a, (j + 1) * tex_div_h)
#             glVertex3f(radius * math.cos(theta2), radius * math.sin(theta2), z2)

#             # Vértice inferior direito
#             glTexCoord2f((i + 1) * tex_div_a, j * tex_div_h)
#             glVertex3f(radius * math.cos(theta2), radius * math.sin(theta2), z1)
#     glEnd()

def computeSphereCoord(long, lat, radius):
    long_rad = (math.pi / 180) * long
    lat_rad = (math.pi / 180) * lat
    x = radius * math.cos(long_rad) * math.cos(lat_rad)
    y = radius * math.sin(long_rad) * math.cos(lat_rad)
    z = radius * math.sin(lat_rad)
    return glm.vec3(x, y, z)

def draw_sphere(radius, divisoes):
    glColor3f(1, 1, 1)  # Branco (não necessário se estiver mapeando texturas)
    
    # Divisões para latitude e longitude
    lat_div = divisoes
    long_div = divisoes
    
    # Incrementos para latitude e longitude em graus
    lat_increment = int(180 / lat_div)
    long_increment = int(360 / long_div)
    
    glBegin(GL_QUADS)
    
    for lat in range(-90, 90, lat_increment):
        for long in range(0, 360, long_increment):
            # Cálculo dos ângulos para os quatro vértices dos quadrados
            lat1 = lat
            lat2 = lat + lat_increment
            long1 = long
            long2 = long + long_increment
            
            # Vértices para o quadrado na esfera
            v1 = computeSphereCoord(long1, lat1, radius)
            v2 = computeSphereCoord(long2, lat1, radius)
            v3 = computeSphereCoord(long2, lat2, radius)
            v4 = computeSphereCoord(long1, lat2, radius)
            
            # Coordenadas de textura baseadas na latitude e longitude
            tex_coord1 = (long1 / 360.0, (90 - lat1) / 180.0)
            tex_coord2 = (long2 / 360.0, (90 - lat1) / 180.0)
            tex_coord3 = (long2 / 360.0, (90 - lat2) / 180.0)
            tex_coord4 = (long1 / 360.0, (90 - lat2) / 180.0)
            
            # Vértices e coordenadas de textura para o quadrado
            # inf esq
            glTexCoord2f(*tex_coord1)
            glVertex3f(v1.x, v1.y, v1.z)
            
            # sup esq
            glTexCoord2f(*tex_coord2)
            glVertex3f(v2.x, v2.y, v2.z)
            
            # sup dir
            glTexCoord2f(*tex_coord3)
            glVertex3f(v3.x, v3.y, v3.z)
            
            # inf dir
            glTexCoord2f(*tex_coord4)
            glVertex3f(v4.x, v4.y, v4.z)
    
    glEnd()

def computeCylinderCoord(h, a, radius):
    a_rad = (math.pi / 180) * a
    x = radius * math.cos(a_rad)
    y = radius * math.sin(a_rad)
    z = h
    return glm.vec3(x, y, z)

def draw_cylinder(radius, height, divisoes, corpo, tampa):
    glBindTexture(GL_TEXTURE_2D, corpo)

    glColor3f(1, 1, 1)  # Branco (não necessário se estiver mapeando texturas)
    
    # Divisões ao longo da altura e circunferência
    altura_div = height / divisoes
    angulo_div = (360 / divisoes)  # Divisões angulares em graus

    glBegin(GL_QUADS)
    
    for i in range(divisoes):
        for j in range(divisoes):
            # Calcula os ângulos para os vértices ao redor da circunferência
            angle1 = i * angulo_div
            angle2 = (i + 1) * angulo_div
            
            # Calcula as alturas para os vértices ao longo do cilindro
            z1 = j * altura_div
            z2 = (j + 1) * altura_div

            # Vértices para o quadrado na superfície do cilindro
            v1 = computeCylinderCoord(z1, angle1, radius)
            v2 = computeCylinderCoord(z1, angle2, radius)
            v3 = computeCylinderCoord(z2, angle2, radius)
            v4 = computeCylinderCoord(z2, angle1, radius)
            
            # Coordenadas de textura baseadas na altura e ângulo
            tex_coord1 = (i / divisoes, j / divisoes)
            tex_coord2 = ((i + 1) / divisoes, j / divisoes)
            tex_coord3 = ((i + 1) / divisoes, (j + 1) / divisoes)
            tex_coord4 = (i / divisoes, (j + 1) / divisoes)
            
            # Vértices e coordenadas de textura para o quadrado
            glTexCoord2f(*tex_coord1)
            glVertex3f(v1.x, v1.y, v1.z)
            
            glTexCoord2f(*tex_coord2)
            glVertex3f(v2.x, v2.y, v2.z)
            
            glTexCoord2f(*tex_coord3)
            glVertex3f(v3.x, v3.y, v3.z)
            
            glTexCoord2f(*tex_coord4)
            glVertex3f(v4.x, v4.y, v4.z)
    
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)

     # Desenhar a tampa superior
    glBindTexture(GL_TEXTURE_2D, tampa)

    draw_cylinder_cap(radius, height, divisoes)

    # Desenhar a tampa inferior
    draw_cylinder_cap(radius, 0, divisoes)
    glBindTexture(GL_TEXTURE_2D, 0)
    
def draw_cylinder_cap(radius, z, divisoes):
    """Função para desenhar a tampa (topo ou base) do cilindro"""
    angulo_div = (360 / divisoes)  # Divisões angulares em graus

    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0.5, 0.5)  # Coordenada de textura para o centro
    glVertex3f(0, 0, z)  # Centro da tampa

    for i in range(divisoes + 1):
        angle = i * angulo_div
        v = computeCylinderCoord(0, angle, radius)
        
        # Coordenada de textura baseada no ângulo
        tex_coord = (0.5 + 0.5 * math.cos(math.radians(angle)), 0.5 + 0.5 * math.sin(math.radians(angle)))

        glTexCoord2f(*tex_coord)
        glVertex3f(v.x, v.y, z)
    
    glEnd()


#FunÃ§Ã£o contendo configuraÃ§Ãµes iniciais
def inicio():
    global tex1, tex2
    glClearColor(0.5,0.5,0.5,1)
    glClearDepth(1.0)
    glLineWidth(1)           # altera a largura das linhas para 1 pixel
    glEnable(GL_DEPTH_TEST)  # habilitando a remoÃ§Ã£o de faces que estejam atrÃ¡s de outras (remoÃ§Ã£o de faces traseiras)
    glEnable(GL_TEXTURE_2D)                             # habilitando o uso de texturas
    glEnable(GL_BLEND);                                 # habilitando a funcionalidade de mistura (necessário para objetos transparentes)
    glDepthFunc(GL_LEQUAL)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_MULTISAMPLE) # habilita um tipo de antialiasing (melhora serrilhado de linhas e bordas de polÃ­gonos)
    # tex1 = carregaTextura('../Texturas/earth.jpg')

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
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE)                                              # definindo que a cor da textura substituirá a cor do polígono
    glTexImage2D(GL_TEXTURE_2D, 
                 0, 
                 GL_RGBA,  
                 img.width, 
                 img.height, 
                 0, 
                 GL_RGBA, 
                 GL_UNSIGNED_BYTE, 
                 imgData)  # enviando os dados lidos pelo módulo PIL para a OpenGL
    glBindTexture(GL_TEXTURE_2D, 0)                                                                         # tornando o objeto textura inativo por enquanto

    #retornando o identificador da textura recém-criada
    return texId

#FunÃ§Ã£o usada para redesenhar o conteÃºdo do frame buffer
def desenha():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # GL_DEPTH_BUFFER_BIT: a remoÃ§Ã£o de faces traseiras utiliza um depth buffer que precisa ser limpo a cada frame

    glMatrixMode(GL_PROJECTION)  # habilitando definiÃ§Ã£o da projeÃ§Ã£o
    glLoadIdentity()             # carregando matriz identidade
    glFrustum(-1,1,-1,1,2,30)   # criando frustum de visualizaÃ§Ã£o (projeÃ§Ã£o em perspectiva)

    glMatrixMode(GL_MODELVIEW)                                          # habilitando definiÃ§Ã£o da cÃ¢mera e das matrizes de transformaÃ§Ã£o geomÃ©trica
    matrizCamera = glm.lookAt(camPos.xyz, glm.vec3(0), glm.vec3(0,0,1)) # criando matriz de cÃ¢mera com GLM e funÃ§Ã£o look-at(pos, at, up)
    glLoadMatrixf(mat2list(matrizCamera))                               # aplicando matriz de cÃ¢mera no OpenGL

    # glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    # draw_cylinder(3, 5, 60, tex1, tex2)
    # glBindTexture(GL_TEXTURE_2D, tex1)
    # draw_sphere(3, 60)
    # glBindTexture(GL_TEXTURE_2D, 0)

    glScalef(0.1, 0.1, 0.1)
    draw_obj(vertices, textures, normals, faces)

    glutSwapBuffers()
    

    glutSwapBuffers() 


#Corpo principal do cÃ³digo
filename = "goal.obj"
vertices, textures, normals, faces = load_obj(filename)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH) #utilizando Double Buffering atravÃ©s da opÃ§Ã£o GLUT_DOUBLE
glutInitWindowSize(int(janelaLargura),int(janelaAltura))
glutInitWindowPosition(0,0)
glutCreateWindow("Visualizacao 3D - Camera e Projecao em Perspectiva")
inicio()
glutDisplayFunc(desenha)
glutReshapeFunc(alteraJanela)
glutKeyboardFunc(teclado)
glutTimerFunc(int(1000/FPS), timer, 0)
glutMainLoop()



import glm
import math
import CONSTS
from PIL import Image
from OpenGL.GL import *

def recalcMov(normal):

    CONSTS.forca = glm.reflect(CONSTS.forca, normal)
    CONSTS.deslocamento = glm.reflect(CONSTS.deslocamento, normal)
    CONSTS.velocidade = glm.reflect(CONSTS.velocidade, normal)

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

def mat2list(M):
    matrix = []
    for i in range(0,4):
        matrix.append(list(M[i]))
    return matrix

def computeCylinderCoord(h, a, radius):
    a_rad = (math.pi / 180) * a
    x = radius * math.cos(a_rad)
    y = radius * math.sin(a_rad)
    z = h
    return glm.vec3(x, y, z)
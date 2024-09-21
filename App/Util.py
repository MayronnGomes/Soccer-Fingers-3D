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
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE)                                              # definindo que a cor da textura substituirá a cor do polígono
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

def computeSphereCoord(long, lat, radius=1):
    long_rad = (math.pi / 180) * long
    lat_rad = (math.pi / 180) * lat
    x = radius * math.cos(long_rad) * math.cos(lat_rad)
    y = radius * math.sin(long_rad) * math.cos(lat_rad)
    z = radius * math.sin(lat_rad)
    return glm.vec3(x, y, z)

def load_obj(filename):
    vertices = []
    faces = []
    normals = []
    face_materials = []
    current_material = None

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

    return vertices, faces, normals, face_materials

def load_obj_gol(filename):
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

# Calcula a cor de sombreamento de um ponto usando o Modelo de IluminaÃ§Ã£o de Phong
def shading(point, normal, objeto):
    # reflexão ambiente (Ra = Ia * Ka)
    shadeAmbient = CONSTS.lightAmbient * CONSTS.surfaceAmbient

    # reflexão difusa (Rd = Id * Kd * (l * n))
    l = glm.normalize(CONSTS.lightPosition - point) # Luz - Ponto
    n = glm.normalize(normal)
    shadeDiffuse = objeto.lightDiffuse * objeto.surfaceDiffuse * glm.max(0.0, glm.dot(l,n))

    # reflexão especular (Rs = Is  * Ks * (v * r)^e)
    v = glm.normalize(CONSTS.cameraPosition - point)
    r = 2*glm.dot(n,l)*n - l
    shadeSpecular = objeto.lightSpecular * objeto.surfaceSpecular * glm.max(0, glm.dot(v,r) ** objeto.surfaceShine)

    # modelo de iluminação de Phong (R = Ra + Rd + Rs)
    shade = shadeAmbient + shadeDiffuse + shadeSpecular

    return shade

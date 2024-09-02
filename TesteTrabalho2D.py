import math
import glm
from OpenGL.GL import *

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
    lat_increment = 180 / lat_div
    long_increment = 360 / long_div
    
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
            glTexCoord2f(*tex_coord1)
            glVertex3f(v1.x, v1.y, v1.z)
            
            glTexCoord2f(*tex_coord2)
            glVertex3f(v2.x, v2.y, v2.z)
            
            glTexCoord2f(*tex_coord3)
            glVertex3f(v3.x, v3.y, v3.z)
            
            glTexCoord2f(*tex_coord4)
            glVertex3f(v4.x, v4.y, v4.z)
    
    glEnd()

def computeCylinderCoord(h, a, radius):
    a_rad = (math.pi / 180) * a
    x = radius * math.cos(a_rad)
    y = radius * math.sin(a_rad)
    z = h
    return glm.vec3(x, y, z)

def draw_cylinder(radius, height, divisoes):
    glColor3f(1, 1, 1)  # Branco (não necessário se estiver mapeando texturas)
    
    # Divisões ao longo da altura e circunferência
    altura_div = height / divisoes
    angulo_div = (360 / divisoes)  # Divisões angulares em graus
    tex_div_h = 1 / divisoes
    tex_div_a = 1 / divisoes

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

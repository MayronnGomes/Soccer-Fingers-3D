import glm

import numpy as np
import glm
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

FPS = 30
divisaoCilindro = 60
campoLar = 30
campoAlt = 15
bolaRaio = 1
mundoLar  = 10
mundoAlt  = 12
janelaLar = 960
janelaAlt = 540
dir = glm.vec3(0, bolaRaio, 0)
lat = glm.vec3(bolaRaio, 0, 0)
M = glm.mat4(1) #
texCampo   = 0 
texProgBar = 0 #
progressbar = False #
mov = False
angleProgressbar = 0.0 #
forca = glm.vec3(0.0, 0.0, 0.0)
deslocamento = glm.vec3(0.0, 0.0, 0.0)
velocidade = glm.vec3(0.0, 0.0, 0.0)
winner = ""
normal = glm.vec3(0, 0, 0)
colisao = None
cameraPosition = None
# lightPosition = glm.vec3(0, 0, 30)
# lightAmbient = glm.vec3(0.1)    
# lightDiffuse = glm.vec3(1.0)                    
# lightSpecular = glm.vec3(1.0)  
# surfaceAmbient = glm.vec3(0.1)         
# surfaceDiffuse = glm.vec3(1,1,1)              
# surfaceSpecular = glm.vec3(0.5)                      
# surfaceShine = 128

SIGLAS = {}

PLACAR = {}

TIME = {
    "belgica": 0,
    "brasil": 0,
    "inglaterra": 0,
    "italia": 0
}

CAMISAS_TIME = {
    "belgica": glm.vec3(1, 0, 0),
    "brasil": glm.vec3(1, 204/255, 0),
    "inglaterra": glm.vec3(1, 1, 1),
    "italia": glm.vec3(0, 130/255, 99/255)
}

OPTIONS = [glm.vec3(-4.5, 3.3, 0), glm.vec3(-5.5, 0.6, 0), glm.vec3(-3.5, -2, 0), glm.vec3(mundoLar * 0.45, 0, 0)] # 0-2: Tela Inicial | 3: Tela Times

OPTIONSTIMES = [i for i in TIME.keys()]

FORMATION = {
    "1": [glm.vec3(-campoLar/2 + 3, 0, 0), glm.vec3(-campoLar/4 - 1, -4, 0), glm.vec3(-campoLar/4 - 1, 4, 0), glm.vec3(-7, 0, 0), glm.vec3(-3, 0, 0)],
    "2": [glm.vec3(-campoLar/2 + 5, 2, 0), glm.vec3(-campoLar/2 + 5, -2, 0), glm.vec3(-campoLar/4 + 2.5, 5, 0), glm.vec3(-campoLar/4 + 2.5, -5, 0), glm.vec3(-3, 0, 0)],
    "3": [glm.vec3(-campoLar/2 + 3, 2, 0), glm.vec3(-campoLar/2 + 3, -2, 0), glm.vec3(-campoLar/4 + 1, 0, 0), glm.vec3(-3, -5, 0), glm.vec3(-3, 5, 0)],
    "4": [glm.vec3(-campoLar/2 + 4, -3.5, 0), glm.vec3(-campoLar/2 + 4, 3.5, 0), glm.vec3(-campoLar/4 + 1, 2, 0), glm.vec3(-campoLar/4 + 1, -2, 0), glm.vec3(-3, 0, 0)],
    "5": [glm.vec3(-campoLar/2 + 3, 0, 0), glm.vec3(-campoLar/4, -5, 0), glm.vec3(-campoLar/4, 5, 0), glm.vec3(-3, -2, 0), glm.vec3(-3, 2, 0)],
    "6": [glm.vec3(-campoLar/2 + 4, 0, 0), glm.vec3(-7, -4, 0), glm.vec3(-7, 4, 0), glm.vec3(-7, 0, 0), glm.vec3(-3, 0, 0)],
    "7": [glm.vec3(-campoLar/2 + 3, 0, 0), glm.vec3(-3.5, -2, 0), glm.vec3(-3.5, 2, 0), glm.vec3(-3.5, -6, 0), glm.vec3(-3.5, 6, 0)],
    "8": [glm.vec3(-campoLar/2 + 3, 0, 0), glm.vec3(-6.5, -4, 0), glm.vec3(-6.5, 4, 0), glm.vec3(-campoLar/4 - 0.5, 0, 0), glm.vec3(-3, 0, 0)]
}

TELAS = {"inicial": 0,
         "times": 0,
         "formação1": 0,
         "formação2": 0#,
        #  "gol": 0,
        #  "vencedor": 0
}
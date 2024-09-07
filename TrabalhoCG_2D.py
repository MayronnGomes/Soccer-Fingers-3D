import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Definir os limites da janela de recorte
xmin, xmax = -1.0, 1.0
ymin, ymax = -1.0, 1.0
zmin, zmax = -1.0, 1.0

def compute_code_3d(x, y, z): #ok
    code = 0
    if x < xmin:  # à esquerda
        code |= 1
    elif x > xmax:  # à direita
        code |= 2
    if y < ymin:  # abaixo
        code |= 4
    elif y > ymax:  # acima
        code |= 8
    if z < zmin:  # atrás
        code |= 16
    elif z > zmax:  # na frente
        code |= 32
    return code

def liang_barsky_clip_3d(x1, y1, z1, x2, y2, z2):
    # Calcula as variações nas coordenadas (diferença entre os pontos finais e iniciais do segmento)
    dx = x2 - x1  # Variação no eixo X
    dy = y2 - y1  # Variação no eixo Y
    dz = z2 - z1  # Variação no eixo Z

    # Definindo os vetores para as bordas (p) e as distâncias até os limites (q)
    # p[i] define a direção da reta em relação ao plano de clipping
    # q[i] define a distância do ponto inicial até o plano de clipping correspondente

    p = [-dx, dx, -dy, dy, -dz, dz]
    # p[0] = -dx, p[1] = dx -> Planos X min/max
    # p[2] = -dy, p[3] = dy -> Planos Y min/max
    # p[4] = -dz, p[5] = dz -> Planos Z min/max

    q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1, z1 - zmin, zmax - z1]
    # q[0] = x1 - xmin -> Distância até o plano Xmin
    # q[1] = xmax - x1 -> Distância até o plano Xmax
    # q[2] = y1 - ymin -> Distância até o plano Ymin
    # q[3] = ymax - y1 -> Distância até o plano Ymax
    # q[4] = z1 - zmin -> Distância até o plano Zmin
    # q[5] = zmax - z1 -> Distância até o plano Zmax

    # Inicializando os parâmetros Tin e Tout:
    Tin = 0.0  # Valor paramétrico inicial (t = 0, ponto inicial do segmento)
    Tout = 1.0  # Valor paramétrico final (t = 1, ponto final do segmento)

    # Iteramos sobre as 6 bordas (Xmin, Xmax, Ymin, Ymax, Zmin, Zmax)
    for i in range(6):
        # Caso a reta seja paralela a uma borda (p[i] == 0) e esteja fora (q[i] < 0):
        if p[i] == 0 and q[i] < 0:
            # Isso significa que o segmento é completamente externo ao volume de recorte
            return None  # Sem interseção, segmento totalmente fora

        # Caso a reta não seja paralela à borda:
        if p[i] != 0:
            # Calcula o valor paramétrico t (interseção com a borda)
            t = q[i] / p[i]

            if p[i] < 0:
                # Se p[i] < 0, estamos lidando com uma borda de entrada
                Tin = max(Tin, t)
                # Atualizamos Tin, mantendo o maior valor
            else:
                # Se p[i] > 0, estamos lidando com uma borda de saída
                Tout = min(Tout, t)
                # Atualizamos Tout, mantendo o menor valor

    # Verificação final: se Tin > Tout, o segmento está completamente fora.
    if Tin > Tout:
        return None  # Sem interseção, segmento totalmente fora

    # Cálculo dos pontos de interseção para o segmento recortado (usando os valores ajustados de Tin e Tout):
    x1_clip = x1 + Tin * dx  # Novo ponto inicial recortado
    y1_clip = y1 + Tin * dy  # Novo ponto inicial recortado
    z1_clip = z1 + Tin * dz  # Novo ponto inicial recortado

    x2_clip = x1 + Tout * dx  # Novo ponto final recortado
    y2_clip = y1 + Tout * dy  # Novo ponto final recortado
    z2_clip = z1 + Tout * dz  # Novo ponto final recortado

    return x1_clip, y1_clip, z1_clip, x2_clip, y2_clip, z2_clip  # Retorna os novos pontos recortados

def cohen_sutherland_clip_3d(x1, y1, z1, x2, y2, z2):
    # Calcular os outcodes para os dois pontos
    code1 = compute_code_3d(x1, y1, z1)
    code2 = compute_code_3d(x2, y2, z2)

    while True:
        # Possibilidade 1: Se ambos os outcodes são 0, o segmento está totalmente dentro do volume
        if code1 == 0 and code2 == 0:
            return x1, y1, z1, x2, y2, z2  # Segmento aceito

        # Possibilidade 3: Se o operador AND entre os outcodes não é zero, o segmento está fora do volume
        elif code1 & code2 != 0:
            return None  # Segmento completamente fora do volume, rejeitado

        # Possibilidade 2 e 4: Precisamos recortar o segmento
        else:
            # Escolher um dos pontos fora do volume para recortar
            if code1 != 0:
                clipped_segment = liang_barsky_clip_3d(x1, y1, z1, x2, y2, z2)
                if clipped_segment is not None:
                    x1, y1, z1, x2, y2, z2 = clipped_segment
                    code1 = compute_code_3d(x1, y1, z1)
                else:
                    return None  # Segmento fora após clipping
            else:
                clipped_segment = liang_barsky_clip_3d(x2, y2, z2, x1, y1, z1)
                if clipped_segment is not None:
                    x2, y2, z2, x1, y1, z1 = clipped_segment
                    code2 = compute_code_3d(x2, y2, z2)
                else:
                    return None  # Segmento fora após clipping

    return None  # Segmento fora do volume

def draw_line(x1, y1, x2, y2):
    plt.plot([x1, x2], [y1, y2], 'g', linewidth=2)

# Função para desenhar a janela de recorte e regiões
def draw_window():
    fig, ax = plt.subplots()
    # Desenhar a janela de recorte (área central)
    ax.add_patch(Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, fill=False, edgecolor='b', linewidth=2))
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)

# Exemplo de uso
draw_window()

# Exemplo de linha fora e dentro do espaço
x1, y1, x2, y2 = -0.5, -1.5, 1.25, 0.75
cohen_sutherland_clip_9_regions(x1, y1, x2, y2)

# Mostrar resultado
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

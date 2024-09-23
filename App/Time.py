import CONSTS
from Jogador import *

class Time:

    def __init__(self, escudo, formacao, visitante):
        self.escudo = escudo
        self.formacao = formacao
        self.visitante = visitante
        self.jogadores = [Jogador(1, 1, self.escudo, (self.formacao[i]*(-1) if self.visitante else self.formacao[i])) for i in range(5)]

    def desenha(self):
        for i in self.jogadores:
            glPushMatrix()
            i.desenha()
            glPopMatrix()

    def alterarFormacao(self):
        for i in range(0, 5):
            self.jogadores[i].posicao = self.formacao[i]*(-1) if self.visitante else self.formacao[i]

    def colisao(self, bola):
        for i in self.jogadores:
            colisao_jogador = i.verifica_colisao(bola)

            if colisao_jogador:
                return True
            
        return False
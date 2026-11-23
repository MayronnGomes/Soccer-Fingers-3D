# Soccer Fingers 3D

Jogo de futebol 3D em **computação gráfica**, feito em Python com **OpenGL**. Tem campo, times com formações, bola, jogadores, placar, texturas e sons (chute, apito e gol).

A versão 2D está em [Soccer-Fingers-2D](https://github.com/MayronnGomes/Soccer-Fingers-2D).

<!-- Adicione aqui um print ou GIF do jogo em docs/ e referencie: ![Jogo](docs/jogo.gif) -->

## Tecnologias

Python · PyOpenGL (GLUT) · PyGLM · NumPy · Pillow · Pygame (sons)

## O que há no código

- `Game` com laço de jogo, temporizador de quadros, teclado e mouse.
- `Campo`, `Bola`, `Jogador`, `Time`, `Formation` e `Placar`.
- Primitivas geométricas (`Cube`, `Triangule`, `Cilindro`).
- Pastas `Texturas` e `Sons` com os recursos do jogo.

## Como rodar

Requisito: Python 3.12.

```bash
pip install PyOpenGL PyGLM numpy pillow pygame
cd App
python Game.py
```

Execute de dentro da pasta `App`, porque os caminhos de sons e texturas são relativos.

## Autor

Mayronn Gomes Viana. Projeto de computação gráfica desenvolvido durante a graduação na UFC.

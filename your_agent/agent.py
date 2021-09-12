import random
import sys
import board
from copy import deepcopy

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


# Peso de cada posição no tabuleiro estimado de artigos sobre o jogo
peso_posicao = [
    [100, -20,  10,   5,   5,  10, -20, 100],
    [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
    [10,  -2,  -1,   -1,   -1,  -1,  -2,  10],
    [5,  -2,  -1,   -1,   -1,  -1,  -2,  5],
    [5,  -2,  -1,   -1,   -1,  -1,  -2,  5],
    [10,  -2,  -1,   -1,   -1,  -1,  -2,  10],
    [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
    [100, -20,  10,   5,   5,  10, -20, 100]
]

# Busca quais posições no tabuleiro estão sendo ocupadas por certa cor
def busca_posicoes(the_board, color):
    posicoes = []
    for y in range(8):
        for x in range(8):
            if the_board.tiles[x][y] == color:
                posicoes.append((x, y))
    return posicoes

# Busca o valor do tabuleiro de acordo com o peso das posições levando em conta as nossas posições e as do oponente
# Quanto menor o valor melhor
def valor_tabuleiro(the_board, color):
    total = 0
    oponente = the_board.opponent(color)
    minhas_posicoes = busca_posicoes(the_board, color)
    posicoes_oponente = busca_posicoes(the_board, oponente)

    for posicao in minhas_posicoes:
        total -= peso_posicao[posicao[0]][posicao[1]]

    for posicao in posicoes_oponente:
        total += peso_posicao[posicao[0]][posicao[1]]

    return total

# Execução do MAX com poda alfa-beta
def valor_max(the_board, color, score, score_oponente, depth):
    if depth == 0:
        return valor_tabuleiro(the_board,color)
   
    legal_moves = the_board.legal_moves(color)

    if not legal_moves:
        return valor_min(the_board, color, score, score_oponente, depth-1)

    for move in legal_moves:
        copy_board = deepcopy(the_board)
        copy_board.process_move(move, color)
        valor = valor_min(copy_board, the_board.opponent(color), score, score_oponente, depth-1)
        if valor >= score_oponente:
            return valor
        if valor > score:
            score = valor 

    return score

# Execução do MIN com poda alfa-beta
def valor_min(the_board, color, score, score_oponente, depth):
    if depth == 0:
        return valor_tabuleiro(the_board,color)
   
    legal_moves = the_board.legal_moves(color)

    if not legal_moves:
        return valor_min(the_board, color, score, score_oponente, depth-1)

    for move in legal_moves:
        copy_board = deepcopy(the_board)
        copy_board.process_move(move, color)
        valor = valor_min(copy_board, color, score, score_oponente, depth-1)
        if valor < score:
            return valor
        if valor < score_oponente:
            score_oponente = valor 

    return score_oponente

# Função que retorna a decisão do minmax de acordo com os movimentos possíveis
def decisao_minmax(the_board, color, depth):
    legal_moves = the_board.legal_moves(color)
    movimento = None 
    score = -10000 #Alfa 
    score_oponente = 10000 #Beta

    for move in legal_moves:
        copy_board = deepcopy(the_board)
        copy_board.process_move(move,color)
        valor = valor_max(copy_board, color, score, score_oponente, depth)
        if valor > score:
            score = valor
            movimento = move

    return movimento


def make_move(the_board, color):
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    
    legal_moves = the_board.legal_moves(color)

    # Escolhe a profundidade que vai buscar 
    # 2 vai de boa, 3 ja demora um pouco mais e 4 não rola
    depth = 2

    return decisao_minmax(the_board,color,depth) if len(legal_moves) > 0 else (-1, -1)

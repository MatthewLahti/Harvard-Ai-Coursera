
"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None
human = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    num = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                num += 1
    if num % 2 != 0:
        return "X"
    return "O"


def actions(board):
    action = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.append((i,j))
    return action


def result(board, action):
    if type(action) == int or action == None:
        return board
    currentPlayer = player(board)
    board[action[0]][action[1]] = currentPlayer
    return board


def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != None:
            return board[i][0]
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != None:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]
    return None

def terminal(board):
    if len(actions(board)) == 0:
        return True
    if winner(board):
        return True
    return False


def utility(board):
    cwinner = winner(board)
    if cwinner == X:
        return 1
    elif cwinner == O:
        return -1
    else:
        return 0

def undoMove(board,move):
    i = move[0]
    j = move[1]
    board[i][j] = EMPTY

def minimax(board):
    if not terminal(board):
        if len(actions(board)) == 9:
            return actions(board)[0]
        isMax = False
        if player(board) == "X":
            isMax = True
        retVal = realMinimax(board,isMax)
        return retVal['move']

def realMinimax(board,maximizingPlayer):
    if winner(board):
        return {'score':utility(board)}
    elif len(actions(board)) == 0:
        return {'score': 0}
    if maximizingPlayer:
        best = {'move':None,'score':-math.inf}
    else:
        best = {'move':None,'score':math.inf}
    for move in actions(board):
        board = result(board,move)
        temporaryScore = realMinimax(board,not maximizingPlayer)
        undoMove(board,move)
        temporaryScore['move'] = move
        if maximizingPlayer:
            if temporaryScore['score'] > best['score']:
                best = temporaryScore
        else:
            if temporaryScore['score'] < best['score']:
                best = temporaryScore
    return best

from flask import Flask, render_template, request, jsonify
import json

import copy

board = [["br", "bk", "bb", "bq", "bK", "bb", "bk", "br"],
         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
         ["wr", "wk", "wb", "wq", "wK", "wb", "wk", "wr"]]

prevClick = [-1, -1]# last valid click
lastPawn = [-1,-1] #only for en passant
prevPos = [] # all the possible positions made by last valid click

turn = "w"
bL = False
bR = False
wL = False
wR = False
wK = False
bK = False
promote = 0
promoteCol = -1
promotePawn = [-1,-1] # pos of pawn that is about to get promoted

def isCheck(brd):
    white = False
    black = False
    for i in range(8):
        for j in range(8):
            if j == 6:
                sadf = 0
            if brd[i][j] != "  ":
                color = brd[i][j][0]
                type = brd[i][j][1]
                if type == "k":
                    for k in [[1, 2], [1, -2], [2, 1], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]:
                        newR = i + k[0]
                        newC = j + k[1]
                        if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC][0] != color and brd[newR][newC][1] == "K":
                            if color == "w":
                                black = True
                            else:
                                white = True
                if type == "b":
                    for k in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        step = 1
                        while True:
                            newR = i + k[0] * step
                            newC = j + k[1] * step
                            if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC][0] != color and brd[newR][newC][1] == "K":
                                if color == "w":
                                    black = True
                                else:
                                    white = True
                            if min(newC,newR)<0 or max(newC,newR)>7:
                                break
                            if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC] != "  ":
                                break
                            step += 1
                if type == "r":
                    for k in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        step = 1
                        while True:
                            newR = i + k[0] * step
                            newC = j + k[1] * step
                            if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC][0] != color and brd[newR][newC][1] == "K":
                                if color == "w":
                                    black = True
                                else:
                                    white = True
                            if min(newC,newR)<0 or max(newC,newR)>7:
                                break
                            if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC] != "  ":
                                break
                            step += 1
                if type == "p" and color == "w":
                    newR = i - 1
                    newC = j - 1
                    if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC] == "bK":
                        black = True
                    newC = j + 1
                    if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC] == "bK":
                        black = True
                if type == "p" and color == "b":
                    newR = i + 1
                    newC = j - 1
                    if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC] == "wK":
                        white = True
                    newC = j + 1
                    if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC] == "wK":
                        white = True
                if type == "q":
                    for k in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        step = 1
                        while True:
                            newR = i + k[0] * step
                            newC = j + k[1] * step
                            if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC][0] != color and brd[newR][newC][1] == "K":
                                if color == "w":
                                    black = True
                                else:
                                    white = True
                            if min(newC,newR)<0 or max(newC,newR)>7:
                                break
                            if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC] !=  "  ":
                                break
                            step += 1
                    for k in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        step = 1
                        while True:
                            newR = i + k[0] * step
                            newC = j + k[1] * step
                            if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC][0] != color and brd[newR][newC][1] == "K":
                                if color == "w":
                                    black = True
                                else:
                                    white = True
                            if min(newC,newR)<0 or max(newC,newR)>7:
                                break
                            if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC] !=  "  ":
                                break
                            step += 1
                if type == "K":
                    for k in [1, -1, 0]:
                        for l in [1, -1, 0]:
                            if k == l and l == 0:
                                continue
                            newR = i + k
                            newC = j + l
                            if min(newC, newR) >= 0 and max(newC, newR) <= 7 and brd[newR][newC][1] == "K":
                                white = True
                                black = True
    return [white, black]


def moveKnight(pos):
    global turn
    moves = []
    color = board[pos[0]][pos[1]][0]
    for i in [[1, 2], [1, -2], [2, 1], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]:
        newR = pos[0] + i[0]
        newC = pos[1] + i[1]
        if min(newC, newR) >= 0 and max(newC, newR) <= 7 and board[newR][newC][0] != turn:
            newB = copy.deepcopy(board)
            newB[newR][newC] = board[pos[0]][pos[1]]
            newB[pos[0]][pos[1]] = "  "
            check = isCheck(newB)
            if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
                moves.append([newR, newC])
    return moves


def moveBishop(pos):
    global turn

    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    color = board[pos[0]][pos[1]][0]
    for direction in directions:
        newR, newC = pos[0] + direction[0], pos[1] + direction[1]
        while 0 <= newR <= 7 and 0 <= newC <= 7:
            if board[newR][newC][0] != turn:
                newB = copy.deepcopy(board)
                newB[newR][newC] = board[pos[0]][pos[1]]
                newB[pos[0]][pos[1]] = "  "
                check = isCheck(newB)
                if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
                    moves.append([newR, newC])
            if board[newR][newC] != "  ":
                break
            newR += direction[0]
            newC += direction[1]

    return moves


def whiteLong():
    if wL == True or wK == True:
        return False
    if board[7][1]!="  " or board[7][2]!="  " or board[7][3]!="  ":
        return False
    brd = copy.deepcopy(board)
    if isCheck(brd)[0] == True:
        return False
    brd[7][3] = "wK"
    brd[7][4] = "  "
    if isCheck(brd)[0]:
        return False
    brd[7][2] = "wK"
    brd[7][3] = "  "
    if isCheck(brd)[0]:
        return False
    brd[7][1] = "wK"
    brd[7][2] = "  "
    if isCheck(brd)[0]:
        return False
    brd[7][0] = "wK"
    brd[7][1] = "  "
    if isCheck(brd)[0]:
        return False
    return True

def blackLong():
    if bL == True or bK == True:
        return False
    if board[0][1]!="  " or board[0][2]!="  " or board[0][3]!="  ":
        return False
    brd = copy.deepcopy(board)
    if isCheck(brd)[0] == True:
        return False
    brd[0][3] = "bK"
    brd[0][4] = "  "
    if isCheck(brd)[0]:
        return False
    brd[0][2] = "bK"
    brd[0][3] = "  "
    if isCheck(brd)[0]:
        return False
    brd[0][1] = "bK"
    brd[0][2] = "  "
    if isCheck(brd)[0]:
        return False
    brd[0][0] = "bK"
    brd[0][1] = "  "
    if isCheck(brd)[0]:
        return False
    return True

def whiteShort():
    if wK or wR:
        return False
    if board[7][5]!="  " or board[7][6]!="  ":
        return False
    brd = copy.deepcopy(board)
    if isCheck(brd)[0]:
        return False
    brd[7][4] = "  "
    brd[7][5] = "wK"
    if isCheck(brd)[0]:
        return False
    brd[7][5] = "  "
    brd[7][6] = "wK"
    if isCheck(brd)[0]:
        return False
    brd[7][6] = "  "
    brd[7][7] = "wK"
    if isCheck(brd)[0]:
        return False
    return True

def blackShort():
    if bK or bR:
        return False
    if board[0][5]!="  " or board[0][6]!="  ":
        return False
    brd = copy.deepcopy(board)
    if isCheck(brd)[0]:
        return False
    brd[0][4] = "  "
    brd[0][5] = "bK"
    if isCheck(brd)[0]:
        return False
    brd[0][5] = "  "
    brd[0][6] = "bK"
    if isCheck(brd)[0]:
        return False
    brd[0][6] = "  "
    brd[0][7] = "bK"
    if isCheck(brd)[0]:
        return False
    return True

def moveRook(pos):
    global turn
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    color = board[pos[0]][pos[1]][0]
    for direction in directions:
        newR, newC = pos[0] + direction[0], pos[1] + direction[1]
        while 0 <= newR <= 7 and 0 <= newC <= 7:
            if board[newR][newC][0] != turn:
                newB = copy.deepcopy(board)
                newB[newR][newC] = board[pos[0]][pos[1]]
                newB[pos[0]][pos[1]] = "  "
                check = isCheck(newB)
                if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
                    moves.append([newR, newC])
            if board[newR][newC] != "  ":
                break
            newR += direction[0]
            newC += direction[1]

    return moves


def moveQueen(pos):
    moves = []
    moves.extend(moveBishop(pos))
    moves.extend(moveRook(pos))
    return moves


def moveKing(pos):
    global turn
    moves = []
    color = board[pos[0]][pos[1]][0]
    for i in [1, -1, 0]:
        for j in [1, -1, 0]:
            if j == 0 and i == 0:
                continue
            newR = pos[0] + i
            newC = pos[1] + j
            if min(newC, newR) >= 0 and max(newC, newR) <= 7 and board[newR][newC][0] != turn:
                newB = copy.deepcopy(board)
                newB[newR][newC] = board[pos[0]][pos[1]]
                newB[pos[0]][pos[1]] = "  "
                check = isCheck(newB)
                if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
                    moves.append([newR, newC])
    if turn == "w":
        if whiteLong():
            moves.append([7,2])
        if whiteShort():
            moves.append([7,6])
    else:
        if blackLong():
            moves.append([0,2])
        if blackShort():
            moves.append([0,6])

    return moves

n = 0

def moveWhitePawn(pos):
    global turn
    global n
    if n == 2:
        sf  = 0
    n+=1
    moves = []
    color = board[pos[0]][pos[1]][0]
    if pos[0] == 6:  # starting row
        newR = 4
        newC = pos[1]
        if board[5][pos[1]] == "  " and board[4][pos[1]] == "  ":
            newB = copy.deepcopy(board)
            newB[newR][newC] = board[pos[0]][pos[1]]
            newB[pos[0]][pos[1]] = "  "
            check = isCheck(newB)
            if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
                moves.append([newR, newC])
    newR = pos[0] - 1
    newC = pos[1]
    if newR >= 0 and board[newR][newC] == "  ":
        newB = copy.deepcopy(board)
        newB[newR][newC] = board[pos[0]][pos[1]]
        newB[pos[0]][pos[1]] = "  "
        check = isCheck(newB)
        if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
            moves.append([newR, newC])

    newR = pos[0] - 1
    newC = pos[1] - 1
    if newR >= 0 and newC >= 0 and board[newR][newC][0] != turn and board[newR][newC]!="  ":
        newB = copy.deepcopy(board)
        newB[newR][newC] = board[pos[0]][pos[1]]
        newB[pos[0]][pos[1]] = "  "
        check = isCheck(newB)
        if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
            moves.append([newR, newC])
    newR = pos[0] - 1
    newC = pos[1] + 1
    if newR >= 0 and newC <= 7 and board[newR][newC][0] != turn and board[newR][newC]!="  ":
        newB = copy.deepcopy(board)
        newB[newR][newC] = board[pos[0]][pos[1]]
        newB[pos[0]][pos[1]] = "  "
        check = isCheck(newB)
        if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
            moves.append([newR, newC])
    if [pos[0],pos[1]-1] == lastPawn:
        newB = copy.deepcopy(board)
        newB[pos[0]][pos[1]] = "  "
        newB[pos[0] - 1][pos[1] - 1] = "wp"
        newB[pos[0]][pos[1] - 1] = "  "
        check = isCheck(newB)
        if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
            moves.append([pos[0]-1,pos[1]-1])
    if [pos[0],pos[1]+1] == lastPawn:
        newB = copy.deepcopy(board)
        newB[pos[0]][pos[1]] = "  "
        newB[pos[0] - 1][pos[1] + 1] = "wp"
        newB[pos[0]][pos[1] + 1] = "  "
        check = isCheck(newB)
        if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
            moves.append([pos[0]-1,pos[1]+1])
    return moves


def moveBlackPawn(pos):
    global turn
    moves = []
    color = board[pos[0]][pos[1]][0]
    if pos[0] == 1:  # starting row
        newR = 3
        newC = pos[1]
        if board[2][pos[1]] == "  " and board[3][pos[1]] == "  ":
            newB = copy.deepcopy(board)
            newB[newR][newC] = board[pos[0]][pos[1]]
            newB[pos[0]][pos[1]] = "  "
            check = isCheck(newB)
            if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
                moves.append([newR, newC])
    newR = pos[0] + 1
    newC = pos[1]
    if newR <= 7 and board[newR][newC] == "  ":
        newB = copy.deepcopy(board)
        newB[newR][newC] = board[pos[0]][pos[1]]
        newB[pos[0]][pos[1]] = "  "
        check = isCheck(newB)
        if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
            moves.append([newR, newC])

    newR = pos[0] + 1
    newC = pos[1] - 1
    if newR <= 7 and newC >= 0 and board[newR][newC][0] != turn and board[newR][newC]!="  ":
        newB = copy.deepcopy(board)
        newB[newR][newC] = board[pos[0]][pos[1]]
        newB[pos[0]][pos[1]] = "  "
        check = isCheck(newB)
        if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
            moves.append([newR, newC])
    newR = pos[0] + 1
    newC = pos[1] + 1
    if newR >= 0 and newC <= 7 and board[newR][newC][0] != turn and board[newR][newC]!="  ":
        newB = copy.deepcopy(board)
        newB[newR][newC] = board[pos[0]][pos[1]]
        newB[pos[0]][pos[1]] = "  "
        check = isCheck(newB)
        if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
            moves.append([newR, newC])
    if [pos[0],pos[1]-1] == lastPawn:
        newB = copy.deepcopy(board)
        newB[pos[0]][pos[1]] = "  "
        newB[pos[0]+1][pos[1]-1] = "bp"
        newB[pos[0]][pos[1]-1] = "  "
        check = isCheck(newB)
        if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
            moves.append([pos[0]+1,pos[1]-1])
    if [pos[0],pos[1]+1] == lastPawn:
        newB = copy.deepcopy(board)
        newB[pos[0]][pos[1]] = "  "
        newB[pos[0] + 1][pos[1] + 1] = "bp"
        newB[pos[0]][pos[1] + 1] = "  "
        check = isCheck(newB)
        if (color == "w" and check[0] == False) or (color == "b" and check[1] == False):
            moves.append([pos[0]+1,pos[1]+1])
    return moves


app = Flask(__name__)


@app.route('/')
def chess_board():
    return render_template('chess.html')


@app.route('/square', methods=['POST'])
def handle_square():
    global board
    global prevClick
    global prevPos
    global turn
    global wK
    global wL
    global wR
    global bK
    global bR
    global promote
    global promoteCol
    global bL
    global lastPawn
    global promotePawn
    square = request.form['square']
    row = 8 - int(square[0])
    col = ord(square[2]) - ord("a")
    if promote == 1: #white promote
        prevClick = [-1,-1]
        if col == promoteCol and row == 0:
            board[0][promoteCol] = "wq"
            board[promotePawn[0]][promotePawn[1]] = "  "
            promote = 0
            promoteCol = -1
            if turn == "w":
                turn = "b"
            else:
                turn = "w"
            return "pro wq "+str(col)+" "+str(promotePawn[1]) # promote to white queen, queen as pos of (0,col) and erase old pawn at (1,promotePawn[1])
        elif col == promoteCol and row == 1:
            board[0][promoteCol] = "wr"
            board[promotePawn[0]][promotePawn[1]] = "  "
            promote = 0
            promoteCol = -1
            if turn == "w":
                turn = "b"
            else:
                turn = "w"
            return "pro wr " + str(col) + " " + str(promotePawn[1])
        elif col == promoteCol and row == 2:
            board[0][promoteCol] = "wb"
            board[promotePawn[0]][promotePawn[1]] = "  "
            promote = 0
            promoteCol = -1
            if turn == "w":
                turn = "b"
            else:
                turn = "w"
            return "pro wb " + str(col) + " " + str(promotePawn[1])
        elif col == promoteCol and row == 3:
            board[0][promoteCol] = "wk"
            board[promotePawn[0]][promotePawn[1]] = "  "
            promote = 0
            promoteCol = -1
            if turn == "w":
                turn = "b"
            else:
                turn = "w"
            return "pro wk " + str(col) + " " + str(promotePawn[1])
        else:
            promote = 0
            temp = promoteCol
            promoteCol = -1
            promotePawn = [-1, -1]
            return "res w"+str(temp) #restore white
            # note to self: right now when the pawn kills a piece while promoting, we can not resotre it, probably change the code at bottom so we don't actually take a peice when first promoting
    if promote == 2:  # black promote
        prevClick = [-1, -1]
        if col == promoteCol and row == 7:
            board[7][promoteCol] = "bq"
            board[promotePawn[0]][promotePawn[1]] = "  "
            promote = 0
            promoteCol = -1
            if turn == "w":
                turn = "b"
            else:
                turn = "w"
            return "pro bq " + str(col) + " " + str(promotePawn[
                                                        1])  # promote to white queen, queen as pos of (0,col) and erase old pawn at (1,promotePawn[1])
        elif col == promoteCol and row == 6:
            board[7][promoteCol] = "br"
            board[promotePawn[0]][promotePawn[1]] = "  "
            promote = 0
            promoteCol = -1
            if turn == "w":
                turn = "b"
            else:
                turn = "w"
            return "pro br " + str(col) + " " + str(promotePawn[1])
        elif col == promoteCol and row == 5:
            board[7][promoteCol] = "bb"
            board[promotePawn[0]][promotePawn[1]] = "  "
            promote = 0
            promoteCol = -1
            if turn == "w":
                turn = "b"
            else:
                turn = "w"
            return "pro bb " + str(col) + " " + str(promotePawn[1])
        elif col == promoteCol and row == 4:
            board[7][promoteCol] = "bk"
            board[promotePawn[0]][promotePawn[1]] = "  "
            promote = 0
            promoteCol = -1
            if turn == "w":
                turn = "b"
            else:
                turn = "w"
            return "pro bk " + str(col) + " " + str(promotePawn[1])
        else:
            promote = 0
            temp = promoteCol
            promoteCol = -1
            promotePawn = [-1, -1]
            return "res b" + str(temp)  # restore white
    elif board[row][col][0] == turn:
        prevClick = [row, col]
        moves = []
        piece = board[row][col]
        if piece[1] == "r":
            moves = moveRook(prevClick)
        elif piece[1] == "b":
            moves = moveBishop(prevClick)
        elif piece[1] == "k":
            moves = moveKnight(prevClick)
        elif piece == "bp":
            moves = moveBlackPawn(prevClick)
        elif piece == "wp":
            moves = moveWhitePawn(prevClick)
        elif piece[1] == "K":
            moves = moveKing(prevClick)
        elif piece[1] == "q":
            moves = moveQueen(prevClick)
        res = "0"
        for i in moves:
            res = res+" "+str(i[0])+str(i[1])
        prevPos = moves
        return res
    elif prevClick!=[-1,-1] and (board[row][col] == "  " or board[row][col][0]!= turn):
        if [row,col] in prevPos:
            if board[prevClick[0]][prevClick[1]] == "wK":
                wK = True
            elif board[prevClick[0]][prevClick[1]] == "bK":
                bK = True
            elif prevClick == [7,0] and board[prevClick[0]][prevClick[1]] == "wr":
                wL = True
            elif prevClick == [7,7] and board[prevClick[0]][prevClick[1]] == "wr":
                wR = True
            elif prevClick == [0,0] and board[prevClick[0]][prevClick[1]] == "br":
                bL = True
            elif prevClick == [0,7] and board[prevClick[0]][prevClick[1]] == "br":
                bR = True
            if board[prevClick[0]][prevClick[1]][1] == "p" and abs(row-prevClick[0]) == 2:
                lastPawn = [row,col]
            else:
                lastPawn = [-1,-1]
            res = str(prevClick[0])+str(prevClick[1])+" "+str(row)+str(col)
            if board[prevClick[0]][prevClick[1]] == "wp" and board[row][col] == "  " and col!=prevClick[1]:
                res = str(prevClick[0])+str(prevClick[1])+" "+str(row)+str(col)+"we"
            if board[prevClick[0]][prevClick[1]] == "bp" and board[row][col] == "  " and col != prevClick[1]:
                res = str(prevClick[0])+str(prevClick[1])+" "+str(row)+str(col)+"be"
            if board[prevClick[0]][prevClick[1]] == 'wp' and prevClick[0] == 1:
                promote = 1 # we want the user to choose piece next click
                promoteCol = col
                res = str(col)+"wp"
                promotePawn = prevClick
                return res
            if board[prevClick[0]][prevClick[1]] == "bp" and prevClick[0] == 6:
                promoteCol = col
                promote = 2
                res = str(col)+"bp"
                promotePawn = prevClick
                return res
            board[row][col] = board[prevClick[0]][prevClick[1]]
            board[prevClick[0]][prevClick[1]] = "  "
            if prevClick[0] == 7 and prevClick[1] == 4 and row == 7 and col == 6: #white short
                res = "1"
                board[7][7] = "  "
                board[7][5] = "wr"
            elif prevClick[0] == 7 and prevClick[1] == 4 and row == 7 and col == 2: # white long
                res = "2"
                board[7][0] = "  "
                board[7][3] = "wr"
            elif prevClick[0] == 0 and prevClick[1] == 4 and row == 0 and col == 6: #black short
                res = "3"
                board[0][7] = "  "
                board[0][5] = "br"
            elif prevClick[0] == 0 and prevClick[1] == 4 and row == 0 and col == 2:#black long
                res = "4"
                board[0][0] = "  "
                board[0][5] = "br"

            prevClick = [-1,-1]
            prevPos.clear()
            if not promote:
                if turn == "w":
                    turn = "b"
                else:
                    turn = "w"
            return "1 "+res

if __name__ == '__main__':
    app.run()


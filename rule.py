from abc import ABC, abstractmethod
from copy import deepcopy
import csv
import os

# count score at the bottom half of the chess board
bottomHalfPosition = {'xe':[], 'ma':[], 'vo':[], 'si':[], 'tu':[], 'ph':[], 'ch':[]}
for i in bottomHalfPosition.keys():
    name = i+'.csv'
    with open(os.path.join(os.path.dirname(__file__), 'unity', name), 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for r in range(len(row)):
                row[r] = float(row[r])
            bottomHalfPosition[i] += [row]

startPower = {'xe':90, 'ma':40, 'vo':25, 'si':30, 'tu':9000, 'ph':45, 'ch':10}  # power of chess Man at the start of the game
midPower = {'xe':90, 'ma':40, 'vo':25, 'si':30, 'tu':9000, 'ph':50, 'ch':20}  # power of chess Man at the middle of the game
endPower = {'xe':100, 'ma':50, 'vo':40, 'si':40, 'tu':9000, 'ph':40, 'ch':25}   #  power of chess Man at the end of the game

# count score at the upper half of the chess board
upperHalfPosition = {'xe':[], 'ma':[], 'vo':[], 'si':[], 'tu':[], 'ph':[], 'ch':[]}
for i in bottomHalfPosition.keys():
    upperHalfPosition[i] = bottomHalfPosition[i][::-1]


# this is the class that return list of valid move of CAR (XE)
def chariotValidMoveList(board, position, redIsMachine):
    valideMoveList =[]
    chessSide = board[position[0]][position[1]][0]
    row = position[0]
    col = position[1]

    for x in range(row + 1,10):
        if board[x][col] == '---':
            valideMoveList += [(x,col)]
        
        elif board[x][col][0] != chessSide:
            valideMoveList += [(x,col)]
            break
        else: break
    for x in range(row-1 ,-1, -1):
        if board[x][col] == '---':
            valideMoveList += [(x,col)]
        elif board[x][col][0] != chessSide:
            valideMoveList += [(x,col)]
            break
        else: break
    for y in range(col + 1,9):
        if board[row][y] =='---':
            valideMoveList += [(row, y)]
        elif board[row][y][0] != chessSide:
            valideMoveList += [(row, y)]
            break
        else: break
    for y in range(col-1,-1,-1):
        if board[row][y] =='---':
            valideMoveList += [(row,y)]
        elif board[row][y][0] != chessSide:
            valideMoveList += [(row,y)]
            break
        else: break
    return valideMoveList

# this is the class that return list of valid move of HORSE (MA)
def horseValidMoveList(board, position, redIsMachine):
    validMoveList =[]
    chessSide = board[position[0]][position[1]][0] # Chess side are black or red
    row = position[0]
    col = position[1]
    if col + 1 < 9:
        if board[row][col  +1] == '---':
            if col + 2 < 9 and row + 1 < 10 and (board[row + 1][col + 2] == '---' or board[row + 1][col + 2][0] != chessSide):
                validMoveList += [(row+1,col+2)]
            if col + 2 < 9 and row - 1 >= 0 and (board[row-1][col+2] == '---' or board[row-1][col+2][0] != chessSide):
                validMoveList += [(row-1,col+2)]
    if col - 1 >=0:
        if board[row][col-1] == '---':
            if col - 2 >= 0 and row + 1 < 10 and (board[row+1][col-2] == '---' or board[row+1][col-2][0] != chessSide):
                validMoveList += [(row+1,col-2)]

            if col - 2 >= 0 and row - 1 >= 0 and (board[row-1][col-2] == '---' or board[row-1][col-2][0] != chessSide):
                validMoveList += [(row-1,col-2)]
    if row + 1 < 10:
        if board[row + 1][col] == '---':
            if col + 1 < 9 and row + 2 < 10 and (board[row+2][col+1] == '---' or board[row+2][col+1][0] != chessSide):
                validMoveList += [(row+2,col+1)]

            if col - 1 >= 0 and row + 2 < 10 and (board[row+2][col-1] == '---' or board[row+2][col-1][0] != chessSide):
                validMoveList += [(row+2,col-1)]
    if row - 1 >=0:
        if board[row-1][col] == '---':
            if col + 1 < 9 and row - 2 >= 0 and (board[row-2][col+1] == '---' or board[row-2][col+1][0] != chessSide):
                validMoveList += [(row-2,col+1)]
            if col - 1 >= 0 and row - 2 >= 0 and (board[row-2][col-1] == '---' or board[row-2][col-1][0] != chessSide):
                validMoveList += [(row-2,col-1)]
    return validMoveList

# this is the class that return list of valid move of ELEPHANT (TƯỢNG)
def elephantValidMoveList(board, position, redIsMachine):
    validMoveList = []
    chessSide = board[position[0]][position[1]][0]
    row = position[0]
    col = position[1]
    candidateMoveList = [(row+2,col+2),(row+2,col-2),(row-2,col+2),(row-2,col-2)]
    if not redIsMachine:
        if chessSide == 'b':
            for x in candidateMoveList:
                if 0 <= x[0] < 5 and 0 <= x[1] < 10:
                    if board[int((row+x[0])/2)][int((col+x[1])/2)] =='---' and board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 4<x[0]<10 and 0<=x[1]<10:
                    if board[int((row+x[0])/2)][int((col+x[1])/2)] =='---' and board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    else:
        if chessSide == 'b':
            for x in candidateMoveList:
                if 5<=x[0]<10 and 0<=x[1]<10:
                    if board[int((row+x[0])/2)][int((col+x[1])/2)] =='---' and board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 0<=x[0]<6 and 0<=x[1]<10:
                    if board[int((row+x[0])/2)][int((col+x[1])/2)] =='---' and board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    return validMoveList

# this is the class that return list of valid move of ADVISOR (SI)
def advisorValidMoveList(board, position, redIsMachine):
    validMoveList=[]
    row = position[0]
    col = position[1]
    chessSide = board[position[0]][position[1]][0]
    candidateMoveList = [(row+1,col+1),(row+1,col-1),(row-1,col+1),(row-1,col-1)]
    if not redIsMachine:
        if chessSide == 'b':
            for x in candidateMoveList:
                if 0<=x[0]<3 and 3<=x[1]<6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            
            for x in candidateMoveList:
                if 7<=x[0]<10 and 3<=x[1]<6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    else:
        if chessSide == 'b':
            for x in candidateMoveList:
                if 7<=x[0]<10 and 3<=x[1]<6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 0<=x[0]<3 and 3<=x[1]<6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    return validMoveList


# this is the class that return list of valid move of KING (Tướng)
def kingValidMoveList(board, position, redIsMachine):
    validMoveList=[]
    row = position[0]
    col = position[1]
    chessSide = board[position[0]][position[1]][0]
    candidateMoveList = [(row+1,col),(row,col+1),(row,col-1),(row-1,col)]
    if not redIsMachine:
        if chessSide == 'b':
            for x in candidateMoveList:
                if 0<=x[0]<3 and 3<=x[1]<6: # Row from 0 to 3, Col from 3 to 5
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 7<=x[0]<10 and 3<=x[1]<6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    else:
        if chessSide == 'b':
            for x in candidateMoveList:
                if 7<=x[0]<10 and 3<=x[1]<6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 0<=x[0]<3 and 3<=x[1]<6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    return validMoveList    


# this is the class that return list of valid move of CANON (PHAO)
def cannonValidMoveList(board, position, redIsMachine):
    validMoveList=[]
    row = position[0]
    j = position[1]
    chessSide = board[position[0]][position[1]][0]
    for x in range(row + 1, 10):
        if board[x][j] == '---':
            validMoveList += [(x,j)]
        else: #meet the stone
            for y in range(x +1,10):
                if board[y][j][0] != chessSide and board[y][j] != '---':
                    validMoveList += [(y,j)]
                    break
                if board[y][j][0] == chessSide:
                    break
            break
    for x in range(row-1,-1,-1):
        if board[x][j] == '---' :
            validMoveList += [(x,j)]
        else: 
            for y in range(x-1,-1,-1):
                if board[y][j][0] != chessSide and board[y][j] != '---':
                    validMoveList += [(y,j)]
                    break
                if board[y][j][0] == chessSide:
                    break
            break
    for y in range(j+1,9):
        if board[row][y] =='---' :
            validMoveList += [(row,y)]
        else:
            for x in range(y+1,9):
                if board[row][x][0] != chessSide and board[row][x] != '---':
                    validMoveList += [(row,x)]
                    break
                if board[row][x][0] == chessSide:
                    break
            break
    for y in range(j-1,-1,-1):
        if board[row][y] =='---' :
            validMoveList += [(row,y)]
        else: 
            for x in range(y-1,-1,-1):
                if board[row][x][0] != chessSide and board[row][x] != '---':
                    validMoveList += [(row,x)]
                    break
                if board[row][x][0] == chessSide:
                    break
            break
    return validMoveList


# this is the class that return list of valid move of SOLDIER (TOT)
def soldierValidMoveList(board,position,redIsMachine):
    validMoveList=[]
    row = position[0]
    col = position[1]
    chessSide = board[position[0]][position[1]][0]
    
    if not redIsMachine:
        if chessSide =='b':
            candidate =[(row+1,col)]
            if row > 4:
                candidate += [(row,col+1),(row,col-1)]
            for x in candidate:
                if 0<=x[0]<10 and 0<=x[1]<9:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]                     #[(),(),(),()]
        else:
            candidate = [(row-1,col)]
            if row<5:
                candidate += [(row,col+1),(row,col-1)]
            for x in candidate:
                if 0<=x[0]<10 and 0<=x[1]<9:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    else:
        if chessSide =='b':
            candidate =[(row-1,col)]
            if row < 5:
                candidate += [(row,col+1),(row,col-1)]
            for x in candidate:
                if 0<=x[0]<10 and 0<=x[1]<9:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            candidate = [(row+1,col)]
            if row>4:
                candidate += [(row,col+1),(row,col-1)]
            for x in candidate:
                if 0<=x[0]<10 and 0<=x[1]<9:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    return validMoveList


# valid move list of two tuple [[(),()],...]
def moveRule(board, position, redIsMachine):  #(), redIsMachine is after
    chessPiece = board[position[0]][position[1]][1:]
    validMoveList = []
    if chessPiece == 'xe':
        validMoveList = chariotValidMoveList(board, position, redIsMachine)
    elif chessPiece == 'ma':
        validMoveList = horseValidMoveList(board, position, redIsMachine)
    elif chessPiece == 'ph':
        validMoveList = cannonValidMoveList(board, position, redIsMachine)
    elif chessPiece == 'tu':
        validMoveList = kingValidMoveList(board, position, redIsMachine)
    elif chessPiece == 'si':
        validMoveList = advisorValidMoveList(board, position, redIsMachine)
    elif chessPiece == 'ch':
        validMoveList = soldierValidMoveList(board, position, redIsMachine)
    elif chessPiece == 'vo':
        validMoveList = elephantValidMoveList(board, position, redIsMachine)
    return validMoveList
 
# function that return list of valid move with some rules of this game 
def moveCheckValid(board, redTurn, redIsMachine):
    kingBeThreaten = False
    blackKing = ()
    redKing = ()
    
    for i in range(0,3):
        for j in range(3,6):
            if board[i][j][1:] == 'tu':
                blackKing= (i,j) 
    for i in range(7,10):
        for j in range(3,6):
            if board[i][j][1:] == 'tu':
                redKing = (i,j)
    if redIsMachine:
        blackKing, redKing = redKing, blackKing
    if blackKing[1] == redKing[1]:
        for i in range(blackKing[0]+1,redKing[0]+1):
            if board[i][blackKing[1]] == '---':
                continue
            elif board[i][blackKing[1]][1:] == 'tu':
                kingBeThreaten = True
                break
            else:
                break
        if kingBeThreaten:
            return False
    if isKingBeThreaten(board, blackKing, redKing, not redTurn, redIsMachine):
        return False
    return True
    # check it later

# this is the function check if the king is threatened
def isKingBeThreaten(board, blackKing, redKing, redTurn, redIsMachine):
    # turn of red, so check if the red king is threatened
    x = blackKing[0]
    y = blackKing[1]
    chessSide = 'b' 
    
    if not redTurn:
        x = redKing[0]
        y = redKing[1]
        chessSide = 'r' 
    # check if a horse is threatening the king
    horsePositionList =[]
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == 'ma' and board[row][col][0] != chessSide:
                horsePositionList += [(row,col)]
    if horsePositionList != []:
        candidateKingThreatenList = [(x+1,y+2),(x+1,y-2),(x-1,y+2),(x-1,y-2),(x+2,y+1),(x+2,y-1),(x-2,y+1),(x-2,y-1)]
        for i in horsePositionList:
            if i in candidateKingThreatenList:
                validHorseThreatList = horseValidMoveList(board, (i[0],i[1]), redIsMachine)
                if (x,y) in validHorseThreatList:
                    return True
    # check if a car is threatening the king
    carPositionList = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == 'xe' and board[row][col][0] != chessSide:
                carPositionList += [(row,col)]
    if carPositionList != []:
        for i in carPositionList:
            if i[0] == x:
                if i[1] < y:
                    for j in range(i[1], y):
                        if j == y - 1:
                            # print("The king is threatened by a car")
                            return True
                        if board[x][j + 1] != "---":
                            break
                if i[1] > y:
                    for j in range(y, i[1]):
                        if j == i[1] - 1:
                            # print("The king is threatened by a car")
                            return True
                        if board[x][j + 1] != "---":
                            break
            if i[1] == y:
                if i[0] < x:
                    for j in range(i[0], x):
                        if j == x - 1:
                            # print("The king is threatened by a car")
                            return True
                        if board[j + 1][y] != "---":
                            break
                if i[0] > x:
                    for j in range(x, i[0]):
                        if j == i[0] - 1:
                            # print("The king is threatened by a car")
                            return True
                        if board[j + 1][y] != "---":
                            break

    # check if a king is theatening by a canon
    canonPositionList = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == 'ph' and board[row][col][0] != chessSide:
                canonPositionList += [(row,col)]
    if canonPositionList != []:
        stayaway = [(x,y),(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        candidateKingThreatenList = [(a,y) for a in range(10) if (a,y) not in stayaway ] + [(x,b) for b in range(9) if (x,b) not in stayaway ]

        for i in canonPositionList:
            if i in candidateKingThreatenList:
                validCanonThreatList = cannonValidMoveList(board, i, redIsMachine)
                if (x,y) in validCanonThreatList:
                    #print("The king is threatened by a canon")
                    return True
    # check if a king is threatened by a soldier
    soldierPostionList = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == 'ch' and board[row][col][0] != chessSide:
                soldierPostionList += [(row,col)]
    if soldierPostionList != []:
        candidateKingThreatenList = [(x,y+1),(x,y-1)] + ([(x-1,y)] if chessSide == 'r' else [(x+1,y)])
        for i in soldierPostionList:
            if i in candidateKingThreatenList:
                validSoldierThreatList = soldierValidMoveList(board, i, redIsMachine)
                if (x,y) in validSoldierThreatList:
                    ##print("The king is threatened by a soldier")
                    return True
    return False

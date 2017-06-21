#!/usr/bin/env python 
import datetime
import curses 
import time
import signal
import sys

word = R"""
 _______   ____    _______  _______  _   ___  _______  ___      _______   _____   _______    ___      
|  _    | /    |  |       ||       || | |   ||       ||   |    |       | |  _  | |  _    |  |   |     
| | |   |  |   |  |____   ||___    || |_|   ||   ____||   |___ |___    | | |_| | | | |   |  |___|    
| | |   |  |   |   ____|  | ___|   ||       ||  |____ |    _  |    |   ||   _   || |_|   |   ___     
| |_|   |  |   |  | ______||___    ||___    ||_____  ||   | | |    |   ||  | |  ||___    |  |   |    
|       ||       || |_____  ___|   |    |   | _____| ||   |_| |    |   ||  |_|  |    |   |  |___|    
|_______||_______||_______||_______|    |___||_______||_______|    |___||_______|    |___|           """

myscreen = curses.initscr()
def printMatrix(matrix):
    for i in range(len(matrix)):
        string = "".join(matrix[i])
        # print("".join(i))
        myscreen.addstr(i, 10, string + "             ")
    myscreen.refresh()


def getWordMatrix():
    nummap = {}
    wordbyline = word.split("\n")[1:]
    wordstr = "0123456789:"
    for index in range(len(wordstr)):
        a = wordstr[index]
        nummap[a] = [[" " for m in range(9)] for n in range(7)] 
        for i in range(7):
            for j in range(9):
                nummap[a][i][j] = wordbyline[i][(index-0)*9 + j]
    return nummap

# ttt: 0 - 9
def getTrans(scur, snext, ttt):
    transition1 = " _-\|/"
    transition2 = "\|/-_ "
    if snext != " ":
        transition = transition1
    else:
        transition = transition2
    if scur == snext:
        return scur
    curindex = transition.index(scur, 0)
    nextindex = transition.index(snext, 0)
    if nextindex >= curindex:
        transition = transition[curindex:nextindex]
    else:
        transition = transition[curindex:] + transition[:nextindex]
    indextransition = len(transition) - 1
    index = ttt * (float(indextransition)/9)
    return transition[int(index)]

def printTime():
    nummap = getWordMatrix()
    now = datetime.datetime.now()
    timenow = '{0:02d}:{1:02d}:{2:02d}'.format(now.hour, now.minute, now.second)
    timelist = []
    timematrix = []
    for t in list(timenow):
        timelist.append(nummap[t])
    for i in range(7):
        line = []
        for alist in timelist:
            line.extend(alist[i])
        timematrix.append(line)
    printMatrix(timematrix)

def printMatrixTrans(matrixnow, matrixnext, now):
    ttt = int(now.microsecond/100000) 
    for i in range(len(matrixnow)):
        res = []
        for j in range(len(matrixnow[i])):
            res.append(getTrans(matrixnow[i][j], matrixnext[i][j], ttt))
        string = "".join(res)
        myscreen.addstr(i, 10, string + "             ")
    myscreen.refresh()

def printTime2():
    nummap = getWordMatrix()
    now = datetime.datetime.now()
    timenow = '{0:02d}:{1:02d}:{2:02d}'.format(now.hour, now.minute, now.second)
    nexsecond = now.second+1 if now.second<60 else 0
    timenext = '{0:02d}:{1:02d}:{2:02d}'.format(now.hour, now.minute, nexsecond)
    timelist = []
    timematrix = []
    for t in list(timenow):
        timelist.append(nummap[t])
    for i in range(7):
        line = []
        for alist in timelist:
            line.extend(alist[i])
        timematrix.append(line)
    timelist2 = []
    timematrix2 = []
    for t in list(timenext):
        timelist2.append(nummap[t])
    for i in range(7):
        line = []
        for alist in timelist2:
            line.extend(alist[i])
        timematrix2.append(line)
    printMatrixTrans(timematrix, timematrix2, now)

def clock():
    while True:
        time.sleep(0.1)
        printTime2()

if __name__ == "__main__":
    def signal_handler(signal, frame):
        curses.endwin()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    clock()





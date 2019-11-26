file = open('./auth.log', 'r')

attackerDict = {}

while True:
    curLine = file.readline()
    if curLine == '':
        break
    lineArr = curLine.split(' ')
    if lineArr[5] == 'Failed':
        curMonth = lineArr[0]
        curDay = lineArr[1]
        curTime = lineArr[2]
        targetUser = lineArr[8]
        fromIdx = 0
        
        if targetUser == 'root':
            attackerIP = lineArr[10]
        else:
            targetUser = lineArr[10]
            attackerIP = lineArr[12]
            

        if attackerIP in attackerDict:
            attackerDict[attackerIP] += 1
        else:
            attackerDict[attackerIP] = 1

for k in sorted(attackerDict,key=attackerDict.__getitem__):
    print(k, attackerDict[k])
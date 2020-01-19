import time
import os
import sys

sudoPassword = sys.argv[1]

# ========= get history ===========
attackerDictOld = {}
fileOld = open('totalData', 'r')
oldTime = float(fileOld.readline())

while True:
    curLine = fileOld.readline().strip('\n')
    if curLine == '':
        break
    lineArr = curLine.split(' ')
    # print(lineArr)
    attackerDictOld[lineArr[0]] = int(lineArr[1])

fileOld.close()

# ========================================



# ================== parse auth.log ==============================
attackerDict = {}
validDict = {}
curTime = 0.0

fileRaw = open('./auth.log', 'r')

while True:
    curLine = fileRaw.readline()
    if curLine == '':
        break
    
    lineArr = curLine.split(' ')

    # print(time.strptime(lineArr[0]+' '+lineArr[1]+' '+lineArr[2]+' 2020',"%b %d %H:%M:%S %Y"))
    curTime = time.mktime(time.strptime(lineArr[0]+' '+lineArr[1]+' '+lineArr[2]+' 2020',"%b %d %H:%M:%S %Y"))
    # print(time.mktime(time.strptime(lineArr[0]+' '+lineArr[1]+' '+lineArr[2],"%b %d %H:%M:%S")))

    if curTime <= oldTime:
        continue
    
    if 'Failed password' in curLine:
        fromIdx = lineArr.index('from')
        attackerIP = lineArr[fromIdx+1]
        if attackerIP in attackerDict:
            attackerDict[attackerIP] += 1
        else:
            attackerDict[attackerIP] = 1
    elif 'Accepted password' in curLine:
        fromIdx = lineArr.index('from')
        validIP = lineArr[fromIdx+1]
        if validIP in validDict:
            validDict[validIP] += 1
        else:
            validDict[validIP] = 1

fileRaw.close()

if curTime < oldTime:
    curTime = oldTime
# =================================================================================

# ========================== exclude accepted ip ================================
for k in validDict:
    if k in attackerDict:
        del attackerDict[k]
# ===============================================================================

# ===================== get new block target ======================
newBlock = []

for k in attackerDict:
    curCnt = attackerDict[k]    # new fail cnt
    if k in attackerDictOld:    # old fail cnt
        curCnt += attackerDictOld[k]
        if attackerDictOld[k] >= 10:    # should already blocked
            print('error: '+k)
    if (curCnt >= 10) and ((k not in attackerDictOld) or (attackerDictOld[k] < 10)):    # should block this time
        newBlock.append(k)
    attackerDictOld[k] = curCnt # update old

# =============================================================================

# ====================== block target ========================
for i in newBlock:
    print(i)
    os.system('echo %s|sudo -S ufw insert 1 deny from %s' % (sudoPassword, i)) 
    

# ==============================================================================


fileTotal = open('totalData', 'w')
fileTotal.write(str(curTime)+'\n')
for k in attackerDictOld:
    fileTotal.write(k+' '+str(attackerDictOld[k])+'\n')

print(attackerDict)
print(attackerDictOld)
# print(validDict)
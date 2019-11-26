import matplotlib.pyplot as plt
from pyecharts.charts import Bar
from pyecharts import options as opts
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
        fromIdx = lineArr.index('from')
        targetUser = lineArr[fromIdx-1]
        attackerIP = lineArr[fromIdx+1]

        # if targetUser == 'root':
        #     attackerIP = lineArr[10]
        # else:
        #     targetUser = lineArr[10]
        #     attackerIP = lineArr[12]
            

        if attackerIP in attackerDict:
            attackerDict[attackerIP] += 1
        else:
            attackerDict[attackerIP] = 1

# attackerDictSorted = sorted(attackerDict,key=attackerDict.__getitem__,reverse=True)


# plt.bar(range(len(attackerDict.values())), attackerDict.values(), color='rgb')
# plt.show()

# bar = (
#     Bar()
#     .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
#     .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
#     .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
#     .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
# )
# bar.render()

attacker = []
attacknum = []

for k in sorted(attackerDict,key=attackerDict.__getitem__,reverse=True):
    attacker.append(k)
    attacknum.append(attackerDict[k])

print('ss')

bar = (
    Bar()
    .add_xaxis(attacker)
    .add_yaxis("攻击者", attacknum)
    .set_global_opts(title_opts=opts.TitleOpts(title="攻击情况"))
)
bar.render()
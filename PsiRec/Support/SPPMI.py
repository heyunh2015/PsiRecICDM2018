import numpy as np

def calculatePMIfromWalks(walks, windowSizePre, walkLength, userNum, itemNum):
    matrix = np.zeros((userNum, itemNum))
    userList = np.zeros(userNum)
    itemList = np.zeros(itemNum)

    count = 0
    for walk in walks:
        count += 1
        if count%10000==0:
            print count
        walkLength = len(walk)
        for index in range(walkLength):
            windowSize = windowSizePre
            if index - windowSize >= 0:
                preList = walk[index - windowSize: index]
                currentNode = walk[index]
                nextList = walk[index + 1: index + windowSize + 1]
            else:
                preList = walk[0: index]
                currentNode = walk[index]
                nextList = walk[index + 1: index + windowSize + 1]

            preListNum = len(preList)
            nextListNum = len(nextList)

            if currentNode >= 1000000:
                itemList[currentNode-1000000] += 1
                if preListNum > 0:
                    for nodeIndex in range(0, preListNum):
                        otherNode = preList[nodeIndex]
                        if otherNode < 1000000:
                            matrix[otherNode-1, currentNode-1000000] += 1

                if nextListNum > 0:
                    for nodeIndex in range(0, nextListNum):
                        otherNode = nextList[nodeIndex]
                        if otherNode < 1000000:
                            matrix[otherNode - 1, currentNode - 1000000] += 1
            else:
                userList[currentNode-1] += 1
    k=3
    corpusSize = len(walks)*walkLength
    for userId in range(userNum):
       for itemId in range(itemNum):
            pmi = matrix[userId][itemId]*corpusSize/(userList[userId]*itemList[itemId]*k)#*1.0/itemList[itemId]
            if pmi>1:
                pmi = np.log(pmi)
            else:
                pmi=0
            matrix[userId][itemId] = pmi

    return matrix
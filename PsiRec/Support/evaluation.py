import operator

def loadGroundTruth(testFile):
    fp = open(testFile)
    lines = fp.readlines()
    groundTruthDict = {}
    userRecllDict = {}
    for line in lines:
        lineStr = line.strip().split('\t')
        groundTruthDict[str(int(lineStr[0])-1)+'-'+str(int(lineStr[1])-1000000)] = 1
        if int(lineStr[0])-1 not in userRecllDict:
            userRecllDict[int(lineStr[0])-1] = 1
        else:
            userRecllDict[int(lineStr[0])-1] += 1
    #for item in groundTruthDict:
     #   print item
    return groundTruthDict, userRecllDict

def loadTrainDict(trainFile):
    fp = open(trainFile)
    lines = fp.readlines()
    trainDict = {}
    for line in lines:
        lineStr = line.strip().split('\t')
        trainDict[str(int(lineStr[0])-1)+'-'+str(int(lineStr[1])-1000000)] = 1
    #for item in trainDict:
     #   print item
    return trainDict

def test_model_all(prediction, trainDataFile, testDataFile):
    groundTruthDict, userRecallDict = loadGroundTruth(testDataFile)
    trainDict = loadTrainDict(trainDataFile)

    userNum = prediction.shape[0]
    itemNum = prediction.shape[1]
    totalprecision50 = 0
    totalrecall50 = 0
    totalprecision100 = 0
    totalrecall100 = 0
    totalprecision20 = 0
    totalrecall20 = 0
    totalprecision10 = 0
    totalrecall10 = 0
    totalprecision5 = 0
    totalrecall5 = 0
    totalprecision1 = 0
    totalrecall1 = 0
    count = 0
    for userIndex in range(userNum):
        if count%1000==0:
            print count
        count+=1
        userTopDict = {}
        scores = prediction[userIndex]
        maxScore = max(scores)

        for itemIndex in range(itemNum):
            score = scores[itemIndex]
            #print score/maxScore
            if score/maxScore > 0.00001:#
                userTopDict[itemIndex] = score

        userTopDictNoTrain = {}
        for itemIndex in userTopDict:
            pairId = str(userIndex) + '-' + str(itemIndex)
            if pairId not in trainDict:
                userTopDictNoTrain[itemIndex] = userTopDict[itemIndex]

        #print len(userTopDictNoTrain)
        if len(userTopDictNoTrain)<100:
            print 'oooooops!'
        sorted_x = sorted(userTopDictNoTrain.items(), key=operator.itemgetter(1), reverse=True)


        precision50, recall50 = precisionAndRecall(sorted_x, 50, userIndex, groundTruthDict, userRecallDict)
        precision100, recall100 = precisionAndRecall(sorted_x, 100, userIndex, groundTruthDict, userRecallDict)
        precision20, recall20 = precisionAndRecall(sorted_x, 20, userIndex, groundTruthDict,
                                                   userRecallDict)
        precision10, recall10 = precisionAndRecall(sorted_x, 10, userIndex, groundTruthDict,
                                                   userRecallDict)
        precision5, recall5 = precisionAndRecall(sorted_x, 5, userIndex, groundTruthDict,
                                                   userRecallDict)

        precision1, recall1 = precisionAndRecall(sorted_x, 1, userIndex, groundTruthDict,
                                                 userRecallDict)

        totalprecision50 += precision50
        totalrecall50 += recall50
        totalprecision100 += precision100
        totalrecall100 += recall100
        totalprecision20 += precision20
        totalrecall20 += recall20
        totalprecision10 += precision10
        totalrecall10 += recall10
        totalprecision5 += precision5
        totalrecall5 += recall5
        totalprecision1 += precision1
        totalrecall1 += recall1

    print 'precision@1:', totalprecision1 / userNum
    print 'recall@1:', totalrecall1 / userNum
    print 'precision@5:', totalprecision5 / userNum
    print 'recall@5:', totalrecall5 / userNum
    print 'precision@10:', totalprecision10/userNum
    print 'recall@10:', totalrecall10/userNum
    print 'precision@20:', totalprecision20 / userNum
    print 'recall@20:', totalrecall20 / userNum
    print 'precision@50:', totalprecision50/userNum
    print 'recall@50:', totalrecall50/userNum
    print 'precision@100:', totalprecision100/userNum
    print 'recall@100:', totalrecall100/userNum

    return

def precisionAndRecall(sorted_x, k, userIndex, groundTruthDict, userRecallDict):
    hitCount = 0
    recallByUser = 0.0
    hitList = []
    for pair in sorted_x[:k]:
        itemIndex = pair[0]
        pairId = str(userIndex) + '-' + str(itemIndex)
        if pairId in groundTruthDict:
            hitCount += 1
            hitList.append(pairId)
    if userIndex in userRecallDict:
        recallByUser = hitCount * 1.0 / userRecallDict[userIndex]
    #print userIndex, k, hitCount, hitList

    return hitCount * 1.0 / k, recallByUser
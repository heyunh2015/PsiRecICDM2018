import json, random

def preprocessAmazonData(sampleFile, saveFilePath):
    TrainText = ''
    fp = open(sampleFile, 'r')
    lines = fp.readlines()
    count = 0
    Real2InDict = {}
    mapIdReviewer = 1
    mapIdProduct = 1000000 #so that the id of product and reviewer will not be blended
    for line in lines:
        if count % 10000 == 0:
            print count
        count += 1
        text = json.loads(line)
        reviewerId = text['reviewerID']
        productId = text['asin']

        if reviewerId not in Real2InDict:
            Real2InDict[reviewerId] = mapIdReviewer
            mapIdReviewer += 1

        if productId not in Real2InDict:
            Real2InDict[productId] = mapIdProduct
            mapIdProduct += 1

        TrainText += str(Real2InDict[reviewerId]) + '\t' + str(Real2InDict[productId]) + '\t' + '1.0' + '\n'
    saveFile(TrainText, saveFilePath)
    return 0

def splitTrainFile(InFile, trainFile, validationFile, testFile):
    file = open(InFile)
    lines = file.readlines()
    reviewerDict = {}
    productDict = {}
    testDict = {}
    trainDict = {}
    validationDict = {}
    for line in lines:
        lineStr = line.strip().split('\t')
        reviewerId = lineStr[0]
        productId = lineStr[1]
        if reviewerId not in reviewerDict:
            reviewerDict[reviewerId] = []
            reviewerDict[reviewerId].append(line)
        else:
            reviewerDict[reviewerId].append(line)
        if productId not in productDict:
            productDict[productId] = 1
        else:
            productDict[productId] += 1

    for reviewerId in reviewerDict:
        reviewNum = len(reviewerDict[reviewerId])
        for record in reviewerDict[reviewerId]:
            randomNum = random.random()
            lineStr = record.strip().split('\t')
            productId = lineStr[1]
            if reviewNum>1 and randomNum<=0.1 and productDict[productId]>1:
               reviewNum -= 1
               productDict[productId] -= 1
               if reviewerId not in testDict:
                   testDict[reviewerId] = []
                   testDict[reviewerId].append(record)
               else:
                   testDict[reviewerId].append(record)
            elif reviewNum>1 and randomNum > 0.1 and randomNum <= 0.2 and productDict[productId]>1:
                reviewNum -= 1
                productDict[productId] -= 1
                if reviewerId not in validationDict:
                    validationDict[reviewerId] = []
                    validationDict[reviewerId].append(record)
                else:
                    validationDict[reviewerId].append(record)
            else:
                if reviewerId not in trainDict:
                    trainDict[reviewerId] = []
                    trainDict[reviewerId].append(record)
                else:
                    trainDict[reviewerId].append(record)

    trainTxt = ''
    validationTxt = ''
    testTxt = ''
    for reviewerId in trainDict:
        for record in trainDict[reviewerId]:
            trainTxt += record

    for reviewerId in validationDict:
        for record in validationDict[reviewerId]:
            validationTxt += record

    for reviewerId in testDict:
        for record in testDict[reviewerId]:
            testTxt += record

    saveFile(trainTxt, trainFile)
    saveFile(testTxt, testFile)
    saveFile(validationTxt, validationFile)
    return 0

def preprocessTamllData(filename, saveFilePath, k):
    TrainText = ''
    fp = open(filename, 'r')
    lines = fp.readlines()
    Real2InDict = {}

    userDict = {}
    itemDict = {}
    for line in lines:
        lineStr = line.strip().split(',')
        if lineStr[-1] == '2':
            userId = lineStr[0]
            itemId = lineStr[1]
            if userId not in userDict:
                userDict[userId] = 1
            else:
                userDict[userId] += 1
            if itemId not in itemDict:
                itemDict[itemId] = 1
            else:
                itemDict[itemId] += 1

    coreLines = {}
    for line in lines:
        lineStr = line.strip().split(',')
        if lineStr[-1] == '2':#extract purchase behavior
            userId = lineStr[0]
            itemId = lineStr[1]
            if userDict[userId]>=k and itemDict[itemId]>=k:
                id = userId + '-' + itemId
                if id not in coreLines:
                    coreLines[id] = 1

    mapIdReviewer = 1
    mapIdProduct = 1000000  # so that the id of product and reviewer will not be blended

    count = 0
    for id in coreLines:
        if count%100000==0:
            print count
        count += 1
        reviewerId = id.split('-')[0] + 'u'
        productId = id.split('-')[1] + 'i'
        # reviewerId = line[0]+'u'
        # productId = line[1]+'i'
        if reviewerId not in Real2InDict:
            Real2InDict[reviewerId] = mapIdReviewer
            mapIdReviewer += 1

        if productId not in Real2InDict:
            Real2InDict[productId] = mapIdProduct
            mapIdProduct += 1

        TrainText += str(Real2InDict[reviewerId]) + '\t' + str(Real2InDict[productId]) + '\t' + '1.0' + '\n'
    saveFile(TrainText, saveFilePath)
    print 'product num:', mapIdProduct-1000000
    print 'user num:', mapIdReviewer-1
    return 0

def storeweakClassArr(inputTree, filename):
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()


def grabweakClassArr(filename):
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)

def saveFile(string, fileName):
    fp_w = open(fileName,'w')
    fp_w.write(string)
    fp_w.close()
    return 0

if __name__ == '__main__':
    # preprocessAmazonData('rawData/cell/reviews_Cell_Phones_and_Accessories_5.json',
    #                   'preProcessedData/cell/reviews_Cell_Phones_and_Accessories_5.interactions')
    # preprocessTamllData('rawData/Tmall/user_log_format1.csv',
    #                     'preProcessedData/Tmall/tmall_20.interactions',
    #                     20)
    splitTrainFile('preProcessedData/Tmall/tmall_20.interactions',
                   'preProcessedData/Tmall/tmall_20_train.interactions',
                   'preProcessedData/Tmall/tmall_20_validation.interactions',
                   'preProcessedData/Tmall/tmall_20_test.interactions')


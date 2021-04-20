import datetime

# 从P10000开始, P10001, P10002
def createProblemId(seqNum):

    seq = 10000 + seqNum

    problemId = 'P' + str(seq)
    return problemId


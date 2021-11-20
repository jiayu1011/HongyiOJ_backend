import HongyiOJ.config as HostConfig

def outputAnalyze(standardOutputFilePath, dockerOutputFilePath):
    """
    evaluate the output file

    :param standardOutputFilePath:
    :param dockerOutputFilePath:
    :return:
    """

    with open(dockerOutputFilePath, 'r') as f:
        dockerOutputTxt = f.read()

    with open(standardOutputFilePath, 'r') as f:
        stdOutputTxt = f.read()

    if dockerOutputTxt == stdOutputTxt:
        return HostConfig.Config.ACCEPTED

    dockerOutputArr = dockerOutputTxt.split()
    stdOutputArr = stdOutputTxt.split()

    if len(stdOutputArr) != len(dockerOutputArr):
        return HostConfig.Config.WRONG_ANSWER



    for (index, item) in enumerate(stdOutputArr):
        if item != dockerOutputArr[index]:
            return HostConfig.Config.WRONG_ANSWER

    return HostConfig.Config.PRESENTATION_ERROR


if __name__=='__main__':
    res = outputAnalyze('stdOutput.txt', 'dockerOutput.txt')
    print(res)
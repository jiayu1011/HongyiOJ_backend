import HostConfig
import utils

def outputAnalyze(stdInputFilePath, stdOutputFilePath, targetOutputFilePath, CEFilePath, REFilePath):
    """
    evaluate the output file

    :param REFilePath:
    :param CEFilePath:
    :param stdInputFilePath:
    :param stdOutputFilePath:
    :param targetOutputFilePath:
    :return:
    """
    wrongCase = {}


    # Compile Error & Runtime Error Judge
    errType, errLog = utils.checkErr(CEFilePath=CEFilePath, REFilePath=REFilePath)
    if errType:
        if errType==HostConfig.Config.COMPILE_ERROR:
            return errType, wrongCase, errLog
        elif errType==HostConfig.Config.RUNTIME_ERROR:
            return errType, wrongCase, errLog


    with open(targetOutputFilePath, 'r') as f:
        dockerOutputTxt = f.read()

    with open(stdOutputFilePath, 'r') as f:
        stdOutputTxt = f.read()

    with open(stdInputFilePath, 'r') as f:
        stdInputTxt = f.read()

    if dockerOutputTxt == stdOutputTxt:
        return HostConfig.Config.ACCEPTED, wrongCase, errLog

    dockerOutputArr = dockerOutputTxt.split()
    stdOutputArr = stdOutputTxt.split()
    stdInputArr = stdInputTxt.split()

    if len(stdOutputArr) != len(dockerOutputArr):
        return HostConfig.Config.WRONG_ANSWER, wrongCase, errLog



    for (index, item) in enumerate(stdOutputArr):
        if stdOutputArr[index] != dockerOutputArr[index]:
            # Record wrong case
            wrongCase = {
                'stdInputCase': stdInputArr[index],
                'stdOutputCase': stdOutputArr[index],
                'dockerOutputCase': dockerOutputArr[index]
            }
            return HostConfig.Config.WRONG_ANSWER, wrongCase, errLog

    return HostConfig.Config.PRESENTATION_ERROR, wrongCase, errLog


if __name__=='__main__':
    res = outputAnalyze('stdInput.txt', 'stdOutput.txt', 'dockerOutput.txt', '')



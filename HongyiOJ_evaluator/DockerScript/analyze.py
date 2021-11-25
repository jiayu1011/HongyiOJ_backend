import HostConfig
import utils

def outputAnalyze(
        codeLanguage,
        stdInputFilePath,
        stdOutputFilePath,
        targetOutputFilePath,
        CEFilePath,
        REFilePath,
        status
):
    """
    evaluate the output file


    :param status:
    :param REFilePath:
    :param CEFilePath:
    :param stdInputFilePath:
    :param stdOutputFilePath:
    :param targetOutputFilePath:
    :return:
    """
    wrongCase = {
        'stdInputCase': '',
        'stdOutputCase': '',
        'dockerOutputCase': ''
    }




    # Compile Error & Runtime Error Judge
    errType, errLog = utils.checkCodeErr(
        codeLanguage=codeLanguage,
        CEFilePath=CEFilePath,
        REFilePath=REFilePath
    )

    # Check whether process has normally exited(TLE, MLE)
    if status in HostConfig.ProcessStatus.abnormalStatus:
        if status == HostConfig.ProcessStatus.TIME_LIMIT_EXCEEDED:
            return HostConfig.ResultType.TIME_LIMIT_EXCEEDED, wrongCase, errLog
        elif status == HostConfig.ProcessStatus.MEMORY_LIMIT_EXCEEDED:
            return HostConfig.ResultType.MEMORY_LIMIT_EXCEEDED, wrongCase, errLog

    # Check CE, RE
    if errType:
        if errType==HostConfig.ResultType.COMPILE_ERROR:
            return errType, wrongCase, errLog
        elif errType==HostConfig.ResultType.RUNTIME_ERROR:
            return errType, wrongCase, errLog


    with open(targetOutputFilePath, 'r') as f:
        dockerOutputTxt = f.read()

    with open(stdOutputFilePath, 'r') as f:
        stdOutputTxt = f.read()

    with open(stdInputFilePath, 'r') as f:
        stdInputTxt = f.read()

    if dockerOutputTxt == stdOutputTxt:
        return HostConfig.ResultType.ACCEPTED, wrongCase, errLog

    dockerOutputArr = dockerOutputTxt.split()
    stdOutputArr = stdOutputTxt.split()
    stdInputArr = stdInputTxt.split()

    if len(stdOutputArr) != len(dockerOutputArr):
        return HostConfig.ResultType.WRONG_ANSWER, wrongCase, errLog



    for (index, item) in enumerate(stdOutputArr):
        if stdOutputArr[index] != dockerOutputArr[index]:
            # Record wrong case
            wrongCase = {
                'stdInputCase': stdInputArr[index],
                'stdOutputCase': stdOutputArr[index],
                'dockerOutputCase': dockerOutputArr[index]
            }
            return HostConfig.ResultType.WRONG_ANSWER, wrongCase, errLog

    return HostConfig.ResultType.PRESENTATION_ERROR, wrongCase, errLog


if __name__=='__main__':
    res = outputAnalyze('stdInput.txt', 'stdOutput.txt', 'dockerOutput.txt', '')



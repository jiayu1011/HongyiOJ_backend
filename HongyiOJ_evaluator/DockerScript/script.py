import os
import sys
import HongyiOJ_evaluator.DockerConfig.config as DockerConfig
import HongyiOJ_evaluator.DockerScript.utils as utils


def separateInput(src, dst):
    """

    :param src: standard input before handling
    :param dst: many input group which is handled
    :return:
    """
    with open(src, 'r') as f:
        inputTxt = f.read()


    inputArr = inputTxt.split('##\n')

    inputIndex = 0

    if not os.path.exists(dst):
        os.mkdir(dst)
    for item in inputArr:
        inputIndex = inputIndex + 1
        with open('{}/input_{}'.format(dst, inputIndex), 'w') as f:
            f.write(item)


def handleC(codeFilePath, compileOutput, inputFilePath, outputFilePath):
    os.system("gcc {} -o {}".format(codeFilePath, compileOutput))
    os.system("./{} < {} >> {}".format(compileOutput, inputFilePath, outputFilePath))

    # windows test version
    # os.system("{} < {} >> {}".format(compileOutput, inputFilePath, outputFilePath))


def handleCpp(codeFilePath, compileOutput, inputFilePath, outputFilePath):
    os.system("g++ {} -o {}".format(codeFilePath, compileOutput))
    os.system("./{} < {} >> {}".format(compileOutput, inputFilePath, outputFilePath))


def handlePy3(codeFilePath, inputFilePath, outputFilePath):
    os.system("python {}  < {} >> ${}".format(codeFilePath, inputFilePath, outputFilePath))


def handleJava(codeFilePath, javaMainClass, inputFilePath, outputFilePath):
    os.system("javac {}".format(codeFilePath))
    os.system("java {}  < {} >> {}".format(javaMainClass, inputFilePath, outputFilePath))







if __name__=='__main__':
    args = sys.argv
    evaluationId = args[1]  # E10001
    codeFileName = args[2]  # E10001_code.java
    codeLanguage = args[3]  # Java
    compileOutput = 'compileOutput'
    javaMainClass = codeFileName.split('.')[0]
    inputFileName = "{}_input.txt".format(evaluationId)
    outputFileName = "{}_output.txt".format(evaluationId)


    inputSrc = inputFileName
    inputDst = DockerConfig.Config.inputGroupFilePath
    """
    Separate Input
    """
    # Separate std input into many input groups
    separateInput(src=inputSrc, dst=inputDst)


    """
    Feeding Input Groups
    """
    # Test through whole input groups and add result
    # to "${evaluationId}_output.txt"
    inputGroups = os.listdir(inputDst)
    cnt = 1
    for curInputGroup in inputGroups:
        if codeLanguage == 'C':
            handleC(codeFileName, compileOutput, "{}/{}".format(inputDst, curInputGroup), outputFileName)

        elif codeLanguage == 'C++':
            handleCpp(codeFileName, compileOutput, "{}/{}".format(inputDst, curInputGroup), outputFileName)

        elif codeLanguage == 'Python3':
            handlePy3(codeFileName, "{}/{}".format(inputDst, curInputGroup), outputFileName)

        elif codeLanguage == 'Java':
            handleJava(codeFileName, javaMainClass, "{}/{}".format(inputDst, curInputGroup), outputFileName)

        # Prevent answer ending with '\s|\r|\n'
        utils.rmEndSpace(outputFileName)

        if cnt<len(inputGroups):
            os.system('echo "##" >> {}'.format(outputFileName))
            cnt += 1

















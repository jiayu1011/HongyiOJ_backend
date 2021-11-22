import os
import sys
import DockerConfig
import utils
import analyze


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
        with open('{}/input_{}.txt'.format(dst, inputIndex), 'w') as f:
            f.write(item)


def handleC(codeFilePath, compileOutput, inputFilePath, outputFilePath, CEFilePath, REFilePath, pIdFilePath):
    # Ignore all warnings during compiling
    os.system(f"gcc {codeFilePath} -w -o {compileOutput} 2>> {CEFilePath}")
    os.system(f"./{compileOutput} < {inputFilePath} 1>> {outputFilePath} 2>> {REFilePath} && echo $! >> {pIdFilePath}")



def handleCpp(codeFilePath, compileOutput, inputFilePath, outputFilePath, CEFilePath, REFilePath, pIdFilePath):
    # Ignore all warnings during compiling
    os.system(f"g++ {codeFilePath} -w -o {compileOutput} 2>> {CEFilePath}")
    os.system(f"./{compileOutput} < {inputFilePath} 1>> {outputFilePath} 2>> {REFilePath} && echo $! >> {pIdFilePath}")


def handlePy3(codeFilePath, inputFilePath, outputFilePath, REFilePath, pIdFilePath):
    os.system(f"python {codeFilePath} < {inputFilePath} 1>> {outputFilePath} 2>> {REFilePath} && echo $! >> {pIdFilePath}")


def handleJava(codeFilePath, javaMainClass, inputFilePath, outputFilePath, CEFilePath, REFilePath, pIdFilePath):
    codeFileName = codeFilePath.split('/')[-1]
    if os.path.exists(codeFileName):
        # Rename to Main.java in order to prevent Compile Error
        os.system('rename {} {}.java {}'.format(codeFileName, javaMainClass, codeFileName))
    os.system(f'javac {javaMainClass}.java 2>> {CEFilePath}')
    os.system(f"java {javaMainClass} < {inputFilePath} 1>> {outputFilePath} 2>> {REFilePath} && echo $! >> {pIdFilePath}")








if __name__=='__main__':
    args = sys.argv
    evaluationId = args[1]  # E10001
    problemId = args[2]     # P10001
    codeFileName = args[3]  # E10001_code.java
    codeLanguage = args[4]  # Java

    dockerConfig = DockerConfig.Config(evaluationId=evaluationId, problemId=problemId)


    inputSrc = dockerConfig.stdInputFilePath
    inputDst = dockerConfig.inputCasesFolderPath
    """
    Separate Input
    """
    # Separate std input into many input groups
    separateInput(src=inputSrc, dst=inputDst)


    if not os.path.exists(dockerConfig.outputFolderPath):
        os.mkdir(dockerConfig.outputFolderPath)

    os.chdir(dockerConfig.rootPath)



    """
    Feeding Input Groups
    """
    # Test through all input cases and add result and err(if exist)
    # to "${evaluationId}_output.txt" and "error_log.txt"
    inputCases = os.listdir(inputDst)
    cnt = 1
    for i in range(len(inputCases)):
        index = i+1
        curInputCase = f'input_{index}.txt'
        # Needs compile
        if codeLanguage == 'C':
            handleC(
                codeFilePath='{}/{}'.format(dockerConfig.rootPath, codeFileName),
                compileOutput=dockerConfig.compileOutputFileName,
                inputFilePath="{}/{}".format(dockerConfig.inputCasesFolderPath, curInputCase),
                outputFilePath=dockerConfig.dockerOutputFilePath,
                CEFilePath=dockerConfig.CEFilePath,
                REFilePath=dockerConfig.REFilePath,
                pIdFilePath=dockerConfig.pIdFilePath
            )

        # Needs compile
        elif codeLanguage == 'C++':
            handleCpp(
                codeFilePath='{}/{}'.format(dockerConfig.rootPath, codeFileName),
                compileOutput=dockerConfig.compileOutputFileName,
                inputFilePath="{}/{}".format(dockerConfig.inputCasesFolderPath, curInputCase),
                outputFilePath=dockerConfig.dockerOutputFilePath,
                CEFilePath=dockerConfig.CEFilePath,
                REFilePath=dockerConfig.REFilePath,
                pIdFilePath=dockerConfig.pIdFilePath
            )

        elif codeLanguage == 'Python3':
            handlePy3(
                codeFilePath='{}/{}'.format(dockerConfig.rootPath, codeFileName),
                inputFilePath="{}/{}".format(dockerConfig.inputCasesFolderPath, curInputCase),
                outputFilePath=dockerConfig.dockerOutputFilePath,
                REFilePath=dockerConfig.REFilePath,
                pIdFilePath=dockerConfig.pIdFilePath
            )

        elif codeLanguage == 'Java':
            print('handling java...')

            handleJava(
                codeFilePath='{}/{}'.format(dockerConfig.rootPath, codeFileName),
                javaMainClass=dockerConfig.javaMainClass,
                inputFilePath="{}/{}".format(dockerConfig.inputCasesFolderPath, curInputCase),
                outputFilePath=dockerConfig.dockerOutputFilePath,
                CEFilePath=dockerConfig.CEFilePath,
                REFilePath=dockerConfig.REFilePath,
                pIdFilePath=dockerConfig.pIdFilePath
            )




        # Prevent answer ending with '\s|\r|\n'
        # if os.path.exists(dockerConfig.dockerOutputFilePath):
        #     print('output file has been created...')

        utils.rmEndSpace(dockerConfig.dockerOutputFilePath)

        if cnt<len(inputCases):
            os.system(f'echo -e "\n##" >> {dockerConfig.dockerOutputFilePath}')
            cnt += 1

        errType, errLog = utils.checkErr(
            CEFilePath=dockerConfig.CEFilePath,
            REFilePath=dockerConfig.REFilePath
        )
        if errType:
            break


    print('------running complete!------------')



    """
    Result Analyzing
    """
    result, wrongCase, errLog = analyze.outputAnalyze(
        stdInputFilePath=dockerConfig.stdInputFilePath,
        stdOutputFilePath=dockerConfig.stdOutputFilePath,
        targetOutputFilePath=dockerConfig.dockerOutputFilePath,
        CEFilePath=dockerConfig.CEFilePath,
        REFilePath=dockerConfig.REFilePath
    )



    timeCost = 0
    memoryCost = 0

    with open(dockerConfig.analyzeResFilePath, 'w') as f:
        f.write(f'{result}\n')
        if errLog:
            f.write(f'{errLog}')
        else:
            f.write(f'{timeCost}\n')
            f.write(f'{memoryCost}')

            if wrongCase:
                f.write('\n')
                f.write(f'{wrongCase["stdInputCase"]}\n')
                f.write(f'{wrongCase["stdOutputCase"]}\n')
                f.write(f'{wrongCase["dockerOutputCase"]}')




















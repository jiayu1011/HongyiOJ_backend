import os
import sys
import DockerConfig
import HostConfig
import utils
import analyze
import psutil
import monitor
import subprocess
import time



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


def handleC(
        codeFilePath,
        compileOutput,
        inputFile,
        outputFile,
        CEFile,
        REFile,
        timeLimit,
        memoryLimit
):
    # Ignore all warnings during compiling


    # os.system(f"gcc {codeFilePath} -w -o {compileOutput} 2>> {CEFile}")
    # os.system(f"./{compileOutput} < {inputFile} 1>> {outputFile} 2>> {REFile}")

    """
    Using psutil.Popen in order to monitor process status
    """
    compileProcess = subprocess.Popen(
        [
            'gcc',
            codeFilePath,
            '-w',
            '-o',
            compileOutput
        ],
        stderr=CEFile
    )
    compileProcess.wait()

    try:
        execProcess = subprocess.Popen(
            [
                f'./{compileOutput}'
            ],
            stdin=inputFile,
            stdout=outputFile,
            stderr=REFile
        )
    except IOError:
        return '', 0, 0, 0
    else:
        print(f'execProcess\'s pid:{execProcess.pid}')
        status, timeCost, memoryCost = monitor.monitor(
            process=execProcess,
            timeLimit=timeLimit,
            memoryLimit=memoryLimit,
        )

        return status, timeCost, memoryCost, execProcess.returncode






def handleCpp(
        codeFilePath,
        compileOutput,
        inputFile,
        outputFile,
        CEFile,
        REFile,
        timeLimit,
        memoryLimit
):
    # Ignore all warnings during compiling
    # os.system(f"g++ {codeFilePath} -w -o {compileOutput} 2>> {CEFile}")
    # os.system(f"./{compileOutput} < {inputFile} 1>> {outputFile} 2>> {REFile}")

    compileProcess = subprocess.Popen(
        [
            'g++',
            codeFilePath,
            '-w',
            '-o',
            compileOutput
        ],
        stderr=CEFile
    )
    compileProcess.wait()


    try:
        execProcess = subprocess.Popen(
            [
                f'./{compileOutput}'
            ],
            stdin=inputFile,
            stdout=outputFile,
            stderr=REFile
        )
    except IOError:
        return '', 0, 0, 0
    else:
        print(f'execProcess\'s pid:{execProcess.pid}')
        status, timeCost, memoryCost = monitor.monitor(
            process=execProcess,
            timeLimit=timeLimit,
            memoryLimit=memoryLimit,
        )
        print(execProcess.returncode)



        return status, timeCost, memoryCost, execProcess.returncode



def handlePy3(
        codeFilePath,
        inputFile,
        outputFile,
        REFile,
        timeLimit,
        memoryLimit
):
    # os.system(f"python {codeFilePath} < {inputFile} 1>> {outputFile} 2>> {REFile}")
    execProcess = subprocess.Popen(
        [
            'python',
            codeFilePath
        ],
        stdin=inputFile,
        stdout=outputFile,
        stderr=REFile
    )
    print(f'execProcess\'s pid:{execProcess.pid}')

    status, timeCost, memoryCost = monitor.monitor(
        process=execProcess,
        timeLimit=timeLimit,
        memoryLimit=memoryLimit,
    )


    return status, timeCost, memoryCost, execProcess.returncode



def handleJava(
        codeFilePath,
        javaMainClass,
        inputFile,
        outputFile,
        CEFile,
        REFile,
        timeLimit,
        memoryLimit
):
    codeFileName = codeFilePath.split('/')[-1]
    if os.path.exists(codeFileName):
        # Rename to Main.java in order to prevent Compile Error
        renameProcess = subprocess.Popen(
            [
                'rename',
                codeFileName,
                f'{javaMainClass}.java',
                codeFileName
            ]
        )
        renameProcess.wait()
        # print(os.listdir(os.getcwd()))
        # os.system(f'rename {codeFileName} {javaMainClass}.java {codeFileName}')


    # os.system(f'javac {javaMainClass}.java 2>> {CEFile}')
    # os.system(f"java {javaMainClass} < {inputFile} 1>> {outputFile} 2>> {REFile}")

    compileProcess = subprocess.Popen(
        [
            'javac',
            f'{javaMainClass}.java'
        ],
        stderr=CEFile
    )
    compileProcess.wait()
    try:
        execProcess = subprocess.Popen(
            [
                'java',
                javaMainClass
            ],
            stdin=inputFile,
            stdout=outputFile,
            stderr=REFile
        )
    except IOError:
        return '', 0, 0, 0
    else:
        print(f'execProcess\'s pid:{execProcess.pid}')

        status, timeCost, memoryCost = monitor.monitor(
            process=execProcess,
            timeLimit=timeLimit,
            memoryLimit=memoryLimit
        )

        return status, timeCost, memoryCost, execProcess.returncode








if __name__=='__main__':
    args = sys.argv
    evaluationId = args[1]  # E10001
    problemId = args[2]     # P10001
    codeFileName = args[3]  # E10001_code.java
    codeLanguage = args[4]  # Java
    timeLimit = float(args[5])     # 1000
    memoryLimit = float(args[6])   # 125

    dockerConfig = DockerConfig.Config(
        evaluationId=evaluationId,
        problemId=problemId,
        timeLimit=timeLimit,
        memoryLimit=memoryLimit
    )



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

    print('--------------------------------')
    print('--------start running!----------')
    print('--------------------------------')


    """
    Feeding Input Groups
    """
    # Test through all input cases and add result and err(if exist)
    # to "${evaluationId}_output.txt" and
    # "compile_error_log.txt, runtime_error_log.txt"
    inputCases = os.listdir(inputDst)
    cnt = 1
    status = ''
    timeCost = 0
    memoryCost = 0
    maxTimeCost = 0
    maxMemoryCost = 0
    returnCode = 0

    for i in range(len(inputCases)):
        index = i+1
        print(f'input{index} start...')
        curInputCase = f'input_{index}.txt'

        inputFilePath = f'{dockerConfig.inputCasesFolderPath}/{curInputCase}'
        outputFilePath = dockerConfig.dockerOutputFilePath


        stdInputFile = open(inputFilePath, 'r')
        outputFile = open(outputFilePath, 'a')
        CEFile = open(dockerConfig.CEFilePath, 'a')
        REFile = open(dockerConfig.REFilePath, 'a')


        # Needs compile
        if codeLanguage == HostConfig.CodeLanguageType.C:
            status, timeCost, memoryCost, returnCode = handleC(
                codeFilePath=f'{dockerConfig.rootPath}/{codeFileName}',
                compileOutput=dockerConfig.compileOutputFileName,
                inputFile=stdInputFile,
                outputFile=outputFile,
                CEFile=CEFile,
                REFile=REFile,
                timeLimit=timeLimit,
                memoryLimit=memoryLimit
            )

        # Needs compile
        elif codeLanguage == HostConfig.CodeLanguageType.C_PRIMER_PLUS:
            status, timeCost, memoryCost, returnCode = handleCpp(
                codeFilePath=f'{dockerConfig.rootPath}/{codeFileName}',
                compileOutput=dockerConfig.compileOutputFileName,
                inputFile=stdInputFile,
                outputFile=outputFile,
                CEFile=CEFile,
                REFile=REFile,
                timeLimit=timeLimit,
                memoryLimit=memoryLimit
            )

        elif codeLanguage == HostConfig.CodeLanguageType.PYTHON3:
            status, timeCost, memoryCost, returnCode = handlePy3(
                codeFilePath=f'{dockerConfig.rootPath}/{codeFileName}',
                inputFile=stdInputFile,
                outputFile=outputFile,
                REFile=REFile,
                timeLimit=timeLimit,
                memoryLimit=memoryLimit
            )

        elif codeLanguage == HostConfig.CodeLanguageType.JAVA:
            # print('handling java...')

            status, timeCost, memoryCost, returnCode = handleJava(
                codeFilePath=f'{dockerConfig.rootPath}/{codeFileName}',
                javaMainClass=dockerConfig.javaMainClass,
                inputFile=stdInputFile,
                outputFile=outputFile,
                CEFile=CEFile,
                REFile=REFile,
                timeLimit=timeLimit,
                memoryLimit=memoryLimit
            )

        stdInputFile.close()
        outputFile.close()
        CEFile.close()
        REFile.close()

        if status in HostConfig.ProcessStatus.abnormalStatus:
            break

        # Record max usage of CPU time and memory
        maxTimeCost = max(maxTimeCost, timeCost)
        maxMemoryCost = max(maxMemoryCost, memoryCost)

        realReturnCode = -returnCode
        #
        if realReturnCode in HostConfig.Config.processTerminatedExitCode2SignalDict:
            with open(dockerConfig.REFilePath, 'a') as f:
                f.write(HostConfig.Config.processTerminatedExitCode2SignalDict[realReturnCode])

        # Check whether an error has happened
        errType, errLog = utils.checkCodeErr(
            codeLanguage=codeLanguage,
            CEFilePath=dockerConfig.CEFilePath,
            REFilePath=dockerConfig.REFilePath
        )
        if errType:
            break



        # Prevent answer ending with '\s|\r|\n'
        # if os.path.exists(dockerConfig.dockerOutputFilePath):
        #     print('output file has been created...')

        utils.rmEndSpace(dockerConfig.dockerOutputFilePath)

        if cnt<len(inputCases):
            os.system(f'echo -e "\n##" >> {dockerConfig.dockerOutputFilePath}')
            cnt += 1


        print(f'input{index} complete...')




    print('--------------------------------')
    print('-------running complete!--------')
    print('--------------------------------')



    """
    Result Analyzing
    """
    result, wrongCase, errLog = analyze.outputAnalyze(
        codeLanguage=codeLanguage,
        stdInputFilePath=dockerConfig.stdInputFilePath,
        stdOutputFilePath=dockerConfig.stdOutputFilePath,
        targetOutputFilePath=dockerConfig.dockerOutputFilePath,
        CEFilePath=dockerConfig.CEFilePath,
        REFilePath=dockerConfig.REFilePath,
        status=status
    )




    with open(dockerConfig.analyzeResFilePath, 'w') as f:
        f.write(f'result: {result}\n')
        f.write(f'timeCost: {maxTimeCost}\n')
        f.write(f'memoryCost: {maxMemoryCost}\n')
        f.write(f'stdInputCase: {wrongCase["stdInputCase"]}\n')
        f.write(f'stdOutputCase: {wrongCase["stdOutputCase"]}\n')
        f.write(f'dockerOutputCase: {wrongCase["dockerOutputCase"]}\n')
        f.write(f'errLog: {errLog}\n')






















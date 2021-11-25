"""
Inside Docker Container
"""

# Position where data is stored in an exact docker container

class Config:
    rootPath = '/Temp'
    evaluatorImageName = 'hongyioj_evaluator:v2'
    scriptFolderPath = '{}/DockerScript'.format(rootPath)
    inputCasesFolderPath = '{}/input_cases'.format(rootPath)
    outputFolderPath = f'{rootPath}/output'
    compileOutputFileName = 'compile_output'
    javaMainClass = 'Main'
    CEFileName = 'compile_error_log.txt'  # Compile Error log
    CEFilePath = f'{outputFolderPath}/{CEFileName}'
    REFileName = 'runtime_error_log.txt'  # Runtime Error log
    REFilePath = f'{outputFolderPath}/{REFileName}'
    analyzeResFileName = 'analyze_result.txt'
    analyzeResFilePath = '{}/{}'.format(outputFolderPath, analyzeResFileName)
    pIdFileName = 'pid.txt'
    pIdFilePath = '{}/{}'.format(rootPath, pIdFileName)


    perContainerMemoryUsageLimit = '500m'




    def __init__(
            self,
            evaluationId,
            problemId,
            timeLimit,
            memoryLimit
    ):
        self.stdInputFilePath = '{}/{}_stdInput.txt'.format(self.rootPath, problemId)
        self.stdOutputFilePath = '{}/{}_stdOutput.txt'.format(self.rootPath, problemId)
        self.dockerOutputFileName = "{}_output.txt".format(evaluationId)
        self.dockerOutputFilePath = '{}/{}'.format(self.outputFolderPath, self.dockerOutputFileName)
        self.timeLimit = timeLimit
        self.memoryLimit = memoryLimit












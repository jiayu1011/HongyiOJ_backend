"""
Config
"""

class Config:
    rootPath = '/HongyiOJ'
    codeSuffixDic = {
        'C': '.c',
        'C++': '.cpp',
        'Python3': '.py',
        'Java': '.java'
    }




    # Position where recent code is stored
    codeSubmitStorePath = '{}/HongyiOJ_backend/HongyiOJ_evaluator/Evaluation/SubmitCode'.format(rootPath)
    # Code Storage Limit
    codeAmount = 500
    # Position where recent docker is prepared
    dockerPreparedPath = f'{rootPath}/HongyiOJ_backend/HongyiOJ_evaluator/Evaluation/DockerTemp'
    dockerScriptFolderPath = '{}/HongyiOJ_backend/HongyiOJ_evaluator/DockerScript'.format(rootPath)
    outputFolderName = 'output'
    analyzeResFileName = 'analyze_result.txt'


    separator = '##'


    processTerminatedExitCode2SignalDict = {
        7: 'Bus Error',
        8: 'Float Point Error',
        11: 'Segmentation Fault',

    }






    def __init__(self):
        return


class ResultType:
    # Evaluation result types(7 types)
    ACCEPTED = 'Accepted'
    COMPILE_ERROR = 'Compile Error'
    RUNTIME_ERROR = 'Runtime Error'
    PRESENTATION_ERROR = 'Presentation Error'
    TIME_LIMIT_EXCEEDED = 'Time Limit Exceeded'
    MEMORY_LIMIT_EXCEEDED = 'Memory Limit Exceeded'
    WRONG_ANSWER = 'Wrong Answer'


class CodeLanguageType:
    C = 'C'
    C_PRIMER_PLUS = 'C++'
    PYTHON3 = 'Python3'
    JAVA = 'Java'

    """
       Code Languages separation
       """
    # First compile and then execute(Compile Language)
    compileLanguages = [C, C_PRIMER_PLUS, JAVA]
    # Compiling while executing(Interpretive Language)
    interpretiveLanguages = [PYTHON3]


class ProcessStatus:
    NORMALLY_EXIT = 'Normally Exit'
    TERMINATED = 'Terminated'
    TIME_LIMIT_EXCEEDED = 'Time Limit Exceeded'
    MEMORY_LIMIT_EXCEEDED = 'Memory Limit Exceeded'

    abnormalStatus = [
        TIME_LIMIT_EXCEEDED,
        MEMORY_LIMIT_EXCEEDED
    ]


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


    # Evaluation result types(7 types)
    ACCEPTED = 'Accepted'
    COMPILE_ERROR = 'Compile Error'
    RUNTIME_ERROR = 'Runtime Error'
    PRESENTATION_ERROR = 'Presentation Error'
    TIME_LIMIT_EXCEEDED = 'Time Limit Exceeded'
    MEMORY_LIMIT_EXCEEDED = 'Memory Limit Exceeded'
    WRONG_ANSWER = 'Wrong Answer'


    def __init__(self):
        return






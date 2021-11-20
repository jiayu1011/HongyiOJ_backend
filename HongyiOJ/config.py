"""
Config
"""

class Config:
    codeSuffixDic = {
        'C': '.c',
        'C++': '.cpp',
        'Python3': '.py',
        'Java': '.java'
    }
    # Position where recent code is stored
    codeSubmitStorePath = '/HongyiOJ/HongyiOJ_backend/HongyiOJ_evaluator/Evaluation/SubmitCode'
    # Code Storage Limit
    codeAmount = 500
    # Position where recent docker is prepared
    dockerPreparedPath = '/HongyiOJ/HongyiOJ_backend/HongyiOJ_evaluator/Evaluation/DockerTemp'
    dockerScriptPath = '/HongyiOJ/HongyiOJ_backend/HongyiOJ_evaluator/DockerScript/script.py'



    # Evaluation result types(7 types)
    ACCEPTED = 'Accepted'
    COMPILE_ERROR = 'Compile Error'
    RUNTIME_ERROR = 'Runtime Error'
    PRESENTATION_ERROR = 'Presentation Error'
    TIME_LIMIT_EXCEEDED = 'Time Limit Exceeded'
    MEMORY_LIMIT_EXCEEDED = 'Memory Limit Exceeded'
    WRONG_ANSWER = 'Wrong Answer'








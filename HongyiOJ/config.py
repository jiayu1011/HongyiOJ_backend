"""
Config
"""

class Config:
    # Position where recent code is stored
    codeSubmitStorePath = '/HongyiOJ/HongyiOJ_evaluator/Evaluation/SubmitCode'
    # Code Storage Limit
    codeAmount = 500
    # Position where recent docker is prepared
    dockerPreparedPath = '/HongyiOJ/HongyiOJ_evaluator/Evaluation/DockerTemp'
    dockerScriptPath = '/HongyiOJ/HongyiOJ_evaluator/DockerConfig/evaluator.sh'



    """
    Inside Docker
    """

    # Position where data is stored in an exact docker container
    tempPath = '/Temp/'





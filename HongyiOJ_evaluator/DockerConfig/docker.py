import os
import shutil


import HongyiOJ.config as HostConfig
import HongyiOJ_evaluator.DockerConfig.config
import HongyiOJ_evaluator.DockerConfig.config as DockerConfig
from HongyiOJ.utils import *


def runDocker(evaluationId, problemId, stdInputTxt, stdOutputTxt, limitations) -> str:
    hostConfig = HostConfig.Config()
    dockerConfig = DockerConfig.Config(evaluationId=evaluationId, problemId=problemId)

    os.chdir(hostConfig.dockerPreparedPath)
    os.mkdir(evaluationId)

    os.chdir(hostConfig.dockerPreparedPath + '/' + evaluationId)
    codeFileName = ''
    codeFilePath = ''
    destFilePath = ''
    codeLanguage = ''
    for file in os.listdir(hostConfig.codeSubmitStorePath):
        # Find the exact code file and then copy
        if file.find(evaluationId) != -1:
            source = hostConfig.codeSubmitStorePath + '/' + file
            dest = hostConfig.dockerPreparedPath + '/' + evaluationId
            codeFileName = file
            codeFilePath = source
            destFilePath = dest
            # Copy code
            shutil.copy(source, dest)

            suffix = '.' + codeFileName.split('.')[-1]
            codeLanguage = getCodeLanguage(suffix)

            break

    os.system(f'cp -r {hostConfig.dockerScriptFolderPath} {destFilePath}')
    os.system(f'cp {"/HongyiOJ/HongyiOJ_backend/HongyiOJ_evaluator/DockerConfig/config.py"} {destFilePath}/DockerScript/DockerConfig.py')
    os.system(f'cp {"/HongyiOJ/HongyiOJ_backend/HongyiOJ/config.py"} {destFilePath}/DockerScript/HostConfig.py')

    with open(f'{problemId}_stdInput.txt', 'w') as f:
        f.write(stdInputTxt)
    with open(f'{problemId}_stdOutput.txt', 'w') as f:
        f.write(stdOutputTxt)

    # create dockerfile
    with open('Dockerfile', 'w') as f:
        f.writelines(
            DockerfileTemplate(
                evaluationId=evaluationId,
                problemId=problemId,
                codeFileName=codeFileName,
                codeFilePath=codeFilePath,
                codeLanguage=codeLanguage,
                limitations=limitations
            )
        )



    """
    Docker Start
    """

    # Build image
    imageName = 'hongyioj_evaluation/{}'.format(evaluationId[1:])
    os.system('cd {} && docker build -t {} .'.format(destFilePath, imageName))

    # Run container && destroy container
    containerName = evaluationId
    os.system('docker run --name={} -it {}'.format(containerName, imageName))

    # Entering docker bash
    # Analyzing && Running!

    # Check whether docker has done its work



    # Get docker running result
    # """
    # docker cmd:
    # docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH
    # """
    outputFolderPath = dockerConfig.outputFolderPath
    SRC_PATH = outputFolderPath
    DEST_PATH = f'{hostConfig.dockerPreparedPath}/{evaluationId}'
    os.system('docker cp {}:{} {}'.format(containerName, SRC_PATH, DEST_PATH))
    #
    # # Delete container and image after all
    os.system('docker rm {}'.format(containerName))
    os.system('docker rmi {}'.format(imageName))

    """
    Docker End
    """

    """
    ${evaluationId}_output.txt and "analyze_result.txt" already exist 
    """


    evaluationOutputFolderPath = f'{os.getcwd()}/{hostConfig.outputFolderName}'


    return evaluationOutputFolderPath


def DockerfileTemplate(evaluationId, problemId, codeFileName, codeFilePath, codeLanguage, limitations) -> str:
    """

    :param evaluationId:
    :param problemId:
    :param codeFileName:
    :param codeFilePath:
    :param codeLanguage:
    :param limitations:
    :return:
    """
    hostConfig = HostConfig.Config()
    dockerConfig = DockerConfig.Config(evaluationId=evaluationId, problemId=problemId)

    scriptFolderPathSrc = hostConfig.dockerScriptFolderPath
    startScriptFilePath = '{}/{}'.format(dockerConfig.scriptFolderPath, 'script.py')
    destPath = dockerConfig.rootPath
    baseImageName = dockerConfig.evaluatorImageName
    author = 'jiayu1011'

    # sh evaluator.sh // start running evaluator!
    # $1 - evaluationId // E10047
    # $2 - codeFileName // E10047_code.cpp
    # $3 - codeLanguage // C++
    template = 'FROM {}\n'.format(baseImageName) + \
               'MAINTAINER {}\n'.format(author) + \
               f'ADD {codeFileName} {destPath}\n' + \
               f'ADD {problemId}_stdInput.txt {destPath}\n' + \
               f'ADD {problemId}_stdOutput.txt {destPath}\n' + \
               f'ADD {"DockerScript"} {destPath}/{"DockerScript"}\n' + \
               f'CMD python {startScriptFilePath} {evaluationId} {problemId} {codeFileName} {codeLanguage}'


    return template


# if __name__ == '__main__':
#     suffix = '.' + 'E10056_code.py'.split('.')[-1]
#     codeLanguage = getCodeLanguage(suffix)
#     print(codeLanguage)

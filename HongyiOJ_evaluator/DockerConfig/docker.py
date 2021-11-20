import os
import shutil


import HongyiOJ.config as HostConfig
import HongyiOJ_evaluator.DockerConfig.config as DockerConfig
from HongyiOJ.utils import *


def PrepareDocker(evaluationId, limitations):
    os.chdir(HostConfig.Config.dockerPreparedPath)
    os.mkdir(evaluationId)

    os.chdir(HostConfig.Config.dockerPreparedPath + '/' + evaluationId)
    codeFileName = ''
    codeFilePath = ''
    destFilePath = ''
    codeLanguage = ''
    for file in os.listdir(HostConfig.Config.codeSubmitStorePath):
        # Find the exact code file and then copy
        if file.find(evaluationId) != -1:
            source = HostConfig.Config.codeSubmitStorePath + '/' + file
            dest = HostConfig.Config.dockerPreparedPath + '/' + evaluationId
            codeFileName = file
            codeFilePath = source
            destFilePath = dest
            # Copy code
            shutil.copy(source, dest)

            suffix = '.' + codeFileName.split('.')[-1]
            codeLanguage = getCodeLanguage(suffix)

            break

    shutil.copy(HostConfig.Config.dockerScriptPath, destFilePath)


    # create dockerfile
    with open('Dockerfile', 'w') as f:
        f.writelines(
            DockerfileTemplate(
                evaluationId=evaluationId,
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


    # Get docker running result
    """
    docker cmd:
    docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH
    """
    outputFileName = formatOutputFile(evaluationId)
    outputFolderName = formatOutputFolder(evaluationId)
    SRC_PATH = '/Temp/{}'.format(outputFolderName)
    DEST_PATH = ''
    os.system('docker cp {}:{} {}'.format(containerName, SRC_PATH, DEST_PATH))

    # Delete container and image after all
    os.system('docker rm {}'.format(containerName))
    os.system('docker rmi {}'.format(imageName))

    """
    Docker End
    """

    """
    ${evaluationId}_output.txt and standard output already exist 
    """

    """
    Compare output with standard output
    """


    dockerOutputFilePath = os.getcwd() + "\\{}_output.txt".format(evaluationId)


    return dockerOutputFilePath


def DockerfileTemplate(evaluationId, codeFileName, codeFilePath, codeLanguage, limitations) -> str:
    """

    :param evaluationId:
    :param codeFileName:
    :param codeFilePath:
    :param codeLanguage:
    :param limitations:
    :return:
    """

    scriptFilePathSrc = HostConfig.Config.dockerScriptPath
    scriptFilePathDst = DockerConfig.Config.scriptFilePath
    destPath = DockerConfig.Config.tempPath
    baseImageName = DockerConfig.Config.evaluatorImageName
    author = 'jiayu1011'

    # sh evaluator.sh // start running evaluator!
    # $1 - evaluationId // E10047
    # $2 - codeFileName // E10047_code.cpp
    # $3 - codeLanguage // C++
    template = 'FROM {}\n'.format(baseImageName) + \
               'MAINTAINER {}\n'.format(author) + \
               'ADD {} {}\n'.format(codeFileName, destPath) + \
               'ADD {} {}\n'.format(scriptFilePathSrc, destPath) + \
               'CMD python {} {} {} {}'.format(
                   scriptFilePathDst,
                   evaluationId,
                   codeFileName,
                   codeLanguage
               )


    return template


# if __name__ == '__main__':
#     suffix = '.' + 'E10056_code.py'.split('.')[-1]
#     codeLanguage = getCodeLanguage(suffix)
#     print(codeLanguage)

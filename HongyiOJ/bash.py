import os
import shutil
from HongyiOJ.config import *

def PrepareDocker(evaluationId):
    os.chdir(Config.dockerPreparedPath)
    os.mkdir(evaluationId)

    os.chdir(Config.dockerPreparedPath + '/' + evaluationId)
    for file in os.listdir(Config.codeSubmitStorePath):
        # find the exact code file and then copy
        if file.find(evaluationId)!=-1:
            source = Config.codeSubmitStorePath + '/' + file
            dest = Config.dockerPreparedPath + '/' + evaluationId
            shutil.copy(source, dest)

            break



    return


def DockerfileTemplate(codePath, limitOptions):
    temp = 'FROM centos\n' +\
           'MAINTAINER jiayu1011\n' +\
           'CMD '

    return temp

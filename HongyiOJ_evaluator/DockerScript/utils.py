import sys
import HostConfig as HostConfig
def rmEndSpace(filePath):
    with open(filePath, 'r') as f:
        temp = f.read()

    temp = temp.rstrip()
    with open(filePath, 'w') as f:
        f.write(temp)

def checkErr(CEFilePath, REFilePath):
    with open(CEFilePath, 'r') as f:
        errLog = f.read()
        if errLog:
            return HostConfig.Config.COMPILE_ERROR, errLog

    with open(REFilePath, 'r') as f:
        errLog = f.read()
        if errLog:
            return HostConfig.Config.RUNTIME_ERROR, errLog

    return '', ''

if __name__ == '__main__':
    # outputFilePath = sys.argv[1]  # dockerOutput.txt
    # rmEndSpace(outputFilePath)
    a = input()
    print(a)
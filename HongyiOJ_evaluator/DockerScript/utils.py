import sys
import HostConfig
def rmEndSpace(filePath):
    with open(filePath, 'r') as f:
        temp = f.read()

    temp = temp.rstrip()
    with open(filePath, 'w') as f:
        f.write(temp)

def checkCodeErr(
        codeLanguage,
        CEFilePath,
        REFilePath
):
    if codeLanguage in HostConfig.CodeLanguageType.compileLanguages:
        with open(CEFilePath, 'r') as f:
            errLog = f.read()
            if errLog:
                return HostConfig.ResultType.COMPILE_ERROR, errLog

        with open(REFilePath, 'r') as f:
            errLog = f.read()
            if errLog:
                return HostConfig.ResultType.RUNTIME_ERROR, errLog

        return '', ''

    elif codeLanguage in HostConfig.CodeLanguageType.interpretiveLanguages:
        with open(REFilePath, 'r') as f:
            errLog = f.read()
            if errLog:
                return HostConfig.ResultType.RUNTIME_ERROR, errLog

        return '', ''

    else:
        return '', ''



if __name__ == '__main__':
    # outputFilePath = sys.argv[1]  # dockerOutput.txt
    # rmEndSpace(outputFilePath)
    a = input()
    print(a)
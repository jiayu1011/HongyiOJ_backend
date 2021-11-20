import sys
def rmEndSpace(file):
    with open(file, 'r') as f:
        temp = f.read()

    temp = temp.rstrip()
    with open(file, 'w') as f:
        f.write(temp)

if __name__ == '__main__':
    # outputFilePath = sys.argv[1]  # dockerOutput.txt
    # rmEndSpace(outputFilePath)
    a = input()
    print(a)
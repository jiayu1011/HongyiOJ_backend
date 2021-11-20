#!/bin/bash
# $1 - evaluationId  eg. E10047
# $2 - codeFileName  eg. E10047_code.cpp
# $3 - codeLanguage  eg. C++

# shellcheck disable=SC2034
evaluationId=${1}
codeFileName=${2}
codeLanguage=${3}
compileOutput='compileOutput'
javaMainClass='Main'
inputFileName="${evaluationId}_input.txt"
outputFileName="${evaluationId}_output.txt"

cd /Temp || exit

# Some simple actions: compute file size
#du -h "$2" > "$1_result.txt"

# Different code languages

case ${codeLanguage} in
C)
  gcc "${codeFileName}" -o "${compileOutput}"
  ./"${compileOutput} < ${inputFileName} > ${outputFileName}"

  ;;
C++)
  g++ "${codeFileName}" -o "${compileOutput}"
    ./"${compileOutput} < ${inputFileName} > ${outputFileName}"

  ;;
Python3)
  python "${codeFileName}  < ${inputFileName} > ${outputFileName}"

  ;;
Java)
  javac "${codeFileName}"
  java "${javaMainClass}  < ${inputFileName} > ${outputFileName}"

  ;;
esac

echo "Running Complete!"



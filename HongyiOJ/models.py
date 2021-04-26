from django.db import models


# Create your models here.
import datetime


# User
class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    identity = models.CharField(max_length=100, default='user')
    avatarUrl = models.CharField(
        max_length=200,
        default='https://sf1-ttcdn-tos.pstatp.com/img/user-avatar/f4998fe95ef30363f12a04f670579825~300x300.image'
    )
    # Problems which the user has accepted, separated by ','
    acProblems = models.CharField(max_length=1000, default='')


# Problem
class Problem(models.Model):
    problemId = models.CharField(max_length=100, primary_key=True)
    uploader = models.CharField(max_length=100, default='')
    problemName = models.CharField(max_length=100, default='')
    # Tags which describe the algorithm or method that the problem will use
    problemTags = models.CharField(max_length=100, default='')
    # The difficulty of the problem, choosing from 'elementary', 'easy', 'medium' and 'difficult'
    problemDiff = models.CharField(max_length=100, default='')
    # Background description of the problem
    problemBg = models.CharField(max_length=1000, default='')
    problemDes = models.CharField(max_length=5000, default='')
    # Running time limit of the problem, described in millisecond(ms)
    timeLimit = models.FloatField(default=0)
    # Running memory limit of the problem, described in megabyte(MB)
    memoryLimit = models.FloatField(default=0)
    inputFormat = models.CharField(max_length=1000, default='')
    outputFormat = models.CharField(max_length=1000, default='')
    ioExamples = models.CharField(max_length=1000, default='')
    problemTips = models.CharField(max_length=1000, default='')
    dataRange = models.CharField(max_length=1000, default='')
    dataGenerator = models.CharField(max_length=5000, default='')
    stdProgram = models.CharField(max_length=5000, default='')


# Evaluation
class Evaluation(models.Model):
    evaluationId = models.CharField(max_length=100, primary_key=True)  # 从E10000开始, E10001, E10002
    submitter = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    problemId = models.ForeignKey('Problem', to_field='problemId', on_delete=models.CASCADE)
    submitTime = models.DateTimeField(auto_now=True)
    codeLanguage = models.CharField(max_length=100, default='')  # 本项目仅支持C / C++ / Python / Java
    submittedCode = models.CharField(max_length=1000, default='')
    # Running time of the problem, described in millisecond(ms)
    timeCost = models.FloatField(default=0)
    # Running memory of the problem, described in megabyte(MB)
    memoryCost = models.FloatField(default=0)
    '''
    evaluationResult 
    -----
    Accepted 
    Time Limit Exceed 
    Memory Limit Exceed 
    Runtime Error 
    Presentation Error 
    
    '''
    evaluationResult = models.CharField(max_length=100, default='')

    # multi-field unique constraint
    class Meta:
        unique_together = ('submitter', 'problemId', 'submitTime')


# 题解Solution
class Solution(models.Model):
    solutionId = models.CharField(max_length=100, primary_key=True)
    problemId = models.ForeignKey('Problem', to_field='problemId', on_delete=models.CASCADE)
    solutionAuthor = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    updateTime = models.DateTimeField(auto_now=True)
    solutionDes = models.CharField(max_length=1000, default='')  # 题解描述
    solutionCode = models.CharField(max_length=1000, default='')  # 题解代码


# 点赞ThumbsUp
class ThumbsUp(models.Model):
    thumbsUpTime = models.DateTimeField(auto_now=True)
    thumbsUpAuthor = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    solutionId = models.ForeignKey('Solution', to_field='solutionId', on_delete=models.CASCADE)


# 评论Comment
class Comment(models.Model):
    commentTime = models.DateTimeField(auto_now=True)
    commentAuthor = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    solutionId = models.ForeignKey('Solution', to_field='solutionId', on_delete=models.CASCADE)
    commentContent = models.CharField(max_length=500, default='')  # 评论内容


# 比赛Contest
class Contest(models.Model):
    contestId = models.CharField(max_length=100, primary_key=True)



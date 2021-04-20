from django.db import models


# Create your models here.
import datetime


# 用户User
class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    identity = models.CharField(max_length=100, default='user')
    avatarUrl = models.CharField(
        max_length=200,
        default='https://sf1-ttcdn-tos.pstatp.com/img/user-avatar/f4998fe95ef30363f12a04f670579825~300x300.image'
    )
    acceptedCnt = models.IntegerField(default=0)


# 题目Problem
class Problem(models.Model):
    problemId = models.CharField(max_length=100, primary_key=True)
    uploader = models.CharField(max_length=100, default='')
    problemName = models.CharField(max_length=100, default='')
    problemTags = models.CharField(max_length=100, default='')  # 题目标签
    problemDiff = models.CharField(max_length=100, default='')  # 题目难度
    problemBg = models.CharField(max_length=500, default='')  # 题目背景
    problemDes = models.CharField(max_length=500, default='')
    timeLimit = models.CharField(max_length=500, default='')  # 时间限制,以秒为单位
    memoryLimit = models.CharField(max_length=500, default='')  # 内存限制,以MB为单位
    inputFormat = models.CharField(max_length=200, default='')
    outputFormat = models.CharField(max_length=200, default='')
    ioExamples = models.CharField(max_length=200, default='')
    problemTips = models.CharField(max_length=200, default='')
    dataRange = models.CharField(max_length=200, default='')
    dataGenerator = models.CharField(max_length=1000, default='')
    stdProgram = models.CharField(max_length=1000, default='')


# 评测Evaluation
class Evaluation(models.Model):
    evaluationId = models.CharField(max_length=100, primary_key=True)  # 从E10000开始, E10001, E10002
    submitter = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    problemId = models.ForeignKey('Problem', to_field='problemId', on_delete=models.CASCADE)
    submitTime = models.DateTimeField(auto_now=True)
    codeLanguage = models.CharField(max_length=100, default='')  # 本项目仅支持C / C++ / Python / Java
    submittedCode = models.CharField(max_length=1000, default='')
    timeCost = models.FloatField(default=0)  # 以ms毫秒为单位
    memoryCost = models.FloatField(default=0)  # 以MB为单位
    '''
    evaluationResult 运行结果:
    Accepted 运行通过
    Time Limit Exceed 运行时间超出限制
    Memory Limit Exceed 占用内存超出限制
    Runtime Error 运行时错误
    Presentation Error 格式错误
    
    '''
    evaluationResult = models.CharField(max_length=100, default='')

    # 多字段联合约束
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



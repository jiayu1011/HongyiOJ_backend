from django.db import models


# Create your models here.


# 用户User
class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    avatarUrl = models.CharField(
        max_length=200,
        default='https://sf1-ttcdn-tos.pstatp.com/img/user-avatar/f4998fe95ef30363f12a04f670579825~300x300.image'
    )
    acceptedCnt = models.IntegerField(default=0)


# 题目Problem
class Problem(models.Model):
    problemId = models.CharField(max_length=100, primary_key=True)
    problemName = models.CharField(max_length=100)
    problemTags = models.CharField(max_length=100)  # 题目标签
    problemDiff = models.CharField(max_length=100)  # 题目难度
    problemBg = models.CharField(max_length=500)  # 题目背景
    problemDes = models.CharField(max_length=500)
    timeLimit = models.FloatField()  # 时间限制,以秒为单位
    memoryLimit = models.FloatField()  # 内存限制,以MB为单位
    inputFormat = models.CharField(max_length=200)
    outputFormat = models.CharField(max_length=200)
    inputExample = models.CharField(max_length=200)
    outputExample = models.CharField(max_length=200)
    problemTips = models.CharField(max_length=200)
    dataRange = models.CharField(max_length=200)
    dataGenerator = models.CharField(max_length=1000)
    stdProgram = models.CharField(max_length=1000)


# 评测Evaluation
class Evaluation(models.Model):
    evaluationId = models.CharField(max_length=100, primary_key=True)  # 从E10000开始, E10001, E10002
    submitter = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    problemId = models.ForeignKey('Problem', to_field='problemId', on_delete=models.CASCADE)
    submitTime = models.DateTimeField()
    codeLanguage = models.CharField(max_length=100)  # 本项目仅支持C / C++ / Python / Java
    submittedCode = models.CharField(max_length=1000)
    timeCost = models.FloatField()  # 以ms毫秒为单位
    memoryCost = models.FloatField()  # 以MB为单位
    '''
    evaluationResult 运行结果:
    Accepted 运行通过
    Time Limit Exceed 运行时间超出限制
    Memory Limit Exceed 占用内存超出限制
    Runtime Error 运行时错误
    Presentation Error 格式错误
    
    '''
    evaluationResult = models.CharField(max_length=100)

    # 多字段联合约束
    class Meta:
        unique_together = ('submitter', 'problemId', 'submitTime')


# 题解Solution
class Solution(models.Model):
    solutionId = models.CharField(max_length=100, primary_key=True)
    problemId = models.ForeignKey('Problem', to_field='problemId', on_delete=models.CASCADE)
    solutionAuthor = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    updateTime = models.DateTimeField()
    solutionDes = models.CharField(max_length=1000)  # 题解描述
    solutionCode = models.CharField(max_length=1000)  # 题解代码


# 点赞ThumbsUp
class ThumbsUp(models.Model):
    thumbsUpTime = models.DateTimeField()
    thumbsUpAuthor = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    solutionId = models.ForeignKey('Solution', to_field='solutionId', on_delete=models.CASCADE)


# 评论Comment
class Comment(models.Model):
    commentTime = models.DateTimeField()
    commentAuthor = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    solutionId = models.ForeignKey('Solution', to_field='solutionId', on_delete=models.CASCADE)
    commentContent = models.CharField(max_length=500)  # 评论内容


# 比赛Contest
# class Contest(models.Model):
#     contestId = models.CharField(max_length=100, primary_key=True)


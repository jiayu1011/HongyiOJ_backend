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
        default='http://119.29.24.77:8000/sources/HongyiOJ/image/hongyi_logo.png'
    )
    # Problems which the user has accepted, separated by ','
    acProblems = models.CharField(max_length=1000, default='')
    collectedProblems = models.CharField(max_length=1000, default='')


# Problem
class Problem(models.Model):
    problemId = models.CharField(max_length=100, primary_key=True)
    uploader = models.CharField(max_length=100, default='')
    problemName = models.CharField(max_length=100, default='')
    # Tags which describe the algorithm or method that the problem will use
    problemTags = models.CharField(max_length=100, default='')

    '''
    The difficulty of the problem, choosing from
    -----
    'elementary'
    'easy'
    'medium'
    'difficult'
    '''
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
    stdInput = models.CharField(max_length=5000, default='')
    stdOutput = models.CharField(max_length=5000, default='')

    '''
    Status in problem reviewing, choosing from
    -----
    'reviewing'
    'disapproved' 
    'approved'
    '''
    reviewStatus = models.CharField(max_length=100, default='reviewing')


# Evaluation
class Evaluation(models.Model):
    evaluationId = models.CharField(max_length=100, primary_key=True)  # Start from E10000, then E10001, E10002..
    author = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE, default='')
    relatedProblemId = models.ForeignKey('Problem', to_field='problemId', on_delete=models.CASCADE, default='')
    submitTime = models.DateTimeField(auto_now=True)
    # HongyiOJ only support evaluating C / C++ / Python / Java
    codeLanguage = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=1000, default='')
    codeLength = models.IntegerField(default=0)
    # Running time of the problem, described in millisecond(ms)
    timeCost = models.FloatField(default=0)
    # Running memory of the problem, described in megabyte(MB)
    memoryCost = models.FloatField(default=0)

    '''
    evaluationResult, choosing from
    -----
    'Queuing'
    'Accepted' 
    'Time Limit Exceed' 
    'Memory Limit Exceed' 
    'Compile Error'
    'Runtime Error' 
    'Presentation Error'
    'Wrong Answer'
    '''
    result = models.CharField(max_length=100, default='Queuing')
    errLog = models.CharField(max_length=2000, default='')

    # multi-field unique constraint
    class Meta:
        unique_together = ('author', 'relatedProblemId', 'submitTime')


# 题解Discussion
class Discussion(models.Model):
    discussionId = models.CharField(max_length=100, primary_key=True)
    postTime = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE, default='')
    relatedProblemId = models.ForeignKey('Problem', to_field='problemId', on_delete=models.CASCADE, default='')
    content = models.CharField(max_length=5000, default='')


# 点赞ThumbsUp
class ThumbsUp(models.Model):
    thumbsUpTime = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    relatedDiscussionId = models.ForeignKey('Discussion', to_field='discussionId', on_delete=models.CASCADE, default='')



# 评论Comment
class Comment(models.Model):
    postTime = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    relatedDiscussionId = models.ForeignKey('Discussion', to_field='discussionId', on_delete=models.CASCADE, default='')
    content = models.CharField(max_length=500, default='')  # 评论内容


# 比赛Contest
class Contest(models.Model):
    contestId = models.CharField(max_length=100, primary_key=True)
    contestName = models.CharField(max_length=200, default='')
    organizer = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE, default='')
    startTime = models.DateTimeField(auto_now=True)
    endTime = models.DateTimeField(auto_now=True)
    problemList = models.CharField(max_length=1000, default='')

    '''
    Status in contest reviewing, choosing from
    -----
    'reviewing'
    'disapproved' 
    'approved'
    '''
    reviewStatus = models.CharField(max_length=100, default='reviewing')






"""HongyiOJ_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from HongyiOJ import views

basicUrl = 'HongyiOJ'


urlpatterns = [
    path('admin/', admin.site.urls),

    # User related APIs
    path('{}/'.format(basicUrl), views.test),
    path('{}/login'.format(basicUrl), views.login),
    path('{}/register'.format(basicUrl), views.register),
    path('{}/reset/password'.format(basicUrl), views.resetPassword),
    path('{}/logout'.format(basicUrl), views.logout),
    path('{}/verify/code'.format(basicUrl), views.getVerifyCode),
    path('{}/verify'.format(basicUrl), views.verify),

    # Problem related APIs
    path('{}/list/problem'.format(basicUrl), views.getProblemList),
    path('{}/upload/problem'.format(basicUrl), views.uploadProblem),




    # Contest related APIs

    # Discussion related APIs

    # Evaluation related APIs
    path('{}/submit/code'.format(basicUrl), views.submitCode),
    path('{}/list/evaluation'.format(basicUrl), views.getEvaluationList),

    # Manage related APIs
    path('{}/review/problem'.format(basicUrl), views.reviewProblem),
    path('{}/delete/problem'.format(basicUrl), views.deleteProblem),






]


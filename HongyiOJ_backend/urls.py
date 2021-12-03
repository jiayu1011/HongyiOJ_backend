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
    path(f'{basicUrl}/', views.test),
    path(f'{basicUrl}/login', views.login),
    path(f'{basicUrl}/register', views.register),
    path(f'{basicUrl}/reset/password', views.resetPassword),
    path(f'{basicUrl}/logout', views.logout),
    path(f'{basicUrl}/verify/code', views.getVerifyCode),
    path(f'{basicUrl}/verify', views.verify),

    # Problem related APIs
    path(f'{basicUrl}/list/problem', views.getProblemList),
    path(f'{basicUrl}/upload/problem', views.uploadProblem),




    # Contest related APIs

    # Discussion related APIs

    # Evaluation related APIs
    path(f'{basicUrl}/submit/code', views.submitCode),
    path(f'{basicUrl}/list/evaluation', views.getEvaluationList),

    # Manage related APIs
    path(f'{basicUrl}/review/problem', views.reviewProblem),
    path(f'{basicUrl}/delete/problem', views.deleteProblem),






]


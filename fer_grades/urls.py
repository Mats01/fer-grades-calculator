"""fer_grades URL Configuration

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
from .views import AddPredmetView, HomeView, MyPredmetiView, SignupView, UpdatePointsView
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',
         auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='change-password.html'),
        name='password_reset'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('add-predmet/<id>/', AddPredmetView.as_view()),
    path('moj-predmeti/', MyPredmetiView.as_view(), name='moj-predmeti'),
    path('moj-predmeti/update/<id>', UpdatePointsView.as_view()),
    path('', HomeView.as_view(), name='home'),

]

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
from .views import AddPredmetView, DeletePointsView, HomeView, MyPredmetiView, PreLoginView, SignupView, UpdatePointsView, LoginView, logout_view
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', PreLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('login/code/', LoginView.as_view()),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='change-password.html'),
        name='password_reset'),
    path('signup/', SignupView.as_view(), name='signup'),

    path('add-predmet/<id>/', login_required(AddPredmetView.as_view())),
    path('', login_required(MyPredmetiView.as_view()),
         name='moj-predmeti'),
    path('moj-predmeti/update/<id>', login_required(UpdatePointsView.as_view())),
    path('moj-predmeti/delete/<id>', login_required(DeletePointsView.as_view())),
    path('dodaj-predmet/', login_required(HomeView.as_view()), name='home'),

]

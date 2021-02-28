
from .forms import CodeAuthForm, EmailAuthForm, StudentKomponentaBodoviForm
from django import shortcuts
from .models import KomponentaBodovi, Predmet, Student, StudentPredmet
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import uuid

from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist


def get_or_create_user(email):
    try:

        user = User.objects.get(email=email)

    except ObjectDoesNotExist:
        username = email.split("@")[0]
        user = User.objects.create_user(email=email, username=username)
        user.save()

    return user


def logout_view(request):
    logout(request)
    return redirect('login')


class SignupView(TemplateView):
    template_name = "signup.html"

    def get(self, request):

        form = UserCreationForm()
        return render(request, self.template_name, {'form': form, })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
        else:
            return redirect('signup')


class PreLoginView(TemplateView):
    template_name = 'prelogin.html'

    def get(self, request):

        form = EmailAuthForm()
        return render(request, self.template_name, {'form': form, })

    def post(self, request):
        form = EmailAuthForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')

            code = uuid.uuid4().hex[:6].upper()

            user = get_or_create_user(email)

            try:
                student = user.student
            except ObjectDoesNotExist:
                student = Student(user=user)
                student.save()
            student = user.student
            student.login_code = code
            student.save()

            send_mail(
                'Bok',
                'Vas kod je %s' % code,
                'fer-grades@farmoredifferent.com',
                [email],
                fail_silently=False,
            )

            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('/login/code/?email=%s' % email)

        else:
            print("invalid form")
            return redirect('login')


class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, request):

        form = CodeAuthForm(initial={'email': request.GET['email']})
        return render(request, self.template_name, {'form': form, })

    def post(self, request):
        form = CodeAuthForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')
            code = form.cleaned_data.get('code')

            try:

                user = authenticate(email=email, code=code)

                login(request, user,
                      backend='fer_grades.auth_backend.PasswordlessAuthBackend')
                return redirect('home')

            except ObjectDoesNotExist:
                return redirect('login')

        else:
            return redirect('login')


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request):

        predmeti = Predmet.objects.all()

        return render(request, self.template_name, {'predmeti': predmeti})


class AddPredmetView(TemplateView):

    def get(self, request, id):

        predmet = Predmet.objects.get(pk=id)

        student_predmet = StudentPredmet()
        student_predmet.student = request.user.student
        student_predmet.predmet = predmet

        student_predmet.save()

        return redirect('home')


class MyPredmetiView(TemplateView):
    template_name = "moj-predmeti.html"

    def get(self, request):

        predmeti = StudentPredmet.objects.filter(student=request.user.student)
        predmeti_list = []
        for predmet in predmeti:
            components = []
            ukupno = 0
            for component in predmet.predmet.komponenta_set.all():
                points = 0
                for bodovi in component.komponentabodovi_set.filter(predmet=predmet):
                    points += bodovi.points_collected
                components.append({
                    "name": component.name,
                    "points": points,
                    "max_points": component.max_points,
                    "prag": component.max_points * component.prag,
                })
                if points >= component.prag * component.max_points:
                    ukupno += points

            points_from = StudentKomponentaBodoviForm(
                initial={'predmet': predmet})

            grade = 1
            if ukupno > predmet.predmet.dovoljan:
                grade += 1
            if ukupno > predmet.predmet.dobar:
                grade += 1
            if ukupno > predmet.predmet.vrlo_dobar:
                grade += 1
            if ukupno > predmet.predmet.odlican:
                grade += 1

            predmeti_list.append({
                'predmet': predmet,
                "form": points_from,
                'komponente': components,
                'points': ukupno,
                'grade': grade,
            })

        return render(request, self.template_name, {'predmeti': predmeti_list})


class UpdatePointsView(TemplateView):

    def post(self, request, id):

        form = StudentKomponentaBodoviForm(request.POST)

        if form.is_valid():

            komp = form.save()

            return redirect('moj-predmeti')
        else:
            return redirect('moj-predmeti')


class DeletePointsView(TemplateView):

    def get(self, request, id):

        KomponentaBodovi.objects.get(pk=id).delete()
        return redirect('moj-predmeti')

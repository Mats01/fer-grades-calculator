from .forms import StudentKomponentaBodoviForm
from django import shortcuts
from .models import KomponentaBodovi, Predmet, Student, StudentPredmet
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.views.generic import TemplateView


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

        for komponenta in predmet.komponenta_set.all():
            realizirana_komponenta = KomponentaBodovi()
            realizirana_komponenta.komponenta = komponenta
            realizirana_komponenta.points_collected = 0
            realizirana_komponenta.predmet = student_predmet
            realizirana_komponenta.save()

        return redirect('home')


class MyPredmetiView(TemplateView):
    template_name = "moj-predmeti.html"

    def get(self, request):

        predmeti = StudentPredmet.objects.filter(student=request.user.student)
        predmeti_list = []
        for predmet in predmeti:
            forms = []
            points = 0
            for komp in predmet.komponentabodovi_set.all():
                points += komp.points_collected
                forms.append({
                    'form': StudentKomponentaBodoviForm(instance=komp),
                    'component': komp,
                    'id': komp.id,
                })
            predmeti_list.append({
                'predmet': predmet,
                'forms': forms,
                'points': points,
            })

        return render(request, self.template_name, {'predmeti': predmeti_list})


class UpdatePointsView(TemplateView):

    def post(self, request, id):

        komp = KomponentaBodovi.objects.get(pk=id)

        form = StudentKomponentaBodoviForm(request.POST, instance=komp)

        if form.is_valid():
            form.save()
            return redirect('moj-predmeti')

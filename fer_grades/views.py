
from django.contrib.auth import forms
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory
from .forms import CodeAuthForm, EditPredmetForm, EmailAndPassAuthForm, EmailAuthForm, PredmetForm, StudentKomponentaBodoviForm
from django import shortcuts
from .models import Komponenta, KomponentaBodovi, Predmet, Student, StudentPredmet, Uvjeti
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import uuid

from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from .fer_scraper import get_predmet_data


def get_or_create_user(email, password):
    try:

        user = User.objects.get(email=email)

    except ObjectDoesNotExist:
        username = email.split("@")[0]
        user = User.objects.create_user(
            email=email, username=username, password=password)
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


class OLDPreLoginView(TemplateView):
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
                'matej.butkovic@fer.hr',
                [email],
                fail_silently=False,
            )

            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('/login/code/?email=%s' % email)

        else:
            print("invalid form")
            return redirect('login')


class PreLoginView(TemplateView):
    template_name = 'prelogin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('moj-predmeti')

        form = EmailAndPassAuthForm()
        return render(request, self.template_name, {'form': form, })

    def post(self, request):
        form = EmailAndPassAuthForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = get_or_create_user(email, password)

            try:
                student = user.student
            except ObjectDoesNotExist:
                student = Student(user=user)
                student.save()

            user = authenticate(username=user.username, password=password)
            try:
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
            except AttributeError:
                return render(request, self.template_name, {'form': form, 'login_error': 'Kriva lozinka'})

            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('moj-predmeti')

        else:
            return render(request, self.template_name, {'form': form, })


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
                return redirect('moj-predmeti')

            except ObjectDoesNotExist:
                return redirect('login')

        else:
            return redirect('login')


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request):

        predmeti = Predmet.objects.all()

        return render(request, self.template_name, {'predmeti': predmeti})


class AddToMyPredmetiView(TemplateView):

    def get(self, request, id):

        predmet = Predmet.objects.get(pk=id)
        try:
            student_predmet = StudentPredmet.objects.filter(
                predmet=predmet, student=request.user.student)
            if student_predmet:
                return redirect('predmet-list')
        except:
            pass

        student_predmet = StudentPredmet()
        student_predmet.student = request.user.student
        student_predmet.predmet = predmet

        student_predmet.save()

        return redirect('predmet-list')


class DeleteStudentPredmetiView(TemplateView):

    def get(self, request, id):
        try:
            predmet = StudentPredmet.objects.get(pk=id)

            predmet.delete()
        except ObjectDoesNotExist:
            pass

        return redirect('moj-predmeti')


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
        prosjek = 0.0
        if len(predmeti_list) > 0:

            for predmet in predmeti_list:
                prosjek += predmet['grade']
            prosjek = prosjek / len(predmeti_list)

        return render(request, self.template_name, {'predmeti': predmeti_list, 'prosjek': prosjek})


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


class AddPredmetView(TemplateView):
    template_name = "new-predmet.html"

    def get(self, request):

        form = PredmetForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request,):

        form = PredmetForm(request.POST)

        if form.is_valid():
            predmet = form.save(commit=False)
            predmet.created_by = User.objects.get(pk=request.user.id)

            predmet_data = get_predmet_data(predmet.fer_url)

            """
                {'komponente': [{'bodovi': '20', 'ime': 'Domaće zadaće', 'prag': '0'},
                    {'bodovi': '10', 'ime': 'Sudjelovanje u nastavi', 'prag': '0'},
                    {'bodovi': '30', 'ime': 'Međuispit: Pismeni', 'prag': '0'},
                    {'bodovi': '40', 'ime': 'Završni ispit: Pismeni', 'prag': '0'}],
                'ocjenjivanje': {'dobar': '60',
                                'dovoljan': '50',
                                'odlican': '90',
                                'vrlo_dobar': '75'}}
                """

            predmet.dovoljan = predmet_data['ocjenjivanje']['dovoljan']
            predmet.dobar = predmet_data['ocjenjivanje']['dobar']
            predmet.vrlo_dobar = predmet_data['ocjenjivanje']['vrlo_dobar']
            predmet.odlican = predmet_data['ocjenjivanje']['odlican']
            predmet.save()

            for comp in predmet_data['komponente']:
                component = Komponenta(
                    name=comp['ime'],
                    predmet=predmet,
                    max_points=comp['bodovi'],
                    prag=float(comp['prag'])/100.0)
                component.save()

            predmet.save()

            return redirect('/dodaj-predmet/new/%s/' % predmet.pk)
        else:
            return render(request, self.template_name, {'form': form})


class EditPredmetView(TemplateView):
    template_name = "edit-predmet.html"

    def get(self, request, id):

        predmet = Predmet.objects.get(pk=id)
        if not predmet.created_by:
            return redirect('new-predmet')

        if not (predmet.created_by.id == request.user.id):
            return redirect('new-predmet')

        KomponentaFormSet = inlineformset_factory(
            Predmet, Komponenta, exclude=(), extra=3)

        komponente_formset = KomponentaFormSet(instance=predmet)

        UvjetiFormSet = inlineformset_factory(
            Predmet, Uvjeti, exclude=(), extra=1)

        uvjeti_formset = UvjetiFormSet(instance=predmet)

        form = EditPredmetForm(instance=predmet)

        return render(request, self.template_name, {'predmet': predmet, 'form': form, 'komponente_formset': komponente_formset, 'uvjeti_formset': uvjeti_formset})

    def post(self, request, id):

        predmet = Predmet.objects.get(pk=id)
        form = EditPredmetForm(request.POST, instance=predmet)

        if form.is_valid():
            form.save()

        return redirect('/dodaj-predmet/new/%s/' % predmet.pk)


class UpdatePredemetUvjetiView(TemplateView):
    def post(self, request, id):

        UvjetiFormSet = inlineformset_factory(
            Predmet, Uvjeti, exclude=(), extra=1)

        predmet = Predmet.objects.get(pk=id)

        form = UvjetiFormSet(request.POST, instance=predmet)

        if form.is_valid():
            form.save()

        return redirect('/dodaj-predmet/new/%s/' % predmet.pk)


class UpdatePredemetKomponenteView(TemplateView):
    def post(self, request, id):

        KomponentaFormSet = inlineformset_factory(
            Predmet, Komponenta, exclude=(), extra=1)
        predmet = Predmet.objects.get(pk=id)

        form = KomponentaFormSet(request.POST, instance=predmet)

        if form.is_valid():
            form.save()

        return redirect('/dodaj-predmet/new/%s/' % predmet.pk)

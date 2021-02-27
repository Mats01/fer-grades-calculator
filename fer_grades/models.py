from django.db import models
from django.contrib.auth.models import User


class Predmet(models.Model):

    name = models.CharField(max_length=100)
    fer_url = models.CharField(max_length=60, unique=True)

    class Meta:
        verbose_name_plural = "Predmeti"

    def __str__(self):
        return self.name


class Komponenta(models.Model):
    name = models.CharField(max_length=200)
    predmet = models.ForeignKey(Predmet, on_delete=models.CASCADE)
    max_points = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Komponente"

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class StudentPredmet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmet, on_delete=models.CASCADE)

    def __str__(self):
        return self.predmet.name


class KomponentaBodovi(models.Model):
    komponenta = models.ForeignKey(Komponenta, on_delete=models.CASCADE)
    predmet = models.ForeignKey(StudentPredmet, on_delete=models.CASCADE)
    points_collected = models.FloatField(default=0)

from django.contrib import admin

from .models import *


class KomponentaInline(admin.TabularInline):
    model = Komponenta


class StudentPredmetInline(admin.TabularInline):
    model = StudentPredmet


@admin.register(Predmet)
class PredmetAdmin(admin.ModelAdmin):
    inlines = [
        KomponentaInline,
    ]


@admin.register(Komponenta)
class KomponentaAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [
        StudentPredmetInline,
    ]

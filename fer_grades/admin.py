from django.contrib import admin

from .models import *


class KomponentaInline(admin.TabularInline):
    model = Komponenta


class UvjetiInline(admin.TabularInline):
    model = Uvjeti


class StudentPredmetInline(admin.TabularInline):
    model = StudentPredmet


@admin.register(Predmet)
class PredmetAdmin(admin.ModelAdmin):
    inlines = [
        KomponentaInline,
        UvjetiInline,
    ]


@admin.register(Komponenta)
class KomponentaAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [
        StudentPredmetInline,
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.student.id)


@admin.register(StudentPredmet)
class StudentPredmetAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(student=request.user.student)


@admin.register(KomponentaBodovi)
class KomponentaBodoviAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(predmet__student=request.user.student)

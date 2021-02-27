# Generated by Django 3.1.7 on 2021-02-26 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fer_grades', '0002_auto_20210226_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentPredmet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predmet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fer_grades.predmet')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fer_grades.student')),
            ],
        ),
    ]

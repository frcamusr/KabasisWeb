# Generated by Django 4.2.6 on 2023-11-22 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CursosApp', '0015_questioncontent_curso_questioncontent_unidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questioncontent',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='questioncontent',
            name='unidad',
        ),
    ]

# Generated by Django 3.2.22 on 2023-11-15 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CursosApp', '0005_delete_contenidocontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='imagen',
            field=models.ImageField(default=1, upload_to='cursos'),
            preserve_default=False,
        ),
    ]

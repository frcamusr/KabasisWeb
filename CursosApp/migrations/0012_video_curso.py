# Generated by Django 4.2.6 on 2023-11-21 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CursosApp', '0011_quizcontent_descripcion_quizcontent_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='curso',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='CursosApp.curso'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.2.22 on 2023-12-21 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutenticacionApp', '0011_alter_empresa_nombre_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='tipo_usuario',
            field=models.CharField(blank=True, choices=[('', 'Selecciona el tipo de usuario'), ('Administrador', 'Administrador'), ('Alumno', 'Alumno'), ('Administrador Kabasis', 'Administrador Kabasis')], default='', max_length=50, verbose_name='Tipo de Usuario'),
        ),
    ]

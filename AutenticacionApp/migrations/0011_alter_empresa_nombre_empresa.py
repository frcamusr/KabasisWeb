# Generated by Django 3.2.22 on 2023-12-20 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutenticacionApp', '0010_auto_20231220_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='nombre_empresa',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]

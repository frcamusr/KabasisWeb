# Generated by Django 4.2.5 on 2023-11-08 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutenticacionApp', '0007_alter_customuser_tipo_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='empresa',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]

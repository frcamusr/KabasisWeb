# Generated by Django 4.2.6 on 2023-11-21 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CursosApp', '0010_quizcontent_orden_video_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizcontent',
            name='descripcion',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quizcontent',
            name='titulo',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-20 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0004_alter_subject_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='descr',
            field=models.TextField(null=True, verbose_name='Додаткова інформація'),
        ),
        migrations.AddField(
            model_name='subject',
            name='upload',
            field=models.FileField(default=None, upload_to=None),
        ),
    ]

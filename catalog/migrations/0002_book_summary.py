# Generated by Django 2.2 on 2020-05-22 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='summary',
            field=models.TextField(default='values'),
        ),
    ]

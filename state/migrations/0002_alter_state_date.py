# Generated by Django 4.2.1 on 2023-06-09 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('state', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

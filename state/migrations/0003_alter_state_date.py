# Generated by Django 4.2.1 on 2023-06-09 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('state', '0002_alter_state_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]

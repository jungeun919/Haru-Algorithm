# Generated by Django 3.2.6 on 2022-08-07 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='current_date',
            field=models.DateField(null=True),
        ),
    ]
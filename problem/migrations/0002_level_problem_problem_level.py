# Generated by Django 4.0.6 on 2022-08-14 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bronze', models.TextField(null=True)),
                ('silver', models.TextField(null=True)),
                ('gold', models.TextField(null=True)),
                ('platinum', models.TextField(null=True)),
                ('diamond', models.TextField(null=True)),
                ('ruby', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='problem_level',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
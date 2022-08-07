# Generated by Django 4.0.6 on 2022-08-07 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_date', models.DateField(null=True)),
                ('problem_num', models.IntegerField(null=True, unique=True)),
                ('problem_category', models.CharField(max_length=30, null=True)),
                ('problem_title', models.TextField(null=True)),
                ('problem_text', models.TextField(blank=True, null=True)),
                ('problem_input', models.TextField(null=True)),
                ('problem_output', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('example_input', models.TextField(null=True)),
                ('example_output', models.TextField(null=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.problem')),
            ],
        ),
    ]
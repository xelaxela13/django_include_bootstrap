# Generated by Django 3.0.2 on 2020-01-12 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IncludeBootstrap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library', models.CharField(choices=[('1', 'Bootstrap Js'), ('2', 'Jquery'), ('3', 'Popover Js'), ('4', 'Bootstrap Css')], max_length=32)),
                ('version', models.CharField(max_length=8)),
                ('integrity', models.CharField(max_length=255)),
                ('url', models.URLField(verbose_name='Library cdn url')),
                ('url_pattern', models.CharField(help_text='Should be string like - https://code.jquery.com/jquery-{version}.js, {version} is a variable that will be replaced with values from "version" field', max_length=512)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]

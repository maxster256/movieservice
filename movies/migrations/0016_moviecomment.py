# Generated by Django 2.1.7 on 2019-02-21 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_auto_20190221_0918'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Comment', models.TextField()),
                ('Movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CommentedMovie', to='movies.Movie')),
            ],
        ),
    ]

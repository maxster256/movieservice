# Generated by Django 2.1.7 on 2019-02-22 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0022_auto_20190222_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviecomment',
            name='commented_movie_id',
        ),
        migrations.AddField(
            model_name='moviecomment',
            name='movie',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='movies.Movie'),
            preserve_default=False,
        ),
    ]

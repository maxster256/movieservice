# Generated by Django 2.1.7 on 2019-02-20 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20190220_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movierating',
            name='RatedMovie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MovieRatings', to='movies.Movie'),
        ),
    ]

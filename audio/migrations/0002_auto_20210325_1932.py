# Generated by Django 3.1.7 on 2021-03-25 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audiobook',
            options={'verbose_name': 'Audio Book', 'verbose_name_plural': 'Audio Books'},
        ),
        migrations.AlterModelOptions(
            name='podcast',
            options={'verbose_name': 'Podcast', 'verbose_name_plural': 'Podcasts'},
        ),
        migrations.AlterModelOptions(
            name='song',
            options={'verbose_name': 'Song', 'verbose_name_plural': 'Songs'},
        ),
    ]

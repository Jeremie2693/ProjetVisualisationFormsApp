# Generated by Django 4.1.6 on 2023-02-21 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_alter_band_genre_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Csv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='csvs')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='listing',
            name='band',
        ),
        migrations.DeleteModel(
            name='Band',
        ),
        migrations.DeleteModel(
            name='Listing',
        ),
    ]
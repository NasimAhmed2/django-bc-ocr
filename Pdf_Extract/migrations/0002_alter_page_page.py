# Generated by Django 5.0.1 on 2024-02-06 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pdf_Extract', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page',
            field=models.FileField(upload_to='pdf_pages/'),
        ),
    ]

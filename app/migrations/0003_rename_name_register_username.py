# Generated by Django 5.0.1 on 2024-05-06 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_register'),
    ]

    operations = [
        migrations.RenameField(
            model_name='register',
            old_name='name',
            new_name='username',
        ),
    ]
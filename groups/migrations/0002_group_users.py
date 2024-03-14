# Generated by Django 5.0.1 on 2024-03-13 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('users', '0002_remove_user_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(related_name='groups', to='users.user'),
        ),
    ]
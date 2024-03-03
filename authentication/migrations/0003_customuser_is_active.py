# Generated by Django 5.0.1 on 2024-03-02 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_customuser_groups_customuser_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Permission whether user is treated as active. Unselect this instead of deleting accounts', verbose_name='active'),
        ),
    ]
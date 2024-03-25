# Generated by Django 5.0.3 on 2024-03-21 23:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
        ('task_templates', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('label', models.CharField(choices=[('Personal', 'Personal'), ('Family', 'Family'), ('Work', 'Work'), ('Academic', 'Academic'), ('Other', 'Other')], default='Personal', max_length=50)),
                ('status', models.CharField(choices=[('To Do', 'Todo'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='To Do', max_length=12)),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low', max_length=6, null=True)),
                ('effort', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low', max_length=6, null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='groups.group')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_templates.tasktemplate')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

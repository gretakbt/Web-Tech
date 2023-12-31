# Generated by Django 4.2.7 on 2024-01-04 17:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll', '0002_alter_poll_id'),
        ('todolist', '0002_task_delete_todolist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('members', models.ManyToManyField(related_name='group_memberships', to=settings.AUTH_USER_MODEL)),
                ('polls', models.ManyToManyField(blank=True, related_name='groups_polls', to='poll.poll')),
            ],
        ),
    ]

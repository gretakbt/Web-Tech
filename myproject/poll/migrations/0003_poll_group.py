# Generated by Django 4.2.7 on 2024-01-04 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_group'),
        ('poll', '0002_alter_poll_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_polls', to='todolist.group'),
        ),
    ]

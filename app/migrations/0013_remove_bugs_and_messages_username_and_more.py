# Generated by Django 4.2.2 on 2023-09-23 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_bugs_and_messages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bugs_and_messages',
            name='username',
        ),
        migrations.AddField(
            model_name='bugs_and_messages',
            name='mail',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='bugs_and_messages',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bugs_and_messages',
            name='message',
            field=models.CharField(blank=True, max_length=99999, null=True),
        ),
    ]

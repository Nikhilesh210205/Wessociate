# Generated by Django 4.2.6 on 2023-10-16 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_bugs_and_messages_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='idea_industry',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

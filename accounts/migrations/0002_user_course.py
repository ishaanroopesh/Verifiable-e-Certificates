# Generated by Django 4.2.6 on 2023-11-27 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='course',
            field=models.CharField(blank=True, choices=[('option1', 'Computer Science: Programming with a Purpose'), ('option2', 'Python for Everbody Specialization')], max_length=255, null=True),
        ),
    ]
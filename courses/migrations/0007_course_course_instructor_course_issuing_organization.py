# Generated by Django 4.2.6 on 2024-01-02 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_rename_length_hours_course_course_length_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_instructor',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='course',
            name='issuing_organization',
            field=models.CharField(default='', max_length=256),
        ),
    ]

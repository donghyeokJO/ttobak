# Generated by Django 3.0.8 on 2020-10-28 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_apis', '0042_student_ic'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='activated',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='activated',
            field=models.CharField(max_length=1, null=True),
        ),
    ]

# Generated by Django 3.0.3 on 2020-03-29 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SSV', '0003_auto_20200329_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_emial',
            field=models.EmailField(default=False, max_length=254),
        ),
    ]

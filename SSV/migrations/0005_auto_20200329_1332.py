# Generated by Django 3.0.3 on 2020-03-29 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SSV', '0004_auto_20200329_1315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='student_emial',
            new_name='student_email',
        ),
    ]

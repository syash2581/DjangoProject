# Generated by Django 3.0.3 on 2020-03-29 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SSV', '0008_auto_20200329_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='subject_id',
            field=models.AutoField(default=None, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='voted',
            name='student_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='SSV.Student'),
        ),
        migrations.AlterField(
            model_name='voted',
            name='subject_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='SSV.Subject'),
        ),
    ]

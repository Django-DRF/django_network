# Generated by Django 4.0.4 on 2022-04-22 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_add_subtitle_field_to_Userprofile_model_and_set_default_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='subtitle',
            field=models.CharField(default='Default subtitle text', max_length=25),
        ),
    ]

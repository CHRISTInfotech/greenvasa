# Generated by Django 4.0.4 on 2022-05-26 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign_up_in', '0002_alter_g_sign_up_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='g_sign_up',
            name='mobile_number',
            field=models.CharField(max_length=12),
        ),
    ]

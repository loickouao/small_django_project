# Generated by Django 3.0.6 on 2020-05-14 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bridger', '0009_auto_20200514_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='content_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

# Generated by Django 2.2.10 on 2020-04-25 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('admin', 'admin'), ('member', 'member')], default='member', max_length=6),
        ),
    ]
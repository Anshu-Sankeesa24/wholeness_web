# Generated by Django 4.0.1 on 2022-05-09 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0007_user_detail_adult'),
    ]

    operations = [
        migrations.CreateModel(
            name='week_weight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.FloatField(max_length=20)),
                ('weight', models.FloatField(max_length=20)),
            ],
        ),
    ]

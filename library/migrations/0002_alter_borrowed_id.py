# Generated by Django 3.2 on 2021-04-24 14:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowed',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=3000, primary_key=True, serialize=False),
        ),
    ]

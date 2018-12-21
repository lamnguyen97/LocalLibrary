# Generated by Django 2.1.4 on 2018-12-21 04:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('locallibrary', '0002_auto_20181221_1022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('a099acb6-b00e-42df-a9f6-13b8efd8f281'), primary_key=True, serialize=False),
        ),
    ]
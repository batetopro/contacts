# Generated by Django 4.1.6 on 2023-02-26 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_email_contact_emails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='value',
            field=models.EmailField(editable=False, max_length=254, unique=True),
        ),
    ]

# Generated by Django 2.1.5 on 2019-04-15 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='content_type',
            field=models.CharField(help_text='The MIMEType of the file', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='cat',
            name='picture',
            field=models.BinaryField(editable=True, null=True),
        ),
    ]
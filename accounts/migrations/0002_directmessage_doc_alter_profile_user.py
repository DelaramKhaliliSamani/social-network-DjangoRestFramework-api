# Generated by Django 4.2 on 2023-04-30 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='directmessage',
            name='doc',
            field=models.FileField(blank=True, null=True, upload_to='docs/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='puser', to=settings.AUTH_USER_MODEL),
        ),
    ]

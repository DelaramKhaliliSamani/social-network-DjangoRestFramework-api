# Generated by Django 4.2 on 2023-05-06 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanual', '0005_alter_mobilemanual_comment_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webmanual',
            name='register_description',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
    ]
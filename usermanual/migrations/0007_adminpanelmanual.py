# Generated by Django 4.2 on 2023-05-06 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanual', '0006_alter_webmanual_register_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminPanelManual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('login_img', models.ImageField(blank=True, null=True, upload_to='mobile_login_img/%Y/%m/%d')),
                ('profile_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to='mobile_edit_profile_img/%Y/%m/%d')),
                ('message_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('message_img', models.ImageField(blank=True, null=True, upload_to='mobile_edit_img/%Y/%m/%d')),
                ('post_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('post_img', models.ImageField(blank=True, null=True, upload_to='mobile_post_img/%Y/%m/%d')),
                ('comment_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('comment_img', models.ImageField(blank=True, null=True, upload_to='mobile_comment_img/%Y/%m/%d')),
                ('vote_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('vote_img', models.ImageField(blank=True, null=True, upload_to='mobile_vote_img/%Y/%m/%d')),
                ('relation_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('relation_img', models.ImageField(blank=True, null=True, upload_to='web_relation_img/%Y/%m/%d')),
                ('user_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('user_img', models.ImageField(blank=True, null=True, upload_to='web_relation_img/%Y/%m/%d')),
                ('token_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('token_img', models.ImageField(blank=True, null=True, upload_to='web_relation_img/%Y/%m/%d')),
                ('web_manual_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('web_manual_img', models.ImageField(blank=True, null=True, upload_to='web_relation_img/%Y/%m/%d')),
                ('mobile_manual_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('mobile_manual_img', models.ImageField(blank=True, null=True, upload_to='web_relation_img/%Y/%m/%d')),
                ('admin_manual_description', models.TextField(blank=True, max_length=100000, null=True)),
                ('admin_manual_img', models.ImageField(blank=True, null=True, upload_to='web_relation_img/%Y/%m/%d')),
            ],
        ),
    ]
# Generated by Django 4.0.4 on 2022-04-25 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_profile_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_image',
            field=models.ImageField(default='../images/default-user.jpg', upload_to=''),
        ),
    ]

# Generated by Django 4.0.4 on 2022-04-25 01:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_remove_posts_votes_posts_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='likes',
            field=models.ManyToManyField(related_name='comment_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]

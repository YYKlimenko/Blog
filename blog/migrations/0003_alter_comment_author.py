# Generated by Django 4.0.1 on 2022-02-05 10:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_alter_comment_options_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=1, on_delete=models.SET('Неизвестный автор'), to=settings.AUTH_USER_MODEL),
        ),
    ]

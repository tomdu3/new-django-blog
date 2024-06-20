# Generated by Django 5.0.1 on 2024-06-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_comment_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="excerpt",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="post",
            name="updated_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]

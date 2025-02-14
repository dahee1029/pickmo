# Generated by Django 4.2.16 on 2024-11-26 08:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('poster_path', models.URLField(blank=True, null=True)),
                ('genre', models.TextField(blank=True, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('runtime', models.IntegerField(blank=True, null=True)),
                ('budget', models.BigIntegerField(blank=True, null=True)),
                ('revenue', models.BigIntegerField(blank=True, null=True)),
                ('liked_by', models.ManyToManyField(blank=True, related_name='liked_movies_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

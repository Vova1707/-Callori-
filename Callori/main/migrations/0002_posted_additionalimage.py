# Generated by Django 4.2 on 2024-08-17 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='Название поста')),
                ('content', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to=main.utilities.get_timestamp_path, verbose_name='Изображение')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Выводить в списке?')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор объявления')),
            ],
            options={
                'verbose_name': 'Посты',
                'verbose_name_plural': 'Пост',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=main.utilities.get_timestamp_path, verbose_name='Изображение')),
                ('bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.posted', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Дополнительная иллюстрация',
                'verbose_name_plural': 'Дополнительные иллюстрации',
            },
        ),
    ]
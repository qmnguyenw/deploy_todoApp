# Generated by Django 3.0.4 on 2020-03-06 02:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=100)),
                ('task_desc', models.TextField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=False)),
                ('image', models.ImageField(default='images/none/none.jpg', upload_to='images/')),
                ('doc', models.FileField(default='docs/none/none.txt', upload_to='docs/')),
                ('owner', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='task', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
    ]

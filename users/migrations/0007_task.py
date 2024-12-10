# Generated by Django 5.0.6 on 2024-11-26 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('ongoing', 'Ongoing'), ('due', 'Due')], max_length=10)),
                ('due_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]

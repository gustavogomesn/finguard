# Generated by Django 5.1.1 on 2024-10-04 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_fixedexpense_end_month_alter_fixedexpense_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedexpense',
            name='end_month',
            field=models.DateField(),
        ),
    ]

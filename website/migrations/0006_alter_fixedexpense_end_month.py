# Generated by Django 5.1.1 on 2024-10-04 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_alter_fixedexpense_end_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedexpense',
            name='end_month',
            field=models.DateField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.2 on 2025-04-10 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_with_cards_app', '0007_alter_card_definition_alter_card_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='definition',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='cardset',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]

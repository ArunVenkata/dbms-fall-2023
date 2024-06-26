# Generated by Django 4.2.7 on 2023-12-01 07:16

import decimal
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_product_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTransactionDetails',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=decimal.Decimal, max_digits=10)),
                ('category', models.CharField(choices=[('board_game', 'board_game'), ('card_game', 'card_game'), ('video_game', 'video_game'), ('war_games', 'war_games'), ('adventure', 'adventure')], max_length=20)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='usertransaction',
            name='shop_usertransaction_quantity_range',
        ),
        migrations.RemoveField(
            model_name='usertransaction',
            name='category',
        ),
        migrations.RemoveField(
            model_name='usertransaction',
            name='name',
        ),
        migrations.RemoveField(
            model_name='usertransaction',
            name='price',
        ),
        migrations.RemoveField(
            model_name='usertransaction',
            name='product',
        ),
        migrations.RemoveField(
            model_name='usertransaction',
            name='quantity',
        ),
        migrations.AddField(
            model_name='usertransactiondetails',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product'),
        ),
        migrations.AddField(
            model_name='usertransactiondetails',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.usertransaction'),
        ),
        migrations.AddConstraint(
            model_name='usertransactiondetails',
            constraint=models.CheckConstraint(check=models.Q(('quantity__range', (1, 1000))), name='shop_usertransactiondetails_quantity_range'),
        ),
    ]

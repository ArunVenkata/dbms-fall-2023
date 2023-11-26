# Generated by Django 4.2.7 on 2023-11-26 02:32

import decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
        ('shop', '0006_product_original_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertransactiondetails',
            name='id',
        ),
        migrations.RemoveField(
            model_name='usertransactiondetails',
            name='salesperson',
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='category',
            field=models.CharField(choices=[('board_game', 'board_game'), ('card_game', 'card_game'), ('video_game', 'video_game'), ('war_games', 'war_games'), ('adventure', 'adventure')], default='board_game', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='comments',
            field=models.TextField(default=str),
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='price',
            field=models.DecimalField(decimal_places=2, default=decimal.Decimal, max_digits=10),
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product'),
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='quantity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='salesperson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userauth.salesuser'),
        ),
        migrations.AddConstraint(
            model_name='usertransaction',
            constraint=models.CheckConstraint(check=models.Q(('quantity__range', (1, 1000))), name='shop_usertransaction_quantity_range'),
        ),
        migrations.DeleteModel(
            name='UserTransactionDetails',
        ),
    ]

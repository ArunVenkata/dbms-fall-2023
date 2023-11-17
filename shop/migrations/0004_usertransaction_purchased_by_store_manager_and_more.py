# Generated by Django 4.2.7 on 2023-11-17 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0003_region_store_usertransaction_alter_product_price_and_more'),
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertransaction',
            name='purchased_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='store',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='store',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.region'),
        ),
        migrations.AddField(
            model_name='region',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usertransactiondetails',
            name='salesperson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userauth.salesuser'),
        ),
        migrations.AddConstraint(
            model_name='usertransactiondetails',
            constraint=models.CheckConstraint(check=models.Q(('quantity__range', (1, 1000))), name='shop_usertransactiondetails_quantity_range'),
        ),
    ]

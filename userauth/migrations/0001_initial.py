# Generated by Django 4.2.7 on 2023-11-17 21:20

import decimal
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('shop', '0003_region_store_usertransaction_alter_product_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.UUID('c064f828-4bba-49a2-afff-07fcdf2e89ad'), primary_key=True, serialize=False)),
                ('user_type', models.CharField(choices=[('home', 'home'), ('business', 'business'), ('salesperson', 'salesperson')])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('street', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessUser',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('business_category', models.CharField(max_length=100)),
                ('gross_annual_income', models.DecimalField(decimal_places=2, default=decimal.Decimal, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='HomeUser',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('marital_status', models.CharField(choices=[('unmarried', 'unmarried'), ('married', 'married')])),
                ('gender', models.CharField(default=str)),
                ('age', models.IntegerField()),
                ('income', models.DecimalField(decimal_places=2, default=decimal.Decimal, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='SalesUser',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('job_title', models.CharField(max_length=150)),
                ('income', models.DecimalField(decimal_places=2, default=decimal.Decimal, max_digits=20)),
                ('store_assigned', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.store')),
            ],
        ),
        migrations.AddConstraint(
            model_name='homeuser',
            constraint=models.CheckConstraint(check=models.Q(('age__range', (18, 150))), name='userauth_homeuser_age_range'),
        ),
    ]

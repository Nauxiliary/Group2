# Generated by Django 4.0.1 on 2022-02-17 17:32

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
            name='BasePerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone', models.CharField(max_length=15)),
                ('telephone_2', models.CharField(max_length=15)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('printed', models.BooleanField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('breed', models.CharField(max_length=255)),
                ('condition', models.CharField(max_length=255)),
                ('special_instructions', models.CharField(max_length=255)),
                ('last_seen', models.DateTimeField(verbose_name='pet last seen')),
                ('picture', models.BinaryField()),
                ('temperament', models.CharField(max_length=1)),
                ('clip', models.CharField(max_length=255)),
                ('owner', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('local_name', models.CharField(max_length=100)),
                ('date_administered', models.DateField(verbose_name='date pet was administered vaccine')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('baseperson_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='common.baseperson')),
                ('type', models.CharField(max_length=1)),
                ('relationship', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('common.baseperson',),
        ),
        migrations.CreateModel(
            name='PetVaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.pet')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.vaccine')),
            ],
        ),
        migrations.CreateModel(
            name='PetForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.form')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.pet')),
            ],
        ),
        migrations.AddField(
            model_name='pet',
            name='vaccine',
            field=models.ManyToManyField(through='common.PetVaccine', to='common.Vaccine'),
        ),
        migrations.AddField(
            model_name='form',
            name='pet',
            field=models.ManyToManyField(through='common.PetForm', to='common.Pet'),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('request_date', models.DateTimeField(verbose_name='date and time client requested')),
                ('status', models.CharField(max_length=1)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VaccineReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.vaccine')),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.reference')),
            ],
        ),
        migrations.AddField(
            model_name='vaccine',
            name='administered_by',
            field=models.ManyToManyField(through='common.VaccineReference', to='common.Reference'),
        ),
    ]

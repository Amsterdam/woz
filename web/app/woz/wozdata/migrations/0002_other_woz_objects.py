# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 14:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wozdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WOZDeelObject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('volgnummer', models.IntegerField()),
                ('begindatum_deelobject', models.DateField()),
                ('begindatum_voorkomen', models.DateField()),
                ('code', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=3)),
                ('bouwjaar', models.IntegerField(blank=True, null=True)),
                ('bouwlaag', models.IntegerField(blank=True, null=True)),
                ('renovatiejaar', models.IntegerField(blank=True, null=True)),
                ('oppervlakte', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ('woz_object',),
            },
        ),
        migrations.CreateModel(
            name='WOZKadastraalObject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('begindatum_relatie_wozobject', models.DateField()),
                ('begindatum_relatie_voorkomen', models.DateField()),
                ('kadastraal_object_identificatie', models.CharField(max_length=36)),
                ('kadastrale_gemeentecode', models.CharField(max_length=5)),
                ('sectie', models.CharField(max_length=2)),
                ('perceelnummer',models.CharField(max_length=5)),
                ('indexletter', models.CharField(max_length=1)),
                ('indexnummer', models.CharField(max_length=4)),
                ('grootte', models.IntegerField(null=True, blank=True)),
                ('toegekende_oppervlakte', models.IntegerField(null=True, blank=True)),
                ('meegetaxeerde_oppervlakte', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ('woz_object',),
            },
        ),
        migrations.CreateModel(
            name='WOZWaardeBeschikking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('begindatum_waarde_object', models.DateField()),
                ('einddatum_waarde_object', models.DateField(null=True, blank=True)),
                ('begindatum_waarde_voorkomen', models.DateField()),
                ('vastgestelde_waarde', models.IntegerField()),
                ('waardepeildatum', models.DateField()),
                ('begindatum_waarde', models.DateField()),
                ('begindatum_beschikking_object', models.DateField()),
                ('einddatum_beschikking_object', models.DateField(null=True, blank=True)),
                ('begindatum_beschikking_voorkomen', models.DateField()),
                ('documentnummer_beschikking', models.CharField(max_length=16)),
                ('status_beschikking', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ('woz_object',),
            },
        ),
        migrations.AddField(
            model_name='wozdeelobject',
            name='woz_object',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='wozdata.WOZObject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wozkadastraalobject',
            name='woz_object',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='wozdata.WOZObject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wozwaardebeschikking',
            name='woz_object',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='wozdata.WOZObject'),
            preserve_default=False,
        ),
    ]


# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WOZObject',
            fields=[
                ('woz_objectnummer', models.CharField(db_index=True, max_length=12, unique=True, primary_key=True)),
                ('volgnummer', models.IntegerField()),
                ('begindatum_wozobject', models.DateField()),
                ('begindatum_voorkomen', models.DateField()),
                ('status', models.CharField(max_length=32)),
                ('gebruikscode', models.CharField(max_length=50)),
                ('soort_objectcode', models.CharField(max_length=100)),
                ('code_gebouwd_ongebouwd', models.CharField(max_length=1)),
                ('monumentaanduiding', models.IntegerField()),
                ('kadastraal_subject_identificatie', models.CharField(max_length=12)),
                ('subjecttype', models.CharField(max_length=32)),
                ('subjectnaam', models.CharField(max_length=255)),
                ('aard_zakelijk_recht', models.CharField(max_length=64)),
                ('openbare_ruimte_identificatie', models.CharField(max_length=50)),
                ('naam_openbare_ruimte', models.CharField(max_length=255)),
                ('huisnummer', models.CharField(max_length=8)),
                ('huisletter', models.CharField(max_length=8)),
                ('huisnummer_toevoeging', models.CharField(max_length=32)),
                ('nummeraanduidingidentificatie', models.CharField(max_length=50)),
                ('locatieomschrijving', models.CharField(max_length=100)),
                ('verantwoordelijke_gemeente', models.CharField(max_length=4)),
                ('betrokken_waterschap', models.CharField(max_length=14)),
                ('buurtidentificatie', models.CharField(max_length=14)),
                ('volledige_code', models.CharField(max_length=4)),
            ],
        ),
        migrations.AlterModelOptions(
            name='wozobject',
            options={'ordering': ('woz_objectnummer',)},
        ),
    ]


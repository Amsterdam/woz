from django.db import models


class WOZObject(models.Model):
    woz_objectnummer = models.CharField(max_length=12, unique=True, db_index=True, primary_key=True)
    volgnummer = models.IntegerField()
    begindatum_wozobject = models.DateField()
    begindatum_voorkomen = models.DateField()
    status = models.CharField(max_length=32)
    gebruikscode = models.CharField(max_length=50)
    soort_objectcode = models.CharField(max_length=100)
    code_gebouwd_ongebouwd = models.CharField(max_length=1)
    monumentaanduiding = models.IntegerField()
    kadastraal_subject_identificatie = models.CharField(max_length=12)
    subjecttype = models.CharField(max_length=32)
    subjectnaam = models.CharField(max_length=255)
    aard_zakelijk_recht = models.CharField(max_length=64)
    openbare_ruimte_identificatie = models.CharField(max_length=50)
    naam_openbare_ruimte = models.CharField(max_length=255)
    huisnummer = models.CharField(max_length=8)
    huisletter = models.CharField(max_length=8)
    huisnummer_toevoeging = models.CharField(max_length=32)
    nummeraanduidingidentificatie = models.CharField(max_length=50)
    locatieomschrijving = models.CharField(max_length=100)
    verantwoordelijke_gemeente = models.CharField(max_length=4)
    betrokken_waterschap = models.CharField(max_length=14)
    buurtidentificatie = models.CharField(max_length=14)
    volledige_code = models.CharField(max_length=4)

    class Meta:
        ordering = ('woz_objectnummer',)

    def __str__(self):
        return f"<WOZObject {self.woz_objectnummer}>"


class WOZDeelObject(models.Model):
    id = models.AutoField(primary_key=True)
    woz_object = models.ForeignKey(WOZObject)
    volgnummer = models.IntegerField()
    begindatum_deelobject = models.DateField()
    begindatum_voorkomen = models.DateField()
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=3)
    bouwjaar = models.IntegerField(null=True, blank=True)
    bouwlaag = models.IntegerField(null=True, blank=True)
    renovatiejaar = models.IntegerField(null=True, blank=True)
    oppervlakte = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('woz_object',)

    def __str__(self):
        return f"<WOZDeelObject nr. {self.volgnummer} bij {self.woz_object}>"


class WOZKadastraalObject(models.Model):
    id = models.AutoField(primary_key=True)
    woz_object = models.ForeignKey(WOZObject)
    begindatum_relatie_wozobject = models.DateField()
    begindatum_relatie_voorkomen = models.DateField()
    kadastraal_object_identificatie = models.CharField(max_length=36)
    kadastrale_gemeentecode = models.CharField(max_length=5)
    sectie = models.CharField(max_length=2)
    perceelnummer = models.CharField(max_length=5)
    indexletter = models.CharField(max_length=1)
    indexnummer = models.CharField(max_length=4)
    grootte = models.IntegerField(null=True, blank=True)
    toegekende_oppervlakte = models.IntegerField(null=True, blank=True)
    meegetaxeerde_oppervlakte = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('woz_object',)

    def __str__(self):
        return f"<WOZKadastraalObject {self.kadastraal_object_identificatie} - bij WOZ: {self.woz_object}>"


class WOZWaardeBeschikking(models.Model):
    id = models.AutoField(primary_key=True)
    woz_object = models.ForeignKey(WOZObject)
    begindatum_waarde_object = models.DateField()
    einddatum_waarde_object = models.DateField(null=True, blank=True)
    begindatum_waarde_voorkomen = models.DateField()
    vastgestelde_waarde = models.IntegerField()
    waardepeildatum = models.DateField()
    begindatum_waarde = models.DateField()
    begindatum_beschikking_object = models.DateField()
    einddatum_beschikking_object = models.DateField(null=True, blank=True)
    begindatum_beschikking_voorkomen = models.DateField()
    documentnummer_beschikking = models.CharField(max_length=16)
    status_beschikking = models.CharField(max_length=64)

    class Meta:
        ordering = ('woz_object',)

    def __str__(self):
        return f"<WOZWaardeBeschikking {self.documentnummer_beschikking} - bij {self.woz_object}>"

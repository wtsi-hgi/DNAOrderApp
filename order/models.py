from django.db import models


""" ACTUAL DNA ORDER APP """

class PlatformType(models.Model):
    platform_type = models.CharField(max_length=100, unique=True)
    
    def __unicode__(self):
        return self.platform_type
    
class Platform(models.Model):
    platform_name = models.CharField(max_length=100, unique=True)
    platform_type = models.ForeignKey(PlatformType)
    platform_description = models.TextField()
    
    def __unicode__(self):
        return self.platform_name

class PhenotypeType(models.Model):
    phenotype_type = models.CharField(max_length=100, unique=True)
    
    def __unicode__(self):
        return self.phenotype_type

class Phenotype(models.Model):
    phenotype_name = models.CharField(max_length=100, unique=True)
    phenotype_type = models.ForeignKey(PhenotypeType)
    phenotype_description = models.TextField()

    def __unicode__(self):
        return self.phenotype_name
    
class Individual(models.Model):
    active = models.ForeignKey('self', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
class PhenodbIdentifier(models.Model):
    phenodb_id = models.CharField(max_length=100, unique=True)
    individual = models.OneToOneField(Individual, primary_key=True)    
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return self.individual_string

class Collection(models.Model):
    collection_name = models.CharField(max_length=100, unique=True)
    collection_description = models.TextField()
    
    def __unicode__(self):
        return self.source_name

class IndividualCollection(models.Model):
    individual = models.ForeignKey(Individual)
    collection = models.ForeignKey(Collection)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return self.individual_string

class AffectionStatusPhenotypeValue(models.Model):
    phenotype = models.ForeignKey(Phenotype)
    individual = models.ForeignKey(Individual)
    phenotype_value = models.SmallIntegerField()
    flagged = models.BooleanField() 
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    # # phenotype.db_index = True
    
    def __unicode__(self):
        return u'%i' % self.phenotype_value
    
class QualitativePhenotypeValue(models.Model):
    phenotype = models.ForeignKey(Phenotype)
    individual = models.ForeignKey(Individual)
    phenotype_value = models.CharField(max_length=200)
    flagged = models.BooleanField() 
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return self.phenotype_value

class QuantitativePhenotypeValue(models.Model):
    phenotype = models.ForeignKey(Phenotype)
    individual = models.ForeignKey(Individual)
    phenotype_value = models.DecimalField(max_digits=10, decimal_places=2)
    flagged = models.BooleanField() 
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return u'%f' % self.phenotype_value

"""ADDED AFTER THE MANIFEST WAS SHOWN TO JAMES"""


class Study(models.Model):
    study_name = models.CharField(max_length=100, unique=True)
    platform = models.ForeignKey(Platform)
    data_location = models.CharField(max_length=200)
    study_description = models.TextField()
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return self.study_name

class Sample(models.Model):
    individual = models.ForeignKey(Individual)
    sample_id = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
class StudySample(models.Model):
    study = models.ForeignKey(Study)
    sample = models.ForeignKey(Sample)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    
class SampleFeatureType(models.Model):
    sample_feature_type = models.CharField(max_length=100, unique=True)
    
    def __unicode__(self):
        return self.phenotype_type

class SampleFeature(models.Model):
    sample_feature_name = models.CharField(max_length=100, unique=True)
    sample_feature_type = models.ForeignKey(SampleFeatureType)
    sample_feature_description = models.TextField()

    def __unicode__(self):
        return self.phenotype_name    
    

""" DATA TYPE """
class AffectionStatusSampleFeatureValue(models.Model):
    sample_feature = models.ForeignKey(SampleFeature)
    sample = models.ForeignKey(Sample)
    sample_feature_value = models.SmallIntegerField()
    flagged = models.BooleanField() 
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    # # phenotype.db_index = True
    
    def __unicode__(self):
        return u'%i' % self.sample_feature_value
    
class QualitativeSampleFeatureValue(models.Model):
    sample_feature = models.ForeignKey(SampleFeature)
    sample = models.ForeignKey(Sample)
    sample_feature_value = models.CharField(max_length=200)
    flagged = models.BooleanField() 
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return self.sample_feature_value

class QuantitativeSampleFeatureValue(models.Model):
    sample_feature = models.ForeignKey(SampleFeature)
    sample = models.ForeignKey(Sample)
    sample_feature_value = models.DecimalField(max_digits=10, decimal_places=2)
    flagged = models.BooleanField() 
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return u'%f' % self.sample_feature_value    

'''ADDED DATETIME DATATYPE'''
class DateTimeSampleFeatureValue(models.Model):
    sample_feature = models.ForeignKey(SampleFeature)
    sample = models.ForeignKey(Sample)
    sample_feature_value = models.DateField()
    flagged = models.BooleanField()
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return self.sample_feature_value
    
class Source(models.Model):
    source_name = models.CharField(max_length=100, unique=True)
    contact_name = models.CharField(max_length=100)
    source_description = models.TextField()
    
    def __unicode__(self):
        return self.source_name

class IndividualIdentifier(models.Model):
    individual = models.ForeignKey(Individual)
    individual_string = models.CharField(max_length=100)
    source = models.ForeignKey(Source)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return self.individual_string

class QC(models.Model):
    qc_name = models.CharField(max_length=100, unique=True)
    qc_description = models.TextField()
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return self.qc_name
    
class SampleQC(models.Model):
    study_sample = models.ForeignKey(StudySample)
    qc = models.ForeignKey(QC)
    qc_pass = models.BooleanField()
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    
class BulkUpload(models.Model):
    pass    
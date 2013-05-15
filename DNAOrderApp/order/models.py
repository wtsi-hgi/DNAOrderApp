from django.db import models

"""
MODELS.PY

CREATED BY James Morris

Modified by Albertina Wong, March 22, 2013 to address the following issues:
    - Adding longitudinal studies
    - Datetime datatype for phenotypic data and sample data
    - methodology field in Study
    - changing study_desc to comments in Study
    - adding definition field to Phenotype
    - adding id, units to the phenotypical values
    - adding units to sample values
    - adding sanger_plate_id, sanger_sample_id, supplier_sample_name, supplier to Sample Table
    - changing the FK specified between Study and Sample as a ManyToMany Relationship...unless each sample MUST BE 
        LINK WITH A STUDY, in which case, then the FK is necessary...but couldn't we do something about that in a M2M 
        relationship?
    - removed flagged field from all the DataType Models
"""

""" ACTUAL DNA ORDER APP """

class Individual(models.Model):
    active = models.ForeignKey('self', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

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
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
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
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.individual_string

class PhenodbIdentifier(models.Model):
    phenodb_id = models.CharField(max_length=100, unique=True)
    individual = models.OneToOneField(Individual, primary_key=True)    
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.individual_string
    
class PhenotypeType(models.Model):
    phenotype_type = models.CharField(max_length=100, unique=True)
    
    def __unicode__(self):
        return self.phenotype_type

class Phenotype(models.Model):
    phenotype_name = models.CharField(max_length=100, unique=True)
    phenotype_type = models.ForeignKey(PhenotypeType)
    phenotype_description = models.TextField()
    phenotype_definition = models.TextField()  # Not too sure if should be CharField or TextField...should be unique

    def __unicode__(self):
        return self.phenotype_name

class AffectionStatusPhenotypeValue(models.Model):
    phenotype = models.ForeignKey(Phenotype)
    individual = models.ForeignKey(Individual)
    phenotype_value = models.SmallIntegerField()
    phenotype_unit = models.CharField(max_length=100)
    phenotype_set_id = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # # phenotype.db_index = True
    
    def __unicode__(self):
        return u'%i' % self.phenotype_value
    
class QualitativePhenotypeValue(models.Model):
    phenotype = models.ForeignKey(Phenotype)
    individual = models.ForeignKey(Individual)
    phenotype_value = models.CharField(max_length=200)
    phenotype_unit = models.CharField(max_length=100)
    phenotype_set_id = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.phenotype_value

class QuantitativePhenotypeValue(models.Model):
    phenotype = models.ForeignKey(Phenotype)
    individual = models.ForeignKey(Individual)
    phenotype_value = models.DecimalField(max_digits=10, decimal_places=2)
    phenotype_unit = models.CharField(max_length=100)
    phenotype_set_id = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%f' % self.phenotype_value
 
class DatePhenotypeValue(models.Model):
    phenotype = models.ForeignKey(Phenotype)
    individual = models.ForeignKey(Individual)
    phenotype_value = models.DateField()
    phenotype_set_id = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.phenotype_value

"""ADDED AFTER THE MANIFEST WAS SHOWN TO JAMES"""

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

class Study(models.Model):
    study_name = models.CharField(max_length=100, unique=True)
    platform = models.ForeignKey(Platform, null=True, blank=True)
    data_location = models.CharField(max_length=200)
    methodology_desc = models.TextField()
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.study_name

class Sample(models.Model):
    individual = models.ForeignKey(Individual, null=True, blank=True)
    supplier_name = models.CharField(max_length=100)
    #sample_id = models.CharField(max_length=100)
    sanger_plate_id = models.CharField(max_length=100)
    sanger_sample_id = models.CharField(max_length=100)
    supplier_sample_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.individual
    
class StudySample(models.Model):
    study = models.ForeignKey(Study)
    sample = models.ForeignKey(Sample)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.study
    
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
    
class AffectionStatusSampleFeatureValue(models.Model):
    sample_feature = models.ForeignKey(SampleFeature)
    sample = models.ForeignKey(Sample)
    sample_feature_value = models.SmallIntegerField()
    sample_unit = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # # phenotype.db_index = True
    
    def __unicode__(self):
        return u'%i' % self.sample_feature_value
    
class QualitativeSampleFeatureValue(models.Model):
    sample_feature = models.ForeignKey(SampleFeature)
    sample = models.ForeignKey(Sample)
    sample_feature_value = models.CharField(max_length=200)
    sample_unit = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.sample_feature_value

class QuantitativeSampleFeatureValue(models.Model):
    sample_feature = models.ForeignKey(SampleFeature)
    sample = models.ForeignKey(Sample)
    sample_feature_value = models.DecimalField(max_digits=10, decimal_places=2)
    sample_unit = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%f' % self.sample_feature_value    

class DateSampleFeatureValue(models.Model):
    sample_feature = models.ForeignKey(SampleFeature)
    sample = models.ForeignKey(Sample)
    sample_feature_value = models.DateField()
    sample_unit = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u'%s' % self.sample_feature_value

class QC(models.Model):
    qc_name = models.CharField(max_length=100, unique=True)
    qc_description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.qc_name
    
class SampleQC(models.Model):
    study_sample = models.ForeignKey(StudySample)
    qc = models.ForeignKey(QC)
    qc_pass = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
class BulkUpload(models.Model):
    pass   

""" MANIFEST UPLOAD """

# Stores the user uploaded files
class Document(models.Model):
    docfile = models.FileField(upload_to='manifests/%Y-%m-%d')

class Display(models.Model):
    study_name = models.CharField(max_length=100, unique=True)
    supplier_name = models.CharField(max_length=100)
    sanger_plate_id = models.CharField(max_length=100)
    sanger_sample_id = models.CharField(max_length=100)

'''
""" MODELFORMS """
from django.forms import ModelForm 

class StudyForm(ModelForm):
    class Meta:
        model = Study
        exclude = ('platform', 'data_location', 'methodology_desc', 'comment')

class SampleForm(ModelForm):
    class Meta:
        model = Sample
        exclude = ('individual', 'sample_id', 'sanger_plate_id', 'sanger_sample_id',
            'supplier_sample_name')
'''



        








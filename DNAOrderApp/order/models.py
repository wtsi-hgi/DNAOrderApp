from django.db import models
from django.contrib.auth.models import User

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

""" TEMPORARY MODELS TO SIMULATE DIFFERENT ROLES FOR DIFFERENT VIEWS """
'''
There is user authentication in Django: https://docs.djangoproject.com/en/dev/topics/auth/
At the moment that is not the main focus. This is already being done by another project.
'''

# class UserRole(models.Model):
#     user_role = models.CharField(max_length=100, unique=True)
    
#     def __unicode__(self):
#         return self.user_role

# TITLE_CHOICES = (
#     ('MR', 'Mr.'),
#     ('MRS', 'Mrs.'),
#     ('MS', 'Ms.'),
# )

# # DUMMY USER
# class User(models.Model):
#     email = models.EmailField(max_length=254, unique=True)
#     role = models.ForeignKey(UserRole)
#     password = models.CharField(max_length=100)
#     address = models.TextField()
#     fax_num = models.CharField(max_length=100) #To store the number as entered by the user, because different phone formats exists across the globe
#     phone_num = models.CharField(max_length=100)
#     affiliation = models.CharField(max_length=100)
#     date_created = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now=True)
#     title = models.CharField(max_length=3, choices=TITLE_CHOICES)


""" ACTUAL DNA ORDER APP """

class Individual(models.Model):
    active = models.ForeignKey('self', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

# EXTERNAL COLLABORATORS
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


# THIS PARTICULAR DESIGN WOULD ALLOW USER TO ADD ADDITIONAL PHENOTYPETYPES IF ANYMORE APPEARS   
class PhenotypeType(models.Model):
    phenotype_type = models.CharField(max_length=100, unique=True)
    
    def __unicode__(self):
        return self.phenotype_type

class UserProject(models.Model):

    # STATUS = (
    #     ('In Progress', 'In Progress'),
    #     ('Complete', 'Complete'),
    # )

    username = models.ForeignKey(User)
    project_name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # project_status = models.CharField(max_length=100, choices=STATUS, default='In Progress')

    def __unicode__(self):
        return self.project_name

class Phenotype(models.Model):
    phenotype_name = models.CharField(max_length=100, unique=True)
    phenotype_type = models.ForeignKey(PhenotypeType)
    phenotype_description = models.TextField()
    phenotype_definition = models.TextField()  # Not too sure if should be CharField or TextField...should be unique

    def __unicode__(self):
        return self.phenotype_name

class SampleSubmission(models.Model):

    STATUS = (
        ('Incomplete Phenotype List', 'Incomplete Phenotype List'),
        ('Start Well-filling', 'Start Well-filling'),
        ('Sample Submission Complete', 'Sample Submission Complete')
    )

    sample_submission_name = models.CharField(max_length=100, unique=True)
    project_name = models.ForeignKey(UserProject)
    source = models.ForeignKey(Source)
    sample_num = models.IntegerField() #two end users don't need to worry about manifest, we can generate the sample id 
    phenotype_list = models.ManyToManyField(Phenotype) #Associated phenotype list, will generate m2m table
    order_status = models.CharField(max_length=100, choices=STATUS, default='Incomplete Phenotype List')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.sample_submission_name

# THE UNITS MIGHT BE BEST IF PROVIDED BY THE COLLABORATORS INSTEAD OF FACULTY MEMBER
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


# This study model will be modified, since studies are known already, 
# and are associated with the individuals
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
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class Unit(models.Model):
    unit_name = models.CharField(max_length=100, unique=True)

from django.forms import ModelForm
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = User

class PhenotypeForm(ModelForm):
    class Meta:
        model = Phenotype
        widgets = {
            'phenotype_description': forms.Textarea(attrs={'rows':2, 'cols':15}),
            'phenotype_definition' : forms.Textarea(attrs={'rows':2, 'cols':15})
        }

class SampleSubmissionForm(ModelForm):
    class Meta:
        model = SampleSubmission
        # exclude = ['phenotype_list']

class UserProjectForm(ModelForm):
    class Meta:
        model = UserProject


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

'''
# NOTE: I'M TRYING OUT THE DEFAULT M2M RELATIONSHIPS IN DJANGO
# class SampleSubmissionPhenotype(models.Model):
#     phenotype = models.ForeignKey(Phenotype)
#     sample_submission = models.ForeignKey(SampleSubmission)

#     def __unicode__(self):
#         return self.sample_submission_phenotype_name

        
# class OrderStatus(models.Model):
#     # NOTE: these aren't actually choices...but these are the statuses
#     STATUS = (
#         ('A', 'Incomplete Phenotype List'),
#         ('b', 'Start Well-filling'),
#         ('c', 'Sample Submission Complete')
#     )

#     order_status = models.CharField(max_length=100, choices=STATUS, default='A')

#     def __unicode__(self):
#         return self.order_status


#DUMMY PROJECT LIST
# class ProjectStatus(models.Model):
#     # NOTE: these aren't actually choices...but these are the statuses
#     STATUS = (
#         ('in_progress', 'In Progress'),
#         ('complete', 'Complete'),
#     )

#     project_status = models.CharField(max_length=100, default='in_progress')

#     def __unicode__(self):
#         return self.project_status

'''




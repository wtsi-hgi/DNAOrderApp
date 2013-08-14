from django import template
from DNAOrderApp.order.models import Phenotype, PhenotypeType

register = template.Library()

def get_phenotype_type_by_phenotype_name(phenotype_name):
	"""Returns the phenotype type given the associated phenotype name"""
	return PhenotypeType.objects.filter(phenotype__phenotype_name__exact=phenotype_name)


def get_phenotype_type_by_id(phenotype_type_id):
	"""Returns the corresponding phenotype type given its id"""
	return PhenotypeType.objects.get(pk=phenotype_type_id)

def get_all_phenotypes(Queryset_Phenotype):
	"""Returns all phenotypes for typeahead function in fmprojectlist"""
	pheno_list = []
	for c in Queryset_Phenotype:
		print str(c.phenotype_name)
		# print str(c.phenotype_type)  Even though uniqueness of phenotype is defined 
		# by phenotype name and phenotype type, autosuggest is best only for the phenotype
		# name atm.
		pheno_list.append(str(c.phenotype_name))

	print 'this is a list', pheno_list
	return "[\"" + "\",\"".join(pheno_list) + "\"]"


register.filter('get_phenotype_type_by_phenotype_name', get_phenotype_type_by_phenotype_name)
register.filter('get_phenotype_type_by_id', get_phenotype_type_by_id)
register.filter('get_all_phenotypes', get_all_phenotypes)
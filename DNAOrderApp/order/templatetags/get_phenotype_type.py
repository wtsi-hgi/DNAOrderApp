from django import template
from DNAOrderApp.order.models import Phenotype, PhenotypeType

register = template.Library()

def get_phenotype_type_by_phenotype_name(phenotype_name):
	"""Returns the phenotype type given the associated phenotype name"""
	return PhenotypeType.objects.filter(phenotype__phenotype_name__exact=phenotype_name)


def get_phenotype_type_by_id(phenotype_type_id):
	"""Returns the corresponding phenotype type given its id"""
	return PhenotypeType.objects.get(pk=phenotype_type_id)


register.filter('get_phenotype_type_by_phenotype_name', get_phenotype_type_by_phenotype_name)
register.filter('get_phenotype_type_by_id', get_phenotype_type_by_id)
from django import template

register = template.Library()

@register.filter(name='splitYear')
def splitYear(year):
	return str(year)[2:]
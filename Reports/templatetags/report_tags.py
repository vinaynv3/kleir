from django import template

register = template.Library()

@register.filter
def formatSlug(slug,key):
    slug = slug.split('_')
    return slug[key].capitalize()

@register.filter
def getId(ids,key):
    return ids[key]

@register.filter
def pageNo(*args,**kwargs):
    pass

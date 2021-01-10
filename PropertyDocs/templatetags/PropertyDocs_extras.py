from django import template

register = template.Library()

@register.filter
def dict_lookup(dict,key):
    return dict[key]

@register.filter
def list_lookup(customer_list,index_pos):
    return customer_list[index_pos]

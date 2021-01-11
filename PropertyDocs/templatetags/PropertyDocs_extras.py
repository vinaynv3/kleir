from django import template

register = template.Library()

@register.filter
def dict_lookup(dict,key):
    return dict[key]

@register.filter
def list_lookup(customer_list,index_pos):
    return customer_list[index_pos]

@register.filter
def get_firstname(customer_list,index_pos):
    try:
        customer_dict = customer_list[index_pos]
        customer = list(customer_dict.keys())[0]
        return customer.Firstname
    except IndexError:
        return False

@register.filter
def get_lastname(customer_list,index_pos):
    try:
        customer_dict = customer_list[index_pos]
        customer = list(customer_dict.keys())[0]
        return customer.Lastname
    except IndexError:
        return False

@register.filter
def get_slug(customer_list,index_pos):
    try:
        customer_dict = customer_list[index_pos]
        customer = list(customer_dict.keys())[0]
        return customer.Slug
    except IndexError:
        return False

@register.filter
def get_id(customer_list,index_pos):
    try:
        customer_dict = customer_list[index_pos]
        customer = list(customer_dict.keys())[0]
        return customer.Client_ID
    except IndexError:
        return False


@register.filter
def get_val(customer_list,index_pos):
    customer_dict = customer_list[index_pos]
    return list(customer_dict.values())[0]

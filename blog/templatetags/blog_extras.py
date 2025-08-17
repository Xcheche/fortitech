# blog/templatetags/blog_extras.py
from django import template

register = template.Library()


@register.filter
def nice_name(email):
    """
    Converts 'john.doe@example.com' → 'John Doe'
    
    """
    return email.split("@")[0].replace(".", " ").replace("_", " ").title()

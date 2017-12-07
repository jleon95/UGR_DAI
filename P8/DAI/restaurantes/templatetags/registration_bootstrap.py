# coding=utf-8
from django import template
register = template.Library()

@register.filter()
def add_class(field,myclass):
    return field.as_widget(attrs={"class":myclass})

# -*- coding:utf-8 -*-

from django import template
from posts.models import Category, Type

register = template.Library()


@register.filter(name='cat_desc')
def cat_desc(cat_code):
    desc = Category.objects.get(code=cat_code).description
    return desc


@register.filter(name='type_desc')
def type_desc(type_code):
    desc = Type.objects.get(code=type_code).description
    return desc

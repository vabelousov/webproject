from django import template
from posts.models import MyMenu


register = template.Library()


@register.inclusion_tag('menu.html')
def show_menu(menu):
    try:
        menu = MyMenu.objects.all()
    except:
        menu = None
    return {'menu': menu}


@register.inclusion_tag('footer_menu.html')
def show_footer_menu(menu):
    try:
        menu = MyMenu.objects.all()
    except:
        menu = None
    return {'menu': menu}

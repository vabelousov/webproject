# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from .models import MyMenu, Category, Type, Carousel


class MyMenuTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели MyMenu.
    """

    fields = ('name',)


class CategoryTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Category.
    """

    fields = ('description',)


class TypeTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Type.
    """

    fields = ('description',)


class CarouselTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Carousel.
    """

    fields = ('alt_text', 'title', 'text',)


translator.register(MyMenu, MyMenuTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Type, TypeTranslationOptions)
translator.register(Carousel, CarouselTranslationOptions)

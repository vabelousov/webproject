from django.template.defaultfilters import slugify
from taggit.models import Tag, TaggedItem
from unidecode import unidecode


class UnicodeTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        return slugify(unidecode(self.name))[:128]


class UnicodeTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return UnicodeTag

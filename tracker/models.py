from django.db import models


class Thing(models.Model):
    name = models.CharField(max_length=255)
    pigeonhole = models.ForeignKey('tracker.PigeonHole')

    def str_all_attributes(self):
        string = ""
        for attr in self.attributes.all():
            string += "%s: %s\n" % (attr.name, attr.subobject.value)
        return string

class PigeonHole(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Attribute(models.Model):
    name = models.CharField(max_length=255)
    things = models.ManyToManyField('tracker.Thing', related_name='attributes')

    @property
    def subobject(self):
        if self.is_int:
            return self.intattribute
        elif self.is_text:
            return self.textattribute

    @property
    def is_int(self):
        return IntAttribute.objects.filter(attribute_ptr=self).count() > 0

    @property
    def is_text(self):
        return TextAttribute.objects.filter(attribute_ptr=self).count() > 0

class IntAttribute(Attribute):
    value = models.IntegerField()

class TextAttribute(Attribute):
    value = models.TextField()

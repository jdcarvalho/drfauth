from django.db import models


class Country(models.Model):

    acronym = models.CharField(
        max_length=2
    )

    name = models.CharField(
        max_length=200,
    )

    def __str__(self):
        return '{0}-{1}'.format(self.acronym, self.name)

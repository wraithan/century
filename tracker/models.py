from decimal import Decimal
from django.db import models
from lib.century.models import TimedeltaField

class Route(models.Model):
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    distance = models.DecimalField(max_digits=4, decimal_places=2)
    time = TimedeltaField()

    @property
    def miles_per_hour(self):
        return Decimal(self.distance) / Decimal(str(self.time.total_seconds() / 60 / 60))

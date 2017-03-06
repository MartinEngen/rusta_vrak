from __future__ import unicode_literals
from django.conf import settings
from django.db import models

# Create your models here.


# Field to ble able to add a period where there is no business.
# I.e vacation, no time available etc. etc.
class lock_reservation_period(models.Model):
    from_date = models.DateField('Startdato for stopp av bestilling')
    to_date = models.DateField('Sluttdato for stopp av bestilling (T.o.m denne dato)')

    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)



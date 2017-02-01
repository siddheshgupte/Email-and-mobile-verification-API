from __future__ import unicode_literals

from django.utils import timezone

from django.db import models

# Create table
# blank=True for verification_code and updated_at
# Created initialised during creation
class Mobile(models.Model):
    mobile_no = models.CharField(max_length=10, primary_key=True)
    OTP = models.CharField(max_length=6, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.mobile_no

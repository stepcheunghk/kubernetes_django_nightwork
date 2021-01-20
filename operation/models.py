from django.db import models
import datetime

# Create your models here.

def filename(instance, filename):
    filebase, extension = filename.split(".")
    return "%s-%s.%s" %(instance.startdate, instance.subject, extension)

class SpecialDate(models.Model):
    name            = models.CharField(max_length=255)
    startdate       = models.DateField()
    enddate         = models.DateField()

class Operation(models.Model):
    name            = models.CharField(max_length=255)
    phone           = models.CharField(max_length=255)
    domain          = models.CharField(max_length=255)
    category        = models.CharField(max_length=255)
    startdate       = models.DateField()
    starttime       = models.TimeField(default=datetime.time(00,00))
    enddate         = models.DateField()
    endtime         = models.TimeField(default=datetime.time(5,00))
    duration        = models.TextField()
    location        = models.CharField(max_length=255)
    subject         = models.TextField()
    reason_type     = models.CharField(max_length=255)
    reason          = models.TextField()
    impact          = models.TextField(default='No Service Impact')
    remarks         = models.CharField(max_length=255, default='N/A')
    vendor          = models.CharField(blank=True, max_length=255)
    vendor_phone    = models.CharField(blank=True, max_length=255)
    mop             = models.FileField(null=True, blank=True, upload_to=filename)

    @property
    def get_duration(self):
        end_minutes = self.endtime.hour*60 + self.endtime.minute
        start_minutes = self.starttime.hour*60 + self.starttime.minute
        duration_min = end_minutes - start_minutes
        if (duration_min < 0):
            duration_min = 1440 + duration_min
        return duration_min

    def save(self, *arg, **kwargs):
        self.duration = self.get_duration
        super(Operation, self).save(*arg, **kwargs)
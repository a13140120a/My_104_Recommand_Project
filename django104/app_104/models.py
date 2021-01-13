from django.db import models

# Create your models here.

class Job(models.Model):
    url = models.CharField(primary_key=True,max_length=10)
    jobName = models.CharField(max_length=30)
    addressRegion = models.CharField(max_length=3)
    custName = models.CharField(max_length=30)
    jobCat_main = models.CharField(max_length=20)
    workExp = models.SmallIntegerField()
    jiebaCutList_join = models.CharField(max_length=500)
    edu = models.CharField(max_length=40)
    # data = models.JSONField(null=True)

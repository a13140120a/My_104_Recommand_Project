from django.db import models
import json
# Create your models here.

#地區取前三個字就好
with open("./app_104/area.json","r",encoding="utf-8") as f:
    area = json.loads(f.read())
    area = [*map(lambda x: (x,x),area)]

class Job(models.Model):
    data = models.JSONField(null=True)

from django.db import models


class Processo(models.Model):
    numero_processo = models.CharField(max_length=50)
    data = models.JSONField(default={})

from django.db import models


class DefaultModel(models.Model):
    code = models.CharField('код мобильного оператора', max_length=3)
    tag = models.CharField('тег', max_length=200)

    class Meta:
        abstract = True

from django.db import models

class Stratum0(models.Model):
    fqrn = models.CharField('fully qualified repository name', max_length=100)
    url  = models.CharField('stratum 0 URL',                   max_length=255)
    name = models.CharField('name of the repository',          max_length=100)

    def __unicode__(self):
        return self.name + " (" + self.fqrn + ")"


class Stratum1(models.Model):
    stratum0      = models.ForeignKey(Stratum0)
    url           = models.CharField('stratum 1 URL',           max_length=255)
    name          = models.CharField('name of the replica',     max_length=100)

    def __unicode__(self):
        return self.name + " -> " + stratum0.name

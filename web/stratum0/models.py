from django.db import models

class Stratum1(models.Model):
	stratum0_fqrn = models.CharField('mirrored stratum 0 repo', max_length=100)
	url           = models.CharField('stratum 1 URL',           max_length=255)

	def __unicode__(self):
		return self.url

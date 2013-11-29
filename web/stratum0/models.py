from django.db import models
import cvmfs.repository



class ReplicationSite(models.Model):
    name = models.CharField('name of the replication site', max_length=100);

    def __unicode__(self):
        return self.name



class Stratum:
    _repo = None

    def _load_repository_info(self):
        repo = None
        try:
            repo = cvmfs.repository.RemoteRepository(self.url)
        except cvmfs.repository.RepositoryNotFound, e:
            repo = None
        return repo

    def repository(self):
        if not self._repo:
            self._repo = self._load_repository_info()
        return self._repo


class Stratum0(models.Model, Stratum):
    fqrn = models.CharField('fully qualified repository name', max_length=100)
    url  = models.CharField('stratum 0 URL',                   max_length=255)
    name = models.CharField('name of the repository',          max_length=100)

    def __unicode__(self):
        return self.name + " (" + self.fqrn + ")"


class Stratum1(models.Model, Stratum):
    stratum0         = models.ForeignKey(Stratum0)
    replication_site = models.ForeignKey(ReplicationSite)
    url              = models.CharField('stratum 1 URL', max_length=255)

    def __unicode__(self):
        return self.replication_site.name + " -> " + self.stratum0.name

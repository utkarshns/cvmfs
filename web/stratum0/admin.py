from django import forms
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from stratum0.models import Stratum0, Stratum1, ReplicationSite
import cvmfs.repository


class Stratum0AdminForm(forms.ModelForm):
    class Meta:
        model = Stratum0

    def clean(self):
        """
        checks if the provided repository is available
        """
        url  = self.cleaned_data['url']
        fqrn = ""

        try:
            repo = cvmfs.repository.RemoteRepository(url)
            fqrn = repo.fqrn
        except cvmfs.repository.RepositoryNotFound, e:
            raise forms.ValidationError(
                "The URL '%s' does not point to a CVMFS repository" % url)

        try:
            stratum0 = Stratum0.objects.get(fqrn=fqrn)
            if stratum0:
                raise forms.ValidationError(
                    "The URL '%s' points to the repository '%s' which is already used by '%s'." % (url, fqrn, stratum0.name))
        except ObjectDoesNotExist, e:
            pass

        return self.cleaned_data


class Stratum0Admin(admin.ModelAdmin):
    fields       = ['name', 'url']
    form         = Stratum0AdminForm
    list_display = ['name', 'fqrn', 'url' ]

    def save_model(self, request, obj, form, change):
        # availability of <obj.url> was checked in Stratum1AdminForm.clean
        repo     = cvmfs.repository.RemoteRepository(obj.url)
        obj.fqrn = repo.fqrn
        super(Stratum0Admin, self).save_model(request, obj, form, change)



class Stratum1AdminForm(forms.ModelForm):
    class Meta:
        model = Stratum1

    def clean(self):
        """
        checks if the provided repository is available and is a replica of a
        locally defined stratum 0 repository
        """
        url  = self.cleaned_data['url']
        fqrn = ""

        try:
            repo = cvmfs.repository.RemoteRepository(url)
            fqrn = repo.fqrn
        except cvmfs.repository.RepositoryNotFound, e:
            raise forms.ValidationError("The URL '%s' does not point to a CVMFS replica" % url)

        repo = Stratum0.objects.filter(fqrn=fqrn)
        if not repo:
            raise forms.ValidationError("The Stratum 0 of '%s' is not registered." % fqrn)

        return self.cleaned_data


class Stratum1Admin(admin.ModelAdmin):
    fields       = ['replication_site', 'url' ]
    form         = Stratum1AdminForm
    list_display = ['replication_site', 'stratum0', 'url' ]
    list_filter  = ['stratum0']

    def save_model(self, request, obj, form, change):
        # availability of <obj.url> and stratum0 was checked in Stratum1AdminForm.clean
        repo         = cvmfs.repository.RemoteRepository(obj.url)
        stratum0     = Stratum0.objects.get(fqrn=repo.fqrn)
        obj.stratum0 = stratum0
        super(Stratum1Admin, self).save_model(request, obj, form, change)


admin.site.register(Stratum0, Stratum0Admin)
admin.site.register(Stratum1, Stratum1Admin)
admin.site.register(ReplicationSite)

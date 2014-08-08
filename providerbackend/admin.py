from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ugettext as _

from providerbackend.models import ProviderManagePy
from providerbackend.models import ProviderMetaData
from providerbackend.models import Repository
from providerbackend.models import Unit
from providerbackend.models import Job


class ProviderManagePyInline(admin.StackedInline):
    model = ProviderManagePy


class RepositoryAdmin(admin.ModelAdmin):
    list_display = 'url', 'vcs'
    readonly_fields = 'updated_on', 'added_on', 'probed_on'
    inlines = [ProviderManagePyInline]
    actions = ['probe_repo']

    def probe_repo(self, request, queryset):
        for repo in queryset:
            try:
                repo.probe()
            except Exception as exc:
                self.message_user(
                    request, "Unable to probe: {0}: {1!r}".format(
                        repo.url, exc), level=messages.ERROR)
    probe_repo.short_description = _("Probe repository for providers")


class ProviderManagePyAdmin(admin.ModelAdmin):
    list_display = 'repo', 'path'
    readonly_fields = 'repo', 'path', 'problem'


class ProviderMetaDataAdmin(admin.ModelAdmin):
    list_display = 'pb_id', 'version'
    readonly_fields = ('manage_py', 'pb_id', 'namespace', 'version',
                       'description', 'gettext_domain',)


class UnitAdmin(admin.ModelAdmin):
    list_display = 'pb_id', 'unit'


class JobAdmin(admin.ModelAdmin):
    list_display = 'unit', 'plugin', 'summary'
    readonly_fields = ('unit', 'name', 'summary', 'plugin', 'command',
                       'description', 'user', 'environ', 'estimated_duration',
                       'depends', 'requires', 'shell')


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(ProviderManagePy, ProviderManagePyAdmin)
admin.site.register(ProviderMetaData, ProviderMetaDataAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Job, JobAdmin)

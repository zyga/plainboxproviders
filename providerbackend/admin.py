from django.contrib import admin
from django.utils.translation import ugettext as _

from providerbackend.models import ProviderManagePy
from providerbackend.models import ProviderMetaData
from providerbackend.models import Repository
from providerbackend.models import Unit


class ProviderManagePyInline(admin.StackedInline):
    model = ProviderManagePy


def probe_repo(modeladmin, request, queryset):
    for repo in queryset:
        repo.probe()
probe_repo.short_description = _("Probe repository for providers")


class RepositoryAdmin(admin.ModelAdmin):
    list_display = 'url', 'vcs'
    readonly_fields = 'updated_on', 'added_on', 'probed_on'
    inlines = [ProviderManagePyInline]
    actions = [probe_repo]


class ProviderManagePyAdmin(admin.ModelAdmin):
    list_display = 'repo', 'path'
    readonly_fields = 'repo', 'path', 'problem'


class ProviderMetaDataAdmin(admin.ModelAdmin):
    list_display = 'pb_id', 'version'
    readonly_fields = ('manage_py', 'pb_id', 'namespace', 'version',
                       'description', 'gettext_domain',)


class UnitAdmin(admin.ModelAdmin):
    list_display = 'pb_id', 'unit'


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(ProviderManagePy, ProviderManagePyAdmin)
admin.site.register(ProviderMetaData, ProviderMetaDataAdmin)
admin.site.register(Unit, UnitAdmin)

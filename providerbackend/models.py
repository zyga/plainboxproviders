from importlib.machinery import SourceFileLoader
from subprocess import check_call
from tempfile import TemporaryDirectory
import datetime
import os

from django.db import models
from django.utils.translation import ugettext as _

from plainbox.impl.secure.config import Unset
from plainbox.impl.secure.providers.v1 import Provider1
from plainbox.impl.secure.providers.v1 import Provider1Definition


class Repository(models.Model):
    """
    A code repository to monitor for providers
    """

    url = models.CharField(
        max_length=4096,
        help_text=_("vcs-specific URL or path for 'local' vcs"))
    vcs = models.CharField(max_length=16, choices=[
        ('bzr', _("Bazaar")),
        ('git', _("Git")),
        ('local', _("Local Directory")),
    ])
    updated_on = models.DateTimeField(auto_now=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    probed_on = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name = _("repository")
        verbose_name_plural = _("repositories")

    def probe(self):
        with TemporaryDirectory() as dirname:
            root_dir = self.checkout_to(dirname)
            for pathname in self.find_manage_scripts(root_dir):
                manage_py, created = ProviderManagePy.objects.get_or_create(
                    repo=self,
                    path=os.path.relpath(pathname, root_dir))
                try:
                    provider = self.load_provider(pathname)
                except ValueError as exc:
                    manage_py.problem = str(exc)
                else:
                    manage_py.problem = None
                    self.mirror(provider, manage_py)
        self.probed_on = datetime.datetime.now()

    def checkout_to(self, dirname):
        if self.vcs == 'bzr':
            check_call([
                'bzr', 'checkout', '--quiet', '--lightweight',
                self.url, dirname])
            return dirname
        elif self.vcs == 'git':
            check_call(['git', 'clone', self.url, dirname])
            return dirname
        elif self.vcs == 'local':
            return self.url
        else:
            raise NotImplementedError(
                "cannot handle vcs {0!r}".format(self.vcs))

    def find_manage_scripts(self, dirname):
        for root, dirs, files in os.walk(dirname):
            for filename in files:
                if filename == 'manage.py':
                    pathname = os.path.join(root, filename)
                    if self.is_manage_script(pathname):
                        yield pathname

    def is_manage_script(self, pathname):
        with open(pathname, 'rt', encoding='UTF-8') as stream:
            for index, line in enumerate(stream):
                if index > 10:
                    break
                if 'plainbox.provider_manager' in line:
                    return True
                if line == '# this is a plainbox provider':
                    return True

    def load_provider(self, manage_py):
        from plainbox import provider_manager
        from providerbackend import fake_provider_manager
        provider_manager.setup = fake_provider_manager.setup
        loader = SourceFileLoader('manage', manage_py)
        loader.load_module()
        if len(fake_provider_manager.all_setup_kwargs) == 0:
            raise ValueError("provider not defined")
        kwargs = fake_provider_manager.all_setup_kwargs.pop()
        location = os.path.dirname(os.path.abspath(manage_py))
        definition = Provider1Definition()
        definition.location = location
        definition.name = kwargs.get('name', None)
        definition.version = kwargs.get('version', None)
        definition.description = kwargs.get('description', None)
        definition.gettext_domain = kwargs.get('gettext_domain', Unset)
        return Provider1.from_definition(definition, secure=False)

    def mirror(self, provider, manage_py):
        metadata, created = ProviderMetaData.objects.get_or_create(
            manage_py=manage_py)
        metadata.pb_id = provider.name
        metadata.namespace = provider.namespace
        metadata.version = provider.version
        metadata.description = provider.description
        metadata.gettext_domain = provider.gettext_domain
        if created:
            metadata.save()
        units, problems = provider.get_units()
        for unit in units:
            unit_model, created = Unit.objects.get_or_create(
                provider_metadata=metadata, pb_id=unit.id)
            unit_model.unit = unit.unit
            if created:
                unit_model.save()
            if unit_model.unit == 'job':
                self.mirror_job(unit, unit_model)

    def mirror_job(self, job, unit_model):
        job_model, created = Job.objects.get_or_create(unit=unit_model)
        job_model.name = job.name
        job_model.summary = job.summary
        job_model.plugin = job.plugin
        job_model.command = job.command
        job_model.description = job.description
        job_model.user = job.user
        job_model.environ = job.environ
        job_model.estimated_duration = job.estimated_duration
        job_model.depends = job.depends
        job_model.requires = job.requires
        job_model.shell = job.shell
        if created:
            job_model.save()


class ProviderManagePy(models.Model):
    """
    A manage.py file representing a single provider
    """

    repo = models.ForeignKey(Repository, verbose_name="related repository")
    path = models.CharField(
        max_length=1024,
        help_text=_("path to manage.py within the repository"))
    problem = models.TextField(null=True)

    class Meta:
        verbose_name = _("provider manage.py file")
        verbose_name_plural = _("provider manage.py files")


class ProviderMetaData(models.Model):
    """
    A PlainBox provider (metadata), most data (units) is modelled by
    :class:`Unit` below.
    """
    manage_py = models.OneToOneField(ProviderManagePy, primary_key=True)
    # id is not primary_key because we want to help to detect duplicates within
    # the community, it's mostly unique but explicitly not so
    pb_id = models.CharField(max_length=1024)
    # Namespace is currently always derived from the id
    namespace = models.CharField(max_length=1024, editable=False)
    version = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024, blank=True)
    gettext_domain = models.CharField(max_length=1024, null=True)

    def __unicode__(self):
        return self.pb_id

    class Meta:
        verbose_name = _("provider metadata")
        verbose_name_plural = _("provider metadata")


class Unit(models.Model):
    """
    Units are objects loaded from a provider
    """
    # id is not primary_key because we want to help to detect duplicates within
    # the community, it's mostly unique but explicitly not so
    pb_id = models.CharField(max_length=1024)
    unit = models.CharField(max_length=1024)
    provider_metadata = models.ForeignKey(
        ProviderMetaData, verbose_name="related provider")

    def __unicode__(self):
        return self.pb_id


class Job(models.Model):
    unit = models.OneToOneField(Unit, primary_key=True)
    name = models.CharField(max_length=1024, null=True)
    summary = models.CharField(max_length=1024, null=True)
    plugin = models.CharField(max_length=1024, null=True)
    command = models.CharField(max_length=1024, null=True)
    description = models.TextField(null=True)
    user = models.CharField(max_length=1024, null=True)
    environ = models.TextField(null=True)
    estimated_duration = models.CharField(max_length=1024, null=True)
    depends = models.TextField(null=True)
    requires = models.TextField(null=True)
    shell = models.CharField(max_length=1024, null=True)

    def __unicode__(self):
        return self.unit.pb_id

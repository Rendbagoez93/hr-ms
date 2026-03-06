from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.base_models import BaseModel


class JobTitleQuerySet(models.QuerySet["JobTitle"]):
    def active(self) -> "JobTitleQuerySet":
        return self.filter(is_active=True)


class JobTitle(BaseModel):
    title = models.CharField(_("title"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True, default="")

    objects = JobTitleQuerySet.as_manager()

    class Meta:
        verbose_name = _("job title")
        verbose_name_plural = _("job titles")
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

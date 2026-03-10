from django.conf import settings
from django.core.management.base import BaseCommand

from applications.company_profile.services import seed_from_yaml


class Command(BaseCommand):
    help = "Seed the CompanyProfile table from company_config.yaml"

    def handle(self, *_args, **_options) -> None:
        company_config = getattr(settings, "COMPANY_PROFILE", None)
        if company_config is None:
            self.stderr.write(self.style.ERROR("COMPANY_PROFILE not found in settings."))
            return
        profile = seed_from_yaml(company_config)
        self.stdout.write(self.style.SUCCESS(f"CompanyProfile seeded: {profile.name}"))

# - coding: utf-8 -
from django.apps import apps
from django.core.management import call_command
from django.db.models.signals import post_migrate


def load_fixtures(sender, **kwargs):
    call_command(
        'loaddata',
        'countries.json'
    )


post_migrate.connect(load_fixtures,
                     sender=apps.get_app_config('app_api'))

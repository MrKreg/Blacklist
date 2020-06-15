from django.apps import AppConfig


class DomainsConfig(AppConfig):
    name = 'app.pkg.domains'

    def ready(self):
        import app.pkg.domains.signal_hndls

from django.apps import AppConfig


class ApplyConfig(AppConfig):
    name = 'apply'

    def ready(self):
        import users.signals
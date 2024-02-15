from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "balfolk_music.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import balfolk_music.users.signals  # noqa: F401
        except ImportError:
            pass

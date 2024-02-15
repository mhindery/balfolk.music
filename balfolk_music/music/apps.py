from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MusicConfig(AppConfig):
    name = "balfolk_music.music"
    verbose_name = _("Music")

    def ready(self):
        try:
            import balfolk_music.music.signals  # noqa: F401
        except ImportError:
            pass

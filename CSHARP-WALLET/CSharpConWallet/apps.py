"""This module is used to provide Application config
"""
from django.apps import AppConfig


class CSharpConWalletConfig(AppConfig):
    """_summary_

    Args:
        AppConfig
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "CSharpConWallet"
    verbose_name = "CSharpConWallet"

    def ready(self):
        """_summary_

        Args:
            self
        """

        from CSharpConWallet import user_task

        user_task.start()

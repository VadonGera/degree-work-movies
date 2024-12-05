import logging
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver
from django.utils.timezone import now

# Настраиваем логгер для аутентификации
auth_logger = logging.getLogger("auth")


@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    auth_logger.info(
        "Пользователь с id %s вошел в систему. IP: %s, Время: %s",
        user.id,
        request.META.get("REMOTE_ADDR"),
        now(),
    )


@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    auth_logger.info(
        "Пользователь с id %s вышел из системы. IP: %s, Время: %s",
        user.id,
        request.META.get("REMOTE_ADDR"),
        now(),
    )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    auth_logger.warning(
        "Неудачная попытка входа. Имя пользователя: %s, IP: %s, Время: %s",
        credentials.get("username"),
        request.META.get("REMOTE_ADDR"),
        now(),
    )

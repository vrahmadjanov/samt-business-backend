from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator


class BusinessUserManager(BaseUserManager):
    """Менеджер пользователей для бизнес-админки (аутентификация по email)."""

    def create_user(self, phone_number: str, password: str | None = None, **extra_fields):
        if not phone_number:
            raise ValueError("Требуется номер телефона")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone_number, password, **extra_fields)


class BusinessUser(AbstractBaseUser, PermissionsMixin):
    """Кастомный пользователь бизнес-системы: логин по email, без username."""

    phone_regex = RegexValidator(regex=r'^\+992\d{9}$', message='Формат номера: "+992XXYYYYYY"')
    phone_number = models.CharField(max_length=13, unique=True, validators=[phone_regex])
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BusinessUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = "Пользователь (business)"
        verbose_name_plural = "Пользователи (business)"

    def __str__(self) -> str:
        return self.phone_number


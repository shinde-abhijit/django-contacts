from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    Group,
    Permission,
)
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import os
from datetime import datetime
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def user_profile_image_path(instance, filename):
    ext = filename.split(".")[-1]
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    # sanitize email and contact (replace @ and . to _)
    email_sanitized = instance.email.replace("@", "_").replace(".", "_")
    contact_sanitized = instance.contact if instance.contact else "nocontact"
    filename = f"{email_sanitized}_{contact_sanitized}_{datetime_str}.{ext}"
    return os.path.join("account_profiles/", filename)


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, username, first_name, last_name, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("The Email must be set")
        if not username:
            raise ValueError("The Username must be set")
        if not first_name:
            raise ValueError("The First name must be set")
        if not last_name:
            raise ValueError("The Last name must be set")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, username, first_name, last_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email, username, first_name, last_name, password, **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15, unique=True, blank=True)
    image = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)
    bio = models.TextField(blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # change from 'user_set' to 'customuser_set'
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # change from 'user_set' to 'customuser_set'
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]  # required when using createsuperuser

    objects = CustomUserManager()

    def clean(self):
        # Model-level validation
        if not self.first_name:
            raise ValidationError("First name cannot be blank")
        if not self.last_name:
            raise ValidationError("Last name cannot be blank")
        if not self.email:
            raise ValidationError("Email cannot be blank")
        if not self.username:
            raise ValidationError("Username cannot be blank")
        # Check unique contact if contact is set (not blank)
        if self.contact:
            qs = CustomUser.objects.filter(contact=self.contact)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({"contact": "Contact must be unique."})

    def save(self, *args, **kwargs):
        # Call full_clean to run validations (optional)
        self.full_clean()

        # Check if there's an image and if it's newly uploaded or changed
        # inside your CustomUser model's save method
        if self.image:
            img = Image.open(self.image)
            if img.mode != "RGB":
                img = img.convert("RGB")
            img = img.resize((400, 400), Image.Resampling.LANCZOS)

            img_io = BytesIO()
            img.save(img_io, format="JPEG", quality=85)
            img_content = ContentFile(img_io.getvalue(), self.image.name)
            self.image.save(self.image.name, img_content, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}, {self.email}, {self.first_name} {self.last_name}"

    class Meta:
        unique_together = (("contact", "username"),)

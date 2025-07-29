import re
import os
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from django.utils import timezone
from datetime import datetime
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def rename_contact_image(instance, filename):
    base, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    first = (
        instance.first_name.replace(" ", "_").lower()
        if instance.first_name
        else "no_firstname"
    )
    last = (
        instance.last_name.replace(" ", "_").lower()
        if instance.last_name
        else "no_lastname"
    )
    contact = instance.contact if instance.contact else "nocontact"
    new_filename = f"{first}_{last}_{contact}_{timestamp}{ext}"
    return os.path.join("contact_photos", new_filename)


class ContactList(models.Model):

    GENDER_CHOICE = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]

    CONTACT_TYPE = [
        ("personal", "Personal"),
        ("family", "Family"),
        ("friend", "Friend"),
        ("work", "Work"),
        ("client", "Client"),
        ("vendor", "Vendor"),
        ("emergency", "Emergency"),
        ("other", "Other"),
    ]

    COMMUNICATION_METHOD = [
        ("phone", "Phone Call"),
        ("email", "Email"),
        ("sms", "SMS/Text"),
        ("whatsapp", "WhatsApp"),
        ("telegram", "Telegram"),
        ("zoom", "Zoom"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="contacts"
    )
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    contact = models.CharField(max_length=13, blank=False)
    alternate_contact = models.CharField(max_length=13, blank=True)
    email = models.EmailField(blank=True, null=True)
    alternate_email = models.EmailField(blank=True, null=True)

    contact_type = models.CharField(
        max_length=20, choices=CONTACT_TYPE, default="personal"
    )
    preferred_communication = models.CharField(
        max_length=20, choices=COMMUNICATION_METHOD, blank=True, null=True
    )

    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, blank=False)
    nickname = models.CharField(max_length=30, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=75)
    state = models.CharField(max_length=75)
    country = models.CharField(max_length=75)
    postal_code = models.CharField(max_length=20)

    linkedin_username = models.CharField(max_length=50, blank=True)
    twitter_username = models.CharField(max_length=50, blank=True)
    facebook_username = models.CharField(max_length=50, blank=True)
    instagram_username = models.CharField(max_length=50, blank=True)

    notes = models.TextField(blank=True)
    contact_photo = models.ImageField(
        upload_to=rename_contact_image, blank=True, null=True
    )
    is_favorite = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="contact_added_by",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="contact_updated_by",
    )

    def clean(self):
        # First Name
        if not self.first_name:
            raise ValidationError({"first_name": "First name is required."})
        if not re.fullmatch(r"^[A-Za-z ]+$", self.first_name):
            raise ValidationError(
                {"first_name": "First name must contain only alphabets and spaces."}
            )

        # Last Name
        if not self.last_name:
            raise ValidationError({"last_name": "Last name is required."})
        if not re.fullmatch(r"^[A-Za-z ]+$", self.last_name):
            raise ValidationError(
                {"last_name": "Last name must contain only alphabets and spaces."}
            )

        # Contact
        if not self.contact:
            raise ValidationError({"contact": "Contact number is required."})
        if not re.fullmatch(r"^\d{10,13}$", self.contact):
            raise ValidationError(
                {"contact": "Contact must be digits only and 10 to 13 characters long."}
            )

        # Alternate Contact
        if self.alternate_contact:
            if not re.fullmatch(r"^\d{10,13}$", self.alternate_contact):
                raise ValidationError(
                    {
                        "alternate_contact": "Alternate contact must be digits only and 10 to 13 characters long."
                    }
                )

        # Email
        if self.email:
            if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", self.email):
                raise ValidationError({"email": "Enter a valid email address."})

        # Alternate Email
        if self.alternate_email:
            if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", self.alternate_email):
                raise ValidationError(
                    {"alternate_email": "Enter a valid alternate email address."}
                )

        # Date of Birth
        if self.date_of_birth:
            if self.date_of_birth > timezone.now().date():
                raise ValidationError(
                    {"date_of_birth": "Date of birth cannot be in the future."}
                )

        # Nickname
        if self.nickname:
            if not re.fullmatch(r"^[A-Za-z ]+$", self.nickname):
                raise ValidationError(
                    {"nickname": "Nickname must contain only alphabets and spaces."}
                )

        # Job Title
        if self.job_title:
            if not re.fullmatch(r"^[A-Za-z ]+$", self.job_title):
                raise ValidationError(
                    {"job_title": "Job title must contain only alphabets and spaces."}
                )

        # Company
        if self.company:
            if not re.fullmatch(r"^[A-Za-z ]+$", self.company):
                raise ValidationError(
                    {"company": "Company name must contain only alphabets and spaces."}
                )

        # City
        if self.city:
            if not re.fullmatch(r"^[A-Za-z ]+$", self.city):
                raise ValidationError(
                    {"city": "City must contain only alphabets and spaces."}
                )

        # State
        if self.state:
            if not re.fullmatch(r"^[A-Za-z ]+$", self.state):
                raise ValidationError(
                    {"state": "State must contain only alphabets and spaces."}
                )

        # Country
        if self.country:
            if not re.fullmatch(r"^[A-Za-z ]+$", self.country):
                raise ValidationError(
                    {"country": "Country must contain only alphabets and spaces."}
                )

        # Postal Code
        if self.postal_code:
            if not re.fullmatch(r"^\d+$", self.postal_code):
                raise ValidationError(
                    {"postal_code": "Postal code must contain digits only."}
                )

        # LinkedIn Username
        if self.linkedin_username:
            if not re.fullmatch(r"^[\w ]+$", self.linkedin_username):
                raise ValidationError(
                    {
                        "linkedin_username": "LinkedIn username can contain letters, numbers, and spaces only."
                    }
                )

        # Twitter Username
        if self.twitter_username:
            if not re.fullmatch(r"^[\w ]+$", self.twitter_username):
                raise ValidationError(
                    {
                        "twitter_username": "Twitter username can contain letters, numbers, and spaces only."
                    }
                )

        # Facebook Username
        if self.facebook_username:
            if not re.fullmatch(r"^[\w ]+$", self.facebook_username):
                raise ValidationError(
                    {
                        "facebook_username": "Facebook username can contain letters, numbers, and spaces only."
                    }
                )

        # Instagram Username
        if self.instagram_username:
            if not re.fullmatch(r"^[\w ]+$", self.instagram_username):
                raise ValidationError(
                    {
                        "instagram_username": "Instagram username can contain letters, numbers, and spaces only."
                    }
                )

        if self.contact_photo:
            valid_extensions = [".jpg", ".jpeg", ".png"]
            ext = os.path.splitext(self.contact_photo.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError(
                    {"contact_photo": "Only .png, .jpg, and .jpeg files are allowed."}
                )

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.contact_photo:
            img = Image.open(self.contact_photo)

            if img.mode != "RGB":
                img = img.convert("RGB")  # ensure compatibility

            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=70)  # Adjust quality if needed
            buffer.seek(0)

            # Replace the original image with the compressed one
            file_name = os.path.basename(self.contact_photo.name)
            self.contact_photo.save(file_name, ContentFile(buffer.read()), save=False)

        super().save(*args, **kwargs)

        def __str__(self):
            return f"{self.user.id} {self.first_name} {self.last_name} {self.contact}"

        class Meta:
            verbose_name = "Contact List"
            verbose_name_plural = "Contacts"

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta
from io import BytesIO
from PIL import Image

# import os

from contacts.models import ContactList  # Adjust this import to your app name

User = get_user_model()


class ContactListModelTest(TestCase):

    def setUp(self):
        # Create a user to associate with contacts
        self.user = User.objects.create_user(
            email="user@example.com",
            username="user1",
            first_name="User",
            last_name="Test",
            password="password123",
        )

    def generate_test_image(self, color=(255, 0, 0)):
        img = Image.new("RGB", (800, 800), color=color)
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return SimpleUploadedFile("test.jpg", buffer.read(), content_type="image/jpeg")

    def test_valid_contactlist_save_and_image_compression(self):
        contact = ContactList(
            user=self.user,
            first_name="John",
            last_name="Doe",
            contact="1234567890",
            email="john@example.com",
            gender="Male",
            address="123 Main St",
            city="New York",
            state="New York",
            country="USA",
            postal_code="12345",
        )
        contact.contact_photo = self.generate_test_image()
        contact.full_clean()  # Should not raise ValidationError
        contact.save()

        # Check instance saved correctly
        self.assertEqual(contact.first_name, "John")

        # Check image was compressed and saved
        saved_img = Image.open(contact.contact_photo.path)
        self.assertTrue(saved_img.format in ["JPEG", "JPG"])

    def test_missing_required_fields_raises_validation_error(self):
        contact = ContactList(user=self.user)
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()
        self.assertIn("first_name", cm.exception.message_dict)
        self.assertIn("last_name", cm.exception.message_dict)
        self.assertIn("contact", cm.exception.message_dict)
        self.assertIn("gender", cm.exception.message_dict)
        self.assertIn("address", cm.exception.message_dict)

    def test_invalid_first_name_raises_validation_error(self):
        contact = ContactList(
            user=self.user,
            first_name="John123",  # invalid chars
            last_name="Doe",
            contact="1234567890",
            gender="Male",
            address="123 Main St",
            city="New York",
            state="New York",
            country="USA",
            postal_code="12345",
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()
        self.assertIn("first_name", cm.exception.message_dict)

    def test_invalid_contact_number_length(self):
        contact = ContactList(
            user=self.user,
            first_name="John",
            last_name="Doe",
            contact="12345",  # too short
            gender="Male",
            address="123 Main St",
            city="New York",
            state="New York",
            country="USA",
            postal_code="12345",
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()
        self.assertIn("contact", cm.exception.message_dict)

    def test_alternate_contact_validation(self):
        contact = ContactList(
            user=self.user,
            first_name="John",
            last_name="Doe",
            contact="1234567890",
            alternate_contact="invalid",  # non-digit
            gender="Male",
            address="123 Main St",
            city="New York",
            state="New York",
            country="USA",
            postal_code="12345",
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()
        self.assertIn("alternate_contact", cm.exception.message_dict)

    def test_date_of_birth_in_future_raises_validation_error(self):
        future_date = date.today() + timedelta(days=10)
        contact = ContactList(
            user=self.user,
            first_name="John",
            last_name="Doe",
            contact="1234567890",
            gender="Male",
            address="123 Main St",
            city="New York",
            state="New York",
            country="USA",
            postal_code="12345",
            date_of_birth=future_date,
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()
        self.assertIn("date_of_birth", cm.exception.message_dict)

    def test_invalid_email_raises_validation_error(self):
        contact = ContactList(
            user=self.user,
            first_name="John",
            last_name="Doe",
            contact="1234567890",
            email="invalid-email",
            gender="Male",
            address="123 Main St",
            city="New York",
            state="New York",
            country="USA",
            postal_code="12345",
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()
        self.assertIn("email", cm.exception.message_dict)

    def test_invalid_postal_code_raises_validation_error(self):
        contact = ContactList(
            user=self.user,
            first_name="John",
            last_name="Doe",
            contact="1234567890",
            gender="Male",
            address="123 Main St",
            city="New York",
            state="New York",
            country="USA",
            postal_code="12AB3",
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()
        self.assertIn("postal_code", cm.exception.message_dict)

    def test_invalid_social_usernames(self):
        # Example for LinkedIn username
        contact = ContactList(
            user=self.user,
            first_name="John",
            last_name="Doe",
            contact="1234567890",
            linkedin_username="john@doe!",  # invalid characters
            gender="Male",
            address="123 Main St",
            city="New York",
            state="New York",
            country="USA",
            postal_code="12345",
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()
        self.assertIn("linkedin_username", cm.exception.message_dict)

    def test_invalid_image_extension_raises_validation_error(self):
        # Create a dummy file with .txt extension for contact_photo
        invalid_file = SimpleUploadedFile(
            "file.txt", b"file_content", content_type="text/plain"
        )

        contact = ContactList(
            user=self.user,
            first_name="John",
            last_name="Doe",
            contact="1234567890",
            gender="Male",
            address="123 Main St",
            city="New York",
            state="New York",
            country="USA",
            postal_code="12345",
            contact_photo=invalid_file,
        )
        with self.assertRaises(ValidationError) as cm:
            contact.full_clean()
        self.assertIn("contact_photo", cm.exception.message_dict)

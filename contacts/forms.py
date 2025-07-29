from django import forms
from .models import ContactList
import re
import os
from django.utils import timezone
from accounts.utils import tailwind_text_classes

contact_list_tailwind_classes = (
    " w-full p-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none "
    " mt-1 mb-1 "
    " focus:ring-2 focus:ring-indigo-600 duration-300 "
    " hover:ring-2 hover:ring-indigo-400 "
)


class ContactListForm(forms.ModelForm):
    class Meta:
        model = ContactList
        fields = [
            "first_name",
            "last_name",
            "contact",
            "alternate_contact",
            "email",
            "alternate_email",
            "contact_type",
            "preferred_communication",
            "date_of_birth",
            "gender",
            "nickname",
            "job_title",
            "company",
            "website",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "linkedin_username",
            "twitter_username",
            "facebook_username",
            "instagram_username",
            "notes",
            "contact_photo",
            "is_favorite",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "First Name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Last Name",
                }
            ),
            "contact": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Primary Contact Number",
                }
            ),
            "alternate_contact": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Alternate Contact Number",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Email Address",
                }
            ),
            "alternate_email": forms.EmailInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Alternate Email Address",
                }
            ),
            "contact_type": forms.Select(
                attrs={
                    "class": contact_list_tailwind_classes,
                }
            ),
            "preferred_communication": forms.Select(
                attrs={
                    "class": contact_list_tailwind_classes,
                }
            ),
            "date_of_birth": forms.DateInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "type": "date",
                }
            ),
            "gender": forms.Select(
                attrs={
                    "class": contact_list_tailwind_classes,
                }
            ),
            "nickname": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Nickname",
                }
            ),
            "job_title": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Job Title",
                }
            ),
            "company": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Company",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Website URL",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": contact_list_tailwind_classes + tailwind_text_classes,
                    "rows": 3,
                    "placeholder": "Address",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "City",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "State",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Country",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Postal Code",
                }
            ),
            "linkedin_username": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "LinkedIn Username",
                }
            ),
            "twitter_username": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Twitter Username",
                }
            ),
            "facebook_username": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Facebook Username",
                }
            ),
            "instagram_username": forms.TextInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                    "placeholder": "Instagram Username",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": contact_list_tailwind_classes + tailwind_text_classes,
                    "rows": 4,
                    "placeholder": "Additional Notes",
                }
            ),
            "contact_photo": forms.ClearableFileInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                }
            ),
            "is_favorite": forms.CheckboxInput(
                attrs={
                    "class": contact_list_tailwind_classes,
                }
            ),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not re.fullmatch(r"^[A-Za-z ]+$", first_name or ""):
            raise forms.ValidationError(
                "First name must contain only alphabets and spaces."
            )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not re.fullmatch(r"^[A-Za-z ]+$", last_name or ""):
            raise forms.ValidationError(
                "Last name must contain only alphabets and spaces."
            )
        return last_name

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if not re.fullmatch(r"^\d{10,13}$", contact or ""):
            raise forms.ValidationError(
                "Contact must be digits only and 10 to 13 characters long."
            )
        return contact

    def clean_alternate_contact(self):
        alternate = self.cleaned_data.get("alternate_contact")
        if alternate and not re.fullmatch(r"^\d{10,13}$", alternate):
            raise forms.ValidationError(
                "Alternate contact must be digits only and 10 to 13 characters long."
            )
        return alternate

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean_alternate_email(self):
        email = self.cleaned_data.get("alternate_email")
        if email and not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise forms.ValidationError("Enter a valid alternate email address.")
        return email

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        if dob and dob > timezone.now().date():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return dob

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        if nickname and not re.fullmatch(r"^[A-Za-z ]+$", nickname):
            raise forms.ValidationError(
                "Nickname must contain only alphabets and spaces."
            )
        return nickname

    def clean_job_title(self):
        job = self.cleaned_data.get("job_title")
        if job and not re.fullmatch(r"^[A-Za-z ]+$", job):
            raise forms.ValidationError(
                "Job title must contain only alphabets and spaces."
            )
        return job

    def clean_company(self):
        company = self.cleaned_data.get("company")
        if company and not re.fullmatch(r"^[A-Za-z ]+$", company):
            raise forms.ValidationError(
                "Company must contain only alphabets and spaces."
            )
        return company

    def clean_city(self):
        city = self.cleaned_data.get("city")
        if city and not re.fullmatch(r"^[A-Za-z ]+$", city):
            raise forms.ValidationError("City must contain only alphabets and spaces.")
        return city

    def clean_state(self):
        state = self.cleaned_data.get("state")
        if state and not re.fullmatch(r"^[A-Za-z ]+$", state):
            raise forms.ValidationError("State must contain only alphabets and spaces.")
        return state

    def clean_country(self):
        country = self.cleaned_data.get("country")
        if country and not re.fullmatch(r"^[A-Za-z ]+$", country):
            raise forms.ValidationError(
                "Country must contain only alphabets and spaces."
            )
        return country

    def clean_postal_code(self):
        postal = self.cleaned_data.get("postal_code")
        if postal and not re.fullmatch(r"^\d+$", postal):
            raise forms.ValidationError("Postal code must contain digits only.")
        return postal

    def clean_linkedin_username(self):
        username = self.cleaned_data.get("linkedin_username")
        if username and not re.fullmatch(r"^[\w ]+$", username):
            raise forms.ValidationError(
                "LinkedIn username can contain letters, numbers, and spaces only."
            )
        return username

    def clean_twitter_username(self):
        username = self.cleaned_data.get("twitter_username")
        if username and not re.fullmatch(r"^[\w ]+$", username):
            raise forms.ValidationError(
                "Twitter username can contain letters, numbers, and spaces only."
            )
        return username

    def clean_facebook_username(self):
        username = self.cleaned_data.get("facebook_username")
        if username and not re.fullmatch(r"^[\w ]+$", username):
            raise forms.ValidationError(
                "Facebook username can contain letters, numbers, and spaces only."
            )
        return username

    def clean_instagram_username(self):
        username = self.cleaned_data.get("instagram_username")
        if username and not re.fullmatch(r"^[\w ]+$", username):
            raise forms.ValidationError(
                "Instagram username can contain letters, numbers, and spaces only."
            )
        return username

    def clean_contact_photo(self):
        image = self.cleaned_data.get("contact_photo")
        if image:
            valid_extensions = [".jpg", ".jpeg", ".png"]
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    "Only .png, .jpg, and .jpeg files are allowed."
                )
        return image

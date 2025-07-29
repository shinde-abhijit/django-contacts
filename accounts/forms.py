from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .utils import (
    tailwind_register_classes,
    tailwind_file_classes,
    tailwind_text_classes,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "contact",
            "image",
            "bio",
        ]
        labels = {
            "email": "Email",
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "contact": "Contact",
            "image": "Profile Picture",
            "bio": "Add Bio",
        }
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "class": tailwind_register_classes,
                    "type": "email",
                    "placeholder": "Enter Email Address",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": tailwind_register_classes,
                    "type": "text",
                    "placeholder": "Enter Username",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": tailwind_register_classes,
                    "type": "text",
                    "placeholder": "Enter First Name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": tailwind_register_classes,
                    "type": "text",
                    "placeholder": "Enter Last Name",
                }
            ),
            "contact": forms.TextInput(
                attrs={
                    "class": tailwind_register_classes,
                    "type": "text",
                    "placeholder": "Enter Contact Number",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": tailwind_file_classes,
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": tailwind_register_classes + tailwind_text_classes,
                    "type": "text",
                    "placeholder": "Enter User Bio",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Tailwind classes and placeholders to password fields
        self.fields["password1"].widget.attrs.update(
            {
                "class": tailwind_register_classes,
                "placeholder": "Enter Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": tailwind_register_classes,
                "placeholder": "Confirm Password",
            }
        )


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "contact", "image", "bio"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": tailwind_register_classes,
                    "type": "text",
                    "placeholder": "Enter Username",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": tailwind_register_classes,
                    "type": "text",
                    "placeholder": "Enter First Name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": tailwind_register_classes,
                    "type": "text",
                    "placeholder": "Enter Last Name",
                }
            ),
            "contact": forms.TextInput(
                attrs={
                    "class": tailwind_register_classes,
                    "type": "text",
                    "placeholder": "Enter Contact Number",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": tailwind_file_classes,
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": tailwind_register_classes,
                    "type": "text",
                    "placeholder": "Enter User Bio",
                }
            ),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": tailwind_register_classes,
                "placeholder": "Enter your email",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": tailwind_register_classes,
                "placeholder": "Enter your password",
            }
        )
    )


class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": tailwind_register_classes,
                "placeholder": "Confirm your password",
            }
        ),
        label="Confirm Password",
    )

from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Room

User = get_user_model()

class RegisterForm(forms.ModelForm):
    """
    The default 

    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Set Password',
        'class': 'form-control',
    }))
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': "form-control", 
                'placeholder': 'Your Email'
            })
        }

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = ['email']
        # widgets = {
        #     'email': forms.EmailInput(attrs={
        #         'class': "form-control", 
        #         'placeholder': 'Your Email'
        #     })
        # }

    # def clean_password(self):
    #     # Regardless of what the user provides, return the initial value.
    #     # This is done here, rather than on the field, because the
    #     # field does not have access to the initial value
    #     return self.initial["password"]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'date', 'advance_booking', 'defined_check_in_time', 'defined_check_out_time')
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Room Name'}),
            'date': forms.DateInput(attrs={'class': "form-control", 'type': "date"}),
            'advance_booking': forms.NumberInput(attrs={'class': "form-control", 'placeholder': 'Advance Booking (default = 3 days)', 'type': "number"}),
            'defined_check_in_time': forms.TimeInput(attrs={'class': "form-control", 'type': "time"}),
            'defined_check_out_time': forms.TimeInput(attrs={'class': "form-control", 'type': "time"}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

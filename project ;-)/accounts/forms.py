from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class RegisterForm(UserCreationForm):
    """Form for new user registration"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    company_name = forms.CharField(max_length=200, required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    role = forms.ChoiceField(choices=[('buyer', 'Buyer (Industry)'), ('supplier', 'Supplier (Manufacturer)')])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        # First save the User object
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Then create the UserProfile linked to this user
            role = self.cleaned_data['role']
            UserProfile.objects.create(
                user=user,
                role=role,
                company_name=self.cleaned_data['company_name'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data.get('address', ''),
                # Buyers are auto-approved; suppliers need admin approval
                is_approved=(role == 'buyer'),
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Form for editing profile info"""
    class Meta:
        model = UserProfile
        fields = ['company_name', 'phone', 'address']

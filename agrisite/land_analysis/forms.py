from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import LandParcel, IrrigationSystem, CroppingPattern, LandAnalysis

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your last name'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Choose a username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class LandParcelForm(forms.ModelForm):
    class Meta:
        model = LandParcel
        fields = '__all__'
        widgets = {
            'land_holder': forms.Select(attrs={'class': 'form-control'}),
            'parcel_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter parcel ID (e.g., NP-001)'
            }),
            'total_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Total area in hectares'
            }),
            'cultivated_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Cultivated area in hectares'
            }),
            'soil_type': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Latitude coordinates'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Longitude coordinates'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        total_area = cleaned_data.get('total_area')
        cultivated_area = cleaned_data.get('cultivated_area')
        
        if total_area and cultivated_area:
            if cultivated_area > total_area:
                raise ValidationError({
                    'cultivated_area': 'Cultivated area cannot be greater than total area.'
                })
        return cleaned_data

class IrrigationSystemForm(forms.ModelForm):
    class Meta:
        model = IrrigationSystem
        fields = '__all__'
        widgets = {
            'land_parcel': forms.Select(attrs={'class': 'form-control'}),
            'system_type': forms.Select(attrs={'class': 'form-control'}),
            'water_source': forms.Select(attrs={'class': 'form-control'}),
            'efficiency_rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100',
                'placeholder': 'Efficiency rating (1-100)'
            }),
            'annual_water_usage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Annual water usage in cubic meters'
            }),
            'is_automated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CroppingPatternForm(forms.ModelForm):
    class Meta:
        model = CroppingPattern
        fields = '__all__'
        widgets = {
            'land_parcel': forms.Select(attrs={'class': 'form-control'}),
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Year (e.g., 2024)'
            }),
            'season': forms.Select(attrs={'class': 'form-control'}),
            'area_allocated': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Area allocated in hectares'
            }),
            'yield_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Yield amount in tons'
            }),
            'revenue': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Revenue in local currency'
            }),
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year and (year < 2000 or year > 2030):
            raise ValidationError('Year must be between 2000 and 2030.')
        return year

class LandAnalysisForm(forms.ModelForm):
    class Meta:
        model = LandAnalysis
        fields = '__all__'
        widgets = {
            'land_parcel': forms.Select(attrs={'class': 'form-control'}),
            'analysis_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'soil_health_index': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100',
                'placeholder': 'Soil health index (1-100)'
            }),
            'water_availability': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100',
                'placeholder': 'Water availability percentage (1-100)'
            }),
            'productivity_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100',
                'placeholder': 'Productivity score (1-100)'
            }),
            'recommendations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter recommendations for improvement...'
            }),
        }

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject of your message'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your message...'
        })
    )
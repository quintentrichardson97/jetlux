from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.utils import timezone
from rentals.models import (
    User, SkiBuddy, Appointment, Rental, Photo, Vehicle, Review
)

# --- User Registration Form ---
class CustomUserCreationForm(UserCreationForm):
    is_ski_buddy = forms.BooleanField(required=False, label="Register as a Ski Buddy")
    is_affiliate = forms.BooleanField(required=False, label="Register as an Affiliate")
    business_name = forms.CharField(required=False)
    license_number = forms.CharField(required=False)
    availability = forms.CharField(required=False)
    experience_level = forms.CharField(required=False)
    buddy_bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    rate_per_hour = forms.DecimalField(required=False)
    profile_picture = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2',
            'profile_picture', 'is_ski_buddy', 'is_affiliate',
            'business_name', 'license_number',
            'availability', 'experience_level', 'buddy_bio', 'rate_per_hour'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
            })

# --- Login Form ---
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
            })

# --- User Profile Edit Form ---
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture']

# --- Ski Buddy Profile Edit Form ---
class SkiBuddyForm(forms.ModelForm):
    class Meta:
        model = SkiBuddy
        fields = ['availability', 'experience_level', 'rating']

# --- Booking Form ---
class BookingForm(forms.Form):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
        }),
        label="Start Time"
    )

    duration = forms.FloatField(
        label="Duration (hours)",
        min_value=0.5,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
        })
    )

    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.filter(is_available=True),
        required=False,
        label="Rental Vehicle",
        empty_label="Select a vehicle",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
        })
    )

    buddy = forms.ModelChoiceField(
        queryset=SkiBuddy.objects.all(),
        required=False,
        label="Ski Buddy",
        empty_label="No ski buddy",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
        })
    )

    promo_code = forms.CharField(
        required=False,
        label="Promo Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter promo code if any',
            'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
        })
    )

    end_time = forms.DateTimeField(
        required=False,
        label="End Time",
        widget=forms.DateTimeInput(attrs={
            'readonly': 'readonly',
            'type': 'datetime-local',
            'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
        }),
        disabled=True
    )

    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        buddy = cleaned_data.get('buddy')
        if not vehicle and not buddy:
            raise forms.ValidationError("Please select at least a rental vehicle or a ski buddy.")
        return cleaned_data

def save(self, user):
    data = self.cleaned_data
    end_time = data['start_time'] + timezone.timedelta(hours=data['duration'])
    total = 0
    saved = []

    # Calculate vehicle cost
    if data.get('vehicle'):
        vehicle_cost = float(data['vehicle'].rental_rate) * float(data['duration'])
        total += vehicle_cost
        rental = Rental.objects.create(
            user=user,
            vehicle=data['vehicle'],
            start_time=data['start_time'],
            end_time=end_time,
            promo_code=data.get('promo_code'),
            total_cost=vehicle_cost
        )
        saved.append(rental)

    # Calculate ski buddy cost
    if data.get('buddy'):
        buddy_cost = float(data['buddy'].rate_per_hour) * float(data['duration'])
        total += buddy_cost
        appointment = Appointment.objects.create(
            user=user,
            buddy=data['buddy'],
            start_time=data['start_time'],
            end_time=end_time,
            total_cost=buddy_cost
        )
        saved.append(appointment)

    return saved

# --- Photo Upload (Profile Gallery) ---
class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
            })
        }

# --- Rental Check-in/Check-out Photo Form ---
class RentalPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={
                'placeholder': 'Caption (optional)',
                'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
            }),
        }

# --- Affiliate Vehicle Submission Form ---
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'name', 'vehicle_type', 'description', 'rental_rate', 'image',
            'is_available', 'pickup_location_name', 'pickup_address'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-800 text-white'
            })

# --- User Review Form ---
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 rounded bg-white text-black',
                'placeholder': 'Write your review...'
            }),
        }



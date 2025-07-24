from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

# --- Custom User Model ---
class User(AbstractUser):
    USER_TYPES = [
        ('regular', 'Regular'),
        ('affiliate', 'Affiliate'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='regular')
    bio = models.TextField(blank=True, null=True)
    is_ski_buddy = models.BooleanField(default=False)
    is_affiliate = models.BooleanField(default=False)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    
    profile_picture = models.ImageField(upload_to='user_profiles/', blank=True, null=True)

    def __str__(self):
        return self.username


# --- Ski Buddy Profile ---
class SkiBuddy(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buddy_profile')
    availability = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=50)
    buddy_bio = models.TextField(max_length=1000, default="No bio yet.")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    rate_per_hour = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=50.00,
        help_text="Rate charged per hour in USD"
    )

    def __str__(self):
        return f"{self.user.username} - {self.experience_level} buddy"

# --- Jet Ski Rental ---
class Rental(models.Model):
    # Added back to prevent form error if still referenced
    JET_SKI_CHOICES = [
        ("GTR 230", "GTR 230 - High Performance"),
        ("GTX 300", "GTX 300 - Convenient"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.SET_NULL, null=True)  # Link to the actual vehicle object
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    checkin_complete = models.BooleanField(default=False)
    checkout_complete = models.BooleanField(default=False)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle.name if self.vehicle else 'Unknown Vehicle'} booked by {self.user.username} from {self.start_time} to {self.end_time}"

    def is_ready_for_checkout(self):
        return self.checkin_complete and timezone.now() > self.end_time



# --- Ski Buddy Appointment ---
class Appointment(models.Model):
    buddy = models.ForeignKey(SkiBuddy, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Appointment with {self.buddy.user.username} ({self.start_time} - {self.end_time})"

# --- Photo Uploads (Check-in/Check-out) ---
class Photo(models.Model):
    PHOTO_TYPES = [
        ('checkin', 'Check-In'),
        ('checkout', 'Check-Out'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos')
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    image = models.ImageField(upload_to='user_photos/')
    caption = models.CharField(max_length=255, blank=True)
    photo_type = models.CharField(max_length=10, choices=PHOTO_TYPES, default='checkin')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.photo_type.capitalize()} - {self.caption or 'Photo'}"

# --- Affiliate Vehicles (Jet Skis or Boats) ---
class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('jet_ski', 'Jet Ski'),
        ('boat', 'Boat'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    rental_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=150.00,
        help_text="Rate charged per hour in USD",
    )
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default='jet_ski')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    pickup_location_name = models.CharField(
            max_length=100,
            null=True,
            blank=True,
            help_text="e.g. Dock 7 – Clearwater Beach"
        )
    pickup_address = models.CharField(
            max_length=500,
            null=True,
            blank=True,
            help_text="Full address for GPS/Google Maps"
        )

    # Specs
    horsepower = models.PositiveIntegerField(default=300)
    rider_capacity = models.PositiveIntegerField(default=3)
    top_speed_mph = models.PositiveIntegerField(default=65)
    fuel_capacity_gal = models.DecimalField(max_digits=5, decimal_places=2, default=18.5)
    storage_capacity_gal = models.DecimalField(max_digits=5, decimal_places=2, default=42.5)
    weight_capacity_lb = models.PositiveIntegerField(default=600)

    # Features
    has_brake_reverse = models.BooleanField(default=True, verbose_name="Brake & Reverse")
    has_audio = models.BooleanField(default=False, verbose_name="Premium Sound System")
    has_display = models.BooleanField(default=True, verbose_name="Touch Display")

    def __str__(self):
        return f"{self.name} ({self.get_vehicle_type_display()})"

# --- Waiver Agreement Tracking ---
class WaiverAgreement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted_at = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=10, default='v1.0')

    def __str__(self):
        return f"{self.user.username} agreed on {self.accepted_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
#Reviews
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

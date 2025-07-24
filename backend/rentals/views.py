from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from PIL import Image
import stripe
import json
from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal

from rest_framework import viewsets
from .serializers import (
    UserSerializer,
    SkiBuddySerializer,
    RentalSerializer,
    AppointmentSerializer,
    PhotoSerializer,
    VehicleSerializer,
    WaiverAgreementSerializer,
    ReviewSerializer,
)



from .forms import (
    CustomUserCreationForm, UserForm, SkiBuddyForm,
    BookingForm, PhotoUploadForm, RentalPhotoForm, VehicleForm, ReviewForm
)
from .models import (
    User, SkiBuddy, Rental, Appointment,
    Vehicle, WaiverAgreement, Photo, Review
)

# Home
def home(request):
    affiliates = User.objects.filter(is_affiliate=True, profile_picture__isnull=False)
    reviews = Review.objects.order_by('-created_at')[:3]
    return render(request, 'rentals/home.html', {
        'affiliates': affiliates,
        'reviews': reviews,
    })

# Booking
@login_required
def booking(request):
    if not WaiverAgreement.objects.filter(user=request.user, version='v1.0').exists():
        messages.warning(request, "You must agree to the liability waiver before booking.")
        return redirect('waiver')

    initial_data = {}
    start_date = request.GET.get('start_date')
    start_time = request.GET.get('start_time')
    end_date = request.GET.get('end_date')
    end_time = request.GET.get('end_time')

    if all([start_date, start_time, end_date, end_time]):
        try:
            start_dt = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
            duration_hours = round((end_dt - start_dt).total_seconds() / 3600, 1)
            initial_data['start_time'] = start_dt
            initial_data['duration'] = duration_hours
            initial_data['end_time'] = end_dt
        except Exception as e:
            messages.error(request, "Invalid date or time format.")
            return redirect('booking')

    form = BookingForm(initial=initial_data)
    vehicles = Vehicle.objects.filter(is_available=True)
    buddies = SkiBuddy.objects.select_related('user')

    return render(request, 'rentals/booking.html', {
        "form": form,
        "vehicles": vehicles,
        "buddies": buddies,
    })

# Buddy selection
def buddy_selection(request):
    buddies = SkiBuddy.objects.select_related('user').all()
    return render(request, 'rentals/buddy_selection.html', {'buddies': buddies})

@login_required
def profile(request):
    buddy_profile = getattr(request.user, 'buddy_profile', None)
    if buddy_profile:
        buddy_profile.refresh_from_db()

    vehicle_form = None
    vehicles = None
    if request.user.is_affiliate:
        vehicle_form = VehicleForm(request.POST or None, request.FILES or None)
        vehicles = request.user.vehicles.all()
        if request.method == 'POST' and vehicle_form.is_valid():
            new_vehicle = vehicle_form.save(commit=False)
            new_vehicle.owner = request.user
            new_vehicle.save()
            messages.success(request, "Vehicle added successfully.")
            return redirect('profile')

    photo_types = ["checkin", "checkout"]
    rental_photos = defaultdict(dict)
    for rental in request.user.rental_set.all():
        for ptype in photo_types:
            rental_photos[rental.id][ptype] = rental.photos.filter(photo_type=ptype)

    return render(request, 'rentals/profile.html', {
        'user': request.user,
        'buddy_profile': buddy_profile,
        'vehicle_form': vehicle_form,
        'vehicles': vehicles,
        'photo_types': photo_types,
        'rental_photos': rental_photos,
    })

def reviews(request):
    return render(request, 'rentals/reviews.html')

def buddy_profile_view(request, username):
    User = get_user_model()
    buddy_user = get_object_or_404(User, username=username)
    buddy_profile = getattr(buddy_user, 'buddy_profile', None)
    return render(request, 'rentals/buddy_profile.html', {
        'buddy_user': buddy_user,
        'buddy_profile': buddy_profile
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('is_ski_buddy'):
                user.is_ski_buddy = True
            if form.cleaned_data.get('is_affiliate'):
                user.is_affiliate = True
                user.business_name = form.cleaned_data.get('business_name')
                user.license_number = form.cleaned_data.get('license_number')
            if form.cleaned_data.get('profile_picture'):
                user.profile_picture = form.cleaned_data.get('profile_picture')
            user.save()
            if user.is_ski_buddy:
                SkiBuddy.objects.create(
                    user=user,
                    availability=form.cleaned_data.get('availability', ''),
                    experience_level=form.cleaned_data.get('experience_level', ''),
                    buddy_bio=form.cleaned_data.get('buddy_bio', ''),
                    rate_per_hour=form.cleaned_data.get('rate_per_hour') or 0
                )
            login(request, user)
            messages.success(request, "Registration successful. Please accept the waiver to continue.")
            return redirect('waiver')
    else:
        form = CustomUserCreationForm()
    return render(request, 'rentals/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'rentals/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    user = request.user
    buddy_profile = getattr(user, 'buddy_profile', None)
    user_form = UserForm(request.POST or None, request.FILES or None, instance=user)
    buddy_form = SkiBuddyForm(request.POST or None, request.FILES or None, instance=buddy_profile) if buddy_profile else None

    if request.method == 'POST':
        if user_form.is_valid() and (buddy_form is None or buddy_form.is_valid()):
            user_form.save()
            if buddy_form:
                buddy_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')

    return render(request, 'rentals/edit_profile.html', {
        'user_form': user_form,
        'buddy_form': buddy_form,
        'buddy_profile': buddy_profile
    })

@login_required
def calendar_events(request):
    events = []
    own_only = request.GET.get("own") == "true"
    rentals = Rental.objects.select_related('user')
    if own_only:
        rentals = rentals.filter(user=request.user)
    for rental in rentals:
        events.append({
            "title": "Jet Ski Rental",
            "start": rental.start_time.isoformat(),
            "end": rental.end_time.isoformat(),
            "extendedProps": {
                "jet_ski_type": rental.jet_ski_type,
                "is_mine": rental.user_id == request.user.id
            }
        })
    appointments = Appointment.objects.select_related('buddy__user')
    if own_only:
        appointments = appointments.filter(buddy__user=request.user)
    for appointment in appointments:
        is_mine = hasattr(request.user, 'buddy_profile') and appointment.buddy == request.user.buddy_profile
        events.append({
            "title": f"Appointment with {appointment.buddy.user.username}",
            "start": appointment.start_time.isoformat(),
            "end": appointment.end_time.isoformat(),
            "extendedProps": {
                "is_mine": is_mine
            }
        })
    return JsonResponse(events, safe=False)

@login_required
def user_calendar_events(request):
    events = []
    rentals = Rental.objects.filter(user=request.user)
    for rental in rentals:
        events.append({
            "title": "Your Jet Ski Rental",
            "start": rental.start_time.isoformat(),
            "end": rental.end_time.isoformat(),
        })
    if hasattr(request.user, 'buddy_profile'):
        appointments = Appointment.objects.filter(buddy=request.user.buddy_profile)
        for appointment in appointments:
            events.append({
                "title": "Your Ski Buddy Appointment",
                "start": appointment.start_time.isoformat(),
                "end": appointment.end_time.isoformat(),
            })
    return JsonResponse(events, safe=False)

def jetski_list(request):
    vehicles = Vehicle.objects.filter(is_available=True)
    return render(request, 'rentals/jetski_list.html', {'vehicles': vehicles})

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    rentals = Rental.objects.filter(user=request.user).order_by('-end_time')[:1]
    appointments = Appointment.objects.filter(user=request.user).order_by('-end_time')[:1]

    total = Decimal('0.00')

    # Rental cost
    if rentals:
        rental = rentals[0]
        vehicle = getattr(rental, 'vehicle', None)
        if vehicle and vehicle.rental_rate:
            rental_hours = Decimal((rental.end_time - rental.start_time).total_seconds()) / Decimal(3600)
            total += vehicle.rental_rate * rental_hours

    # Appointment cost
    if appointments:
        appointment = appointments[0]
        buddy = getattr(appointment, 'buddy', None)
        if buddy and buddy.rate_per_hour:
            buddy_hours = Decimal((appointment.end_time - appointment.start_time).total_seconds()) / Decimal(3600)
            total += Decimal(buddy.rate_per_hour) * buddy_hours

    total_amount_cents = int(total * 100)
    total_amount_display = f"{total:.2f}"

    return render(request, "rentals/checkout.html", {
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "PAYPAL_CLIENT_ID": settings.PAYPAL_CLIENT_ID,
        "total_amount_cents": total_amount_cents,
        "total_amount_display": total_amount_display
    })

@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = data.get("amount", 15000)  # fallback to 15000 if none provided

            session = stripe.checkout.Session.create(
                mode="payment",
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": amount,  # now using the dynamic amount
                        "product_data": {"name": "Jet Ski Rental"},
                    },
                    "quantity": 1,
                }],
                success_url=request.build_absolute_uri("/?success=true"),
                cancel_url=request.build_absolute_uri("/?canceled=true"),
            )
            return JsonResponse({"id": session.id})
        except Exception as e:
            return JsonResponse({"error": str(e)})

@csrf_exempt
@require_POST
def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        amount = data.get("amount", 15000)
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method_types=["card"],
        )
        return JsonResponse({"clientSecret": intent.client_secret})
    except Exception as e:
        return JsonResponse({"error": str(e)})

@login_required
def waiver(request):
    user = request.user
    if WaiverAgreement.objects.filter(user=user, version='v1.0').exists():
        return redirect('home')
    if request.method == 'POST':
        WaiverAgreement.objects.create(user=user, version='v1.0')
        messages.success(request, "Thank you for agreeing to the waiver.")
        return redirect('home')
    return render(request, 'rentals/waiver.html', {
        'is_affiliate': user.is_affiliate or user.user_type == 'affiliate',
        'is_ski_buddy': user.is_ski_buddy,
    })

@login_required
def upload_rental_photo(request, rental_id, photo_type):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    photos = rental.photos.filter(photo_type=photo_type)
    if request.method == 'POST':
        form = RentalPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.rental = rental
            photo.photo_type = photo_type
            photo.save()
            return redirect('upload_rental_photo', rental_id=rental.id, photo_type=photo_type)
    else:
        form = RentalPhotoForm()
    return render(request, 'rentals/upload_photo.html', {
        'rental': rental,
        'photo_type': photo_type,
        'form': form,
        'photos': photos,
    })

@login_required
def process_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start_time = cd['start_time']
            duration = cd['duration']
            end_time = start_time + timedelta(hours=duration)

            if cd.get('vehicle'):
                Rental.objects.create(
                    user=request.user,
                    vehicle=cd['vehicle'],
                    start_time=start_time,
                    end_time=end_time,
                    promo_code=cd.get('promo_code', '')
                )

            if cd.get('buddy'):
                Appointment.objects.create(
                    user=request.user,
                    buddy=cd['buddy'],
                    start_time=start_time,
                    end_time=end_time
                )

            return redirect('checkout')
        else:
            messages.error(request, "Please correct the errors below.")
    return redirect('booking')


@login_required
def add_vehicle(request):
    if not request.user.is_affiliate:
        return redirect('profile')

    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            return redirect('profile')
    else:
        form = VehicleForm()

    return render(request, 'rentals/add_vehicle.html', {'form': form})

@login_required
def inventory(request):
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'rentals/inventory.html', {'vehicles': vehicles})

@login_required
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user)
    form = VehicleForm(request.POST or None, request.FILES or None, instance=vehicle)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('inventory')
    return render(request, 'rentals/edit_vehicle.html', {'form': form, 'vehicle': vehicle})

@login_required
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('inventory')
    return redirect('inventory')

@login_required
def write_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'rentals/write_review.html', {'form': form})

def review_list(request):
    reviews = Review.objects.select_related('user').order_by('-created_at')
    return render(request, 'rentals/reviews.html', {'reviews': reviews})

@login_required
def reviews_view(request):
    reviews = Review.objects.select_related('user').all()
    return render(request, 'rentals/reviews.html', {'reviews': reviews})

def get_rate(request, model, pk):
    rate = 0
    if model == "vehicle":
        try:
            rate = Vehicle.objects.get(pk=pk).rental_rate
        except Vehicle.DoesNotExist:
            pass
    elif model == "buddy":
        try:
            rate = SkiBuddy.objects.get(pk=pk).rate_per_hour
        except SkiBuddy.DoesNotExist:
            pass
    return JsonResponse({"rate": float(rate)})

# API viewsets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SkiBuddyViewSet(viewsets.ModelViewSet):
    queryset = SkiBuddy.objects.all()
    serializer_class = SkiBuddySerializer

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class WaiverAgreementViewSet(viewsets.ModelViewSet):
    queryset = WaiverAgreement.objects.all()
    serializer_class = WaiverAgreementSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

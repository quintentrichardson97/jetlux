from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import write_review, review_list

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'ski-buddies', views.SkiBuddyViewSet)
router.register(r'rentals', views.RentalViewSet)
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'photos', views.PhotoViewSet)
router.register(r'vehicles', views.VehicleViewSet)
router.register(r'waivers', views.WaiverAgreementViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('jet-skis/', views.jetski_list, name='jetski_list'),
    path('booking/', views.booking, name='booking'),
    path('buddies/', views.buddy_selection, name='buddy_selection'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('waiver/', views.waiver, name='waiver'),
    path("reviews/", views.review_list, name="reviews"),



    # Auth routes
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Calendar routes
    path('calendar/events/', views.calendar_events, name='calendar_events'),
    path('calendar/user-events/', views.user_calendar_events, name='user_calendar_events'),

    # Checkout routes
    path("checkout/", views.checkout, name="checkout"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("process-booking/", views.process_booking, name="process_booking"),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),

    # Buddy profile route
    path("buddy/<str:username>/", views.buddy_profile_view, name="buddy_profile"),

    # Rental photo upload
    path('rental/<int:rental_id>/upload/<str:photo_type>/', views.upload_rental_photo, name='upload_rental_photo'),

    # Affiliate routes
    path('affiliate/add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('inventory/', views.inventory, name='inventory'),
    path('vehicle/<int:vehicle_id>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicle/<int:vehicle_id>/delete/', views.delete_vehicle, name='delete_vehicle'),

    # Review submission routes
    path('reviews/list/', review_list, name='review_list'),
    path('reviews/write/', write_review, name='write_review'),

    # Rate calculation routes
    path('get_rate/<str:model>/<int:pk>/', views.get_rate, name='get_rate'),
    path('api/', include(router.urls)),
]

# Serve media files during development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from rest_framework import serializers
from .models import User, SkiBuddy, Rental, Appointment, Photo, Vehicle, WaiverAgreement, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SkiBuddySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkiBuddy
        fields = '__all__'


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class WaiverAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaiverAgreement
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

from rest_framework import serializers
from . import models
import razorpay
from donation import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'email', 'phone_number', 'is_verified')


class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Charity
        fields = ('id', 'name', 'description')


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Donation
        fields = ('id', 'charity', 'amount', 'timestamp', 'payment_status')

    def validate_amount(self, amount):
        if amount < 0:
            raise serializers.ValidationError("Donation amount cannot be negative")
        return amount

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        client = razorpay.Client(auth=(settings.RazorPay_KEY_ID, settings.RazorPay_KEY_SECRET))

        data = {"amount": int(validated_data.get('amount', 0)), "currency": "INR"}
        payment = client.order.create(data=data)
        donation = super(DonationSerializer, self).create(validated_data)
        if payment and payment.get('id'):
            donation.payment_status = "COMPLETED"
        else:
            donation.payment_status = "FAILED"
        donation.save()
        return donation

from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import models
from . import serializers
from . import helpers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        user = self.request.user
        return models.User.objects.exclude(id=user.id)

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        phone_number = request.data.get('phone_number')

        # Validate phone_number
        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the user associated with the phone_number
        user = models.User.objects.filter(phone_number=phone_number).first()

        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP
        otp = helpers.generate_otp()
        user.one_time_password = otp
        user.save()

        # Send OTP via phone_number
        helpers.send_otp_to_phone_number(phone_number, otp)

        return Response({'success': 'OTP sent to your phone_number.'}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        # Validate phone_number and OTP
        if not phone_number or not otp:
            return Response({'error': 'Email and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the user associated with the phone_number
        user = models.User.objects.filter(phone_number=phone_number).first()

        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if int(otp) != int(user.one_time_password):
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_401_UNAUTHORIZED)

        user.is_verified = True
        user.save()

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        return Response({
            'success': 'Logged in successfully.',
            'token': str(refresh.access_token)
        }, status=status.HTTP_200_OK)


class CharityViewSet(viewsets.ModelViewSet):
    queryset = models.Charity.objects.all()
    serializer_class = serializers.CharitySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class DonationViewSet(viewsets.ModelViewSet):
    queryset = models.Donation.objects.all()
    serializer_class = serializers.DonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request
        })
        return context

    def get_queryset(self):
        user = self.request.user
        return models.Donation.objects.filter(user=user)

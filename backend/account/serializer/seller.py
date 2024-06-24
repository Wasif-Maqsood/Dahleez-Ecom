# from .models import StripeModel, BillingAddress, OrderModel
from rest_framework import serializers
from django.contrib.auth.models import Seller
from rest_framework_simplejwt.tokens import RefreshToken


class SellerSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Seller
        fields = ["id", "username", "email", "admin"]

    def get_admin(self, obj):
        return obj.is_staff


# creating tokens manually (with user registration we will also create tokens)
class SellerRegisterTokenSerializer(SellerSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Seller
        fields = ["id", "username", "email", "admin", "token"]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


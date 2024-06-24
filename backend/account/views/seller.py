from .models import StripeModel, BillingAddress, OrderModel
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import Seller
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import authentication, permissions
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework_simplejwt.views import TokenObtainPairView # for login page
from django.contrib.auth.hashers import check_password
# from django.shortcuts import get_object_or_404
from .serializers import (
    SellerSerializer, 
    SellerRegisterTokenSerializer, 
    CardsListSerializer, 
    BillingAddressSerializer,
    AllOrdersListSerializer
)





class SellerRegisterView(APIView):
    """To Register the Seller"""

    def post(self, request, format=None):
        data = request.data # holds username and password (in dictionary)
        username = data["username"]
        email = data["email"]

        if username == "" or email == "":
            return Response({"detial": "username or email cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            check_username = Seller.objects.filter(username=username).count()
            check_email =  Seller.objects.filter(email=email).count()

            if check_username:
                message = "A Seller with that username already exist!"
                return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
            if check_email:
                message = "A seller with that email address already exist!"
                return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
            else:
                seller = Seller.objects.create(
                    username=username,
                    email=email,
                    password=make_password(data["password"]),
                )
                serializer = SellerRegisterTokenSerializer(seller, many=False)
                return Response(serializer.data)

# login user (customizing it so that we can see fields like username, email etc as a response 
# from server, otherwise it will only provide access and refresh token)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = SellerRegisterTokenSerializer(self.seller).data

        for k, v in serializer.items():
            data[k] = v
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# list all the cards (of currently logged in user only)
class CardsListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # show stripe cards of only that seller which is equivalent 
        #to currently logged in seller
        stripeCards = StripeModel.objects.filter(seller=request.seller)
        serializer = CardsListSerializer(stripeCards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# get seller details
class SellerAccountDetailsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            seller = seller.objects.get(id=pk)
            serializer = SellerSerializer(seller, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except:
            return Response({"details": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)


# update seller account
class SellerAccountUpdateView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        seller = seller.objects.get(id=pk)
        data = request.data

        if seller:
            if request.seller.id == seller.id:
                seller.username = data["username"]
                seller.email = data["email"]

                if data["password"] != "":
                    seller.password = make_password(data["password"])

                seller.save()
                serializer = SellerSerializer(seller, many=False)
                message = {"details": "Seller Successfully Updated.", "seller": serializer.data}
                return Response(message, status=status.HTTP_200_OK)
            else:
                return Response({"details": "Permission Denied."}, status.status.HTTP_403_FORBIDDEN)
        else:
            return Response({"details": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)


# delete Seller account
class SellerAccountDeleteView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        try:
            seller = Seller.objects.get(id=pk)
            data = request.data

            if request.seller.id == seller.id:
                if check_password(data["password"], seller.password):
                    seller.delete()
                    return Response({"details": "Seller successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"details": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"details": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"details": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)


# get billing address (details of seller address, all addresses)
class SellerAddressesListView(APIView):

    def get(self, request):
        seller = request.seller
        seller_address = BillingAddress.objects.filter(seller=seller)
        serializer = BillingAddressSerializer(seller_address, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


# get specific address only
class SellerAddressDetailsView(APIView):

    def get(self, request, pk):
        seller_address = BillingAddress.objects.get(id=pk)
        serializer = BillingAddressSerializer(seller_address, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


# create billing address
class CreateSellerAddressView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        
        new_address = {
            "name": request.data["name"],
            "seller": request.seller.id,
            "phone_number": request.data["phone_number"],
            "pin_code": request.data["pin_code"],
            "house_no": request.data["house_no"],
            "landmark": request.data["landmark"],
            "city": request.data["city"],
            "state": request.data["state"],
        }

        serializer = BillingAddressSerializer(data=new_address, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# edit billing address
class UpdateSellerAddressView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        data = request.data

        try:
            seller_address = BillingAddress.objects.get(id=pk)

            if request.seller.id == seller_address.seller.id:

                updated_address = {
                    "name": data["name"] if data["name"] else seller_address.name,
                    "seller": request.seller.id,
                    "phone_number": data["phone_number"] if data["phone_number"] else seller_address.phone_number,
                    "pin_code": data["pin_code"] if data["pin_code"] else seller_address.pin_code,
                    "house_no": data["house_no"] if data["house_no"] else seller_address.house_no,
                    "landmark": data["landmark"] if data["landmark"] else seller_address.landmark,
                    "city": data["city"] if data["city"] else seller_address.city,
                    "state": data["state"] if data["state"] else seller_address.state,
                }

                serializer = BillingAddressSerializer(seller_address, data=updated_address)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"details": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"details": "Not found."}, status=status.HTTP_404_NOT_FOUND)


# delete address
class DeleteSellerAddressView(APIView):

    def delete(self, request, pk):
        
        try:
            seller_address = BillingAddress.objects.get(id=pk)

            if request.seller.id == seller_address.seller.id:
                seller_address.delete()
                return Response({"details": "Address successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"details": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"details": "Not found."}, status=status.HTTP_404_NOT_FOUND)

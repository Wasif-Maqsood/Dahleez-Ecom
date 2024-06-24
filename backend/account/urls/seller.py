from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [

    # user
    path('seller_register/', views.SellerRegisterView.as_view(), name="register-page"),
    path('seller_login/', views.MyTokenObtainPairView.as_view(), name="login-page"),
    path('seller/<int:pk>/', views.SellerAccountDetailsView.as_view(), name="seller-details"),
    path('seller_update/<int:pk>/', views.SellerAccountUpdateView.as_view(), name="seller-update"),
    path('seller_delete/<int:pk>/', views.SellerAccountDeleteView.as_view(), name="seller-delete"),
    # Forgot password
     # In urls.py
    #  path('forgot-password/', views.forgot_password, name='forgot_password'),
    # # path('forgot-password/', views.forgot_password, name='forgot-password'),
    # path('password-reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),

    # seller address
    path('all-address-details/', views.SellerAddressesListView.as_view(), name="all-address-details"),
    path('address-details/<int:pk>/', views.SellerAddressDetailsView.as_view(), name="address-details"),
    path('create-address/', views.CreateSellerAddressView.as_view(), name="create-address"),
    path('update-address/<int:pk>/', views.UpdateSellerAddressView.as_view(), name="update-address-details"),
    path('delete-address/<int:pk>/', views.DeleteSellerAddressView.as_view(), name="delete-address"),

    # order
    path('all-orders-list/', views.OrdersListView.as_view(), name="all-orders-list"),
    path('change-order-status/<int:pk>/', views.ChangeOrderStatus.as_view(), name="change-order-status"),

    # stripe
    path('stripe-cards/', views.CardsListView.as_view(), name="stripe-cards-list-page"),
]
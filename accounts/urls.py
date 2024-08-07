from django.urls import path
from .views import UserListCreateView, UserRetriveUpdateDestroyView, PasswordResetView, PasswordResetConfirmView, RegisterView, LoginView

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
]

from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, ImageView, ColorizedImageView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    

    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('products/', ImageView.as_view()),
    # path('colorize-image/<int:pk>/', ColorizeImageView.as_view(), name='colorize_image'),
    path('colorized-image/', ColorizedImageView.as_view(), name='colorized_image'),
]
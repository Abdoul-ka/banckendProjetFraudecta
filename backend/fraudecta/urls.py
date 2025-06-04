from django.urls import path
from .views import PredictDiplomeView, ocr_verification
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('predict/', PredictDiplomeView.as_view(), name='predict-diplome'),
    path('ocr/', ocr_verification),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),

]

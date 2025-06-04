from django.urls import path
from .views import PredictDiplomeView, ocr_verification

urlpatterns = [
    path('predict/', PredictDiplomeView.as_view(), name='predict-diplome'),
    path('ocr/', ocr_verification),
]

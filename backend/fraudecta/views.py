from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from users.serializers import UserRegisterSerializer
from users.models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import os

from .prediction import predict_image
from .ocr_utils import extract_id
from .models import Diplome  


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if CustomUser.objects.filter(email=email).exists():
                return Response({'error': 'Cet email est déjà utilisé.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({'message': 'Utilisateur créé avec succès'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Vue API pour la prédiction du diplôme
class PredictDiplomeView(APIView):
    def post(self, request):
        file = request.FILES.get('image')
        if not file:
            return Response({"error": "Aucune image fournie."}, status=status.HTTP_400_BAD_REQUEST)

        # Sauvegarde temporaire de l'image
        image_path = os.path.join(settings.BASE_DIR, 'temp_image.jpg')
        with open(image_path, 'wb+') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        # Prétraitement de l'image
        img = image.load_img(image_path, target_size=(224, 224))  # Adapter selon le modèle
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Chargement du modèle
        model_path = os.path.join(settings.BASE_DIR, 'model/modele_diplome.h5')
        model = load_model(model_path)

        # Prédiction
        prediction = model.predict(img_array)[0][0]
        confidence = float(prediction)
        classification = "faux" if confidence > 0.5 else "vrai"
        confiance = 1 - confidence if classification == "vrai" else confidence

        return Response({
            "classification": classification,
            "confiance": round(confiance, 2)
        })


# Vue API pour l'OCR et la vérification de l'ID étudiant
@api_view(['POST'])
def ocr_verification(request):
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({'error': 'Aucune image reçue.'}, status=status.HTTP_400_BAD_REQUEST)

    id_extrait = extract_id(image_file)
    if not id_extrait:
        return Response({'error': 'ID introuvable.'}, status=status.HTTP_404_NOT_FOUND)

    existe = Diplome.objects.filter(id_etudiant=id_extrait).exists()

    return Response({
        'id': id_extrait,
        'trouve': existe
    })

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['email'] = user.email
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
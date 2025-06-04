from django.db import models

# Create your models here.
from django.db import models

class Diplome(models.Model):
    id_etudiant = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    filiere = models.CharField(max_length=100, null=True, blank=True)
    date_obtention = models.DateField(null=True, blank=True)
    universite = models.CharField(max_length=150, null=True, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'diplome'  # très important !
        managed = False       # Django ne gère pas la création/modification


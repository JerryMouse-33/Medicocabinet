from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TypeConsultation(models.Model):
    id= models.BigAutoField(primary_key=True)
    nom_consult= models.CharField(max_length=100)
    description = models.TextField(max_length=1000)




class Patient(models.Model):
    id= models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CNI = models.CharField(max_length=32)

class Medecin(models.Model):
    id= models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CNI = models.CharField(max_length=32)

class ConsultationS(models.Model):
    id= models.BigAutoField(primary_key=True)
    type_consultation = models.ForeignKey(TypeConsultation, on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    medecin = models.ForeignKey(Medecin, on_delete=models.PROTECT)
    venu_quand = models.DateTimeField(auto_now_add=True)
    parti_quand = models.DateTimeField(on_delete=models.PROTECT)
    notes = models.TextField(max_length=200)


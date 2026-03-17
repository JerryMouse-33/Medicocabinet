from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django.db.models.functions import TruncDate
from django.utils import timezone

# Create your models here.

class TypeConsultation(models.Model):
    id = models.AutoField(primary_key=True)
    nom_consult = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.nom_consult}"


class Patient(models.Model):
    id= models.BigAutoField(primary_key=True)
    nom= models.CharField(max_length=100,null=True, blank=True)
    prenom= models.CharField(max_length=100,null=True, blank=True)
    CNI = models.CharField(max_length=32, unique=True)
    medecin = models.ForeignKey('Medecin', on_delete=models.PROTECT, null=True, blank=True)

    id_patient = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.id_patient is None:
            last = Patient.objects.order_by('-id_patient').first()
            
            if last and last.id_patient:
                self.id_patient = last.id_patient + 1
            else:
                self.id_patient = 1

        super().save(*args, **kwargs)
    def __str__(self):
        return f"Patient {self.id_patient} - {self.nom} {self.prenom} "

class Medecin(models.Model):
    id= models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medecin')
    nom= models.CharField(max_length=100,null=True, blank=True)
    prenom= models.CharField(max_length=100,null=True, blank=True)
    CNI = models.CharField(max_length=32, unique=True)
    role = models.ForeignKey(TypeConsultation, on_delete=models.PROTECT,null=True,blank=True)
    def __str__(self):
        role_name = self.role.nom_consult if self.role else "Aucun rôle"
        return f"Dr. {self.nom} {self.prenom} - Rôle: {role_name}"
    
    
class Consultation(models.Model):
    id = models.BigAutoField(primary_key=True)
    type_consultation = models.ForeignKey(TypeConsultation, on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    medecin = models.ForeignKey(Medecin, on_delete=models.PROTECT)
    venu_quand = models.DateTimeField(auto_now_add=True)  
    parti_quand = models.DateTimeField()
    notes = models.TextField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'venu_quand'],
                name='unique_patient_per_day'
            )
        ]
        ordering = ['-venu_quand']
    # def most_frequent_service(request):
    #   service = (
    #     Consultation.objects
    #     .values("type_consultation")
    #     .annotate(total=Count("service"))
    #     .order_by("-total")
    #     .first()
    #   )
    #   return JsonResponse(service)
    
    def __str__(self):
        patient_name = f"Patient - {self.patient.nom} {self.patient.prenom}" if self.patient else "Patient inconnu"
        med_name = f"Dr. {self.medecin.nom} {self.medecin.prenom}" if self.medecin else "Médecin inconnu"
        return f"Consultation {self.id} - {patient_name} / {med_name} - {self.venu_quand.strftime('%Y-%m-%d %H:%M')}"
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

class TypeConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeConsultation
        fields = ['id', 'nom_consult','description',]
    

class PatientSerializer(serializers.ModelSerializer):
    medecin_nom=serializers.CharField(source="medecin.nom", read_only=True)
    medecin_prenom= serializers.CharField(source="medecin.prenom", read_only=True)

    class Meta:
        model = Patient
        fields = [ 'nom', 'prenom','CNI', 'medecin','medecin_nom','medecin_prenom']


class MedecinSerializer(serializers.ModelSerializer):

    role_nom = serializers.CharField(source="role.nom_consult", read_only=True)

    class Meta:
        model = Medecin
        fields = ['user','nom', 'prenom', 'role', 'role_nom']
        
class ConsultationSerializer(serializers.ModelSerializer):
    type_consult= serializers.CharField(source="type_consultation.nom_consult", read_only= True)
    medecin_nom=serializers.CharField(source="medecin.nom", read_only=True)
    medecin_prenom= serializers.CharField(source="medecin.prenom", read_only=True)
    patient_nom=serializers.CharField(source="patient.nom", read_only=True)
    patient_prenom= serializers.CharField(source="patient.prenom", read_only=True)
    class Meta:
        model = Consultation
        fields = ['id', 'type_consultation','type_consult', 'patient','patient_nom','patient_prenom','medecin','medecin_nom','medecin_prenom', 'venu_quand', 'parti_quand',]



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['is_staff'] = self.user.is_staff
        return data
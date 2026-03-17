from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny, BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView

from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response


class TypeConsultationViewSet(viewsets.ModelViewSet):
    queryset = TypeConsultation.objects.all()
    serializer_class = TypeConsultationSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [AllowAny]
    filterset_fields = {'nom_consult': ['exact', 'icontains']}


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = {'nom': ['exact', 'icontains'],
                        'prenom': ['exact', 'icontains'],
                        'medecin': ['exact']}

class MedecinViewSet(viewsets.ModelViewSet):
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = {'nom': ['exact', 'icontains'],
                        'prenom': ['exact', 'icontains'],
                        'role': ['exact']}

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filterset_fields = {'patient': ['gte', 'lte'],
                        'medecin': ['gte', 'lte'],
                        'type_consultation': ['gte', 'lte'],
                        'venu_quand': ['gte', 'lte']}
   
    @action(detail=False, methods=['get'])
    def most_frequent_service(self, request):
        service = (
            Consultation.objects
            .filter(medecin__role__isnull=False)
            .values('medecin__role__nom_consult')
            .annotate(total=Count('id'))
            .order_by('-total')
            .first()
        )

        return Response({
            "service": service["medecin__role__nom_consult"] if service else None,
            "total": service["total"] if service else 0
              })
    
class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
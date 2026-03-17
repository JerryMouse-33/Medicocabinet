from django.urls import path,include 
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'medecins', MedecinViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'types-consultation', TypeConsultationViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [

    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/medecins/', MedecinViewSet.as_view({
        'get': 'get'
    }), name='Medecin_ViewSet'),
]


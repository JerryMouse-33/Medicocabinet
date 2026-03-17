from django.contrib import admin

# Register your models here.

from .models import *
from django.contrib.admin import ModelAdmin
admin.site.site_header = "MedoCabinet " 
admin.site.site_title = "MedoCabinet " 
admin.site.index_title = "Administration MedoCabinet " 
from .models import ( TypeConsultation, Patient, Medecin, Consultation, ) 

class TypeConsultationAdmin(ModelAdmin):
    list_display = ('nom_consult', 'description')
    search_fields = ('nom_consult',)
admin.site.register(TypeConsultation,TypeConsultationAdmin)


class PatientAdmin(ModelAdmin): 
    list_display = ('id_patient', 'nom', 'prenom', 'CNI', 'medecin') 
    search_fields = ('nom', 'prenom', 'CNI') 
    autocomplete_fields = ('medecin',) 
    def save_model(self, request, obj, form, change): 
        if not change: 
            obj.user = request.user 
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        try:
            med = request.user.medecin
            return qs.filter(medecin=med)
        except:
            return qs.none()
admin.site.register(Patient, PatientAdmin)


class MedecinAdmin(ModelAdmin):
    list_display = ('id', 'user','nom', 'prenom', 'role')
    search_fields = ('user__username', 'nom', 'prenom', 'role')
    autocomplete_fields = ('user',)
    readonly_fields = ('id',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        try:
            med = request.user.medecin
            return qs.filter(id=med.id)
        except:
            return qs.none()

admin.site.register(Medecin, MedecinAdmin)


class ConsultationAdmin(ModelAdmin):
    list_display = ('id', 'type_consultation', 'patient', 'medecin', 'venu_quand', 'parti_quand')
    list_filter = ('type_consultation', 'medecin', 'venu_quand')
    search_fields = (
        'patient__user__username',
        'patient__user__first_name',
        'patient__user__last_name',
        'medecin__user__username',
        'medecin__medecin__nom',
        'medecin__medecin__prenom',
    )

    autocomplete_fields = ('type_consultation', 'patient', 'medecin')
    readonly_fields = ('venu_quand',)
    date_hierarchy = 'venu_quand'
    ordering = ('-venu_quand',)

    def save_model(self, request, obj, form, change):
        if not change and hasattr(request.user, 'medecin'):
            obj.medecin = request.user.medecin
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if hasattr(request.user, 'medecin'):
            return qs.filter(medecin=request.user.medecin)

        return qs.none()
admin.site.register(Consultation, ConsultationAdmin)
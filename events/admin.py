from django.contrib import admin
from django.shortcuts import get_object_or_404


from .models import Evento, Invitado, Integrante, Parroquia, Mesa


class IntegranteInline(admin.TabularInline):
    model = Integrante


class InvitadoInline(admin.TabularInline):
    model = Invitado


@admin.register(Evento)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date")


@admin.register(Invitado)
class InvitadoAdmin(admin.ModelAdmin):
    list_display = ("integrate", "get_integrate_birth_date", "table", "is_present")
    list_filter = ("table", "is_present", "integrate__place")
    list_editable = ("is_present", "table")
    search_fields = (
        "integrate__name",
        "integrate__surname",
        "integrate__place__name",
    )

    def get_integrate_birth_date(self, obj):
        return obj.integrate.birth_date

    get_integrate_birth_date.short_description = "Integrate Birth Date"


@admin.register(Integrante)
class IntegranteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "surname",
        "birth_date",
        "cellphone",
        "place",
        "is_attending",
    )
    list_filter = ("place", "is_attending")
    search_fields = (
        "name",
        "surname",
        "place__name",
    )


@admin.register(Parroquia)
class ParroquiaAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name", "address")
    inlines = [IntegranteInline]


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ("name", "event")
    list_filter = ("event",)
    inlines = [InvitadoInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "event":
            num_events = Evento.objects.count()
            if num_events == 1:
                kwargs["initial"] = get_object_or_404(Evento)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

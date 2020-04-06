from django.contrib import admin, messages
from .models import Student, Project, Coach, MembershipInProject


# Register your models here.

class MembershipInline(admin.TabularInline):
    model = MembershipInProject
    extra = 0


class FiltreDuree(admin.SimpleListFilter):
    title = ('Duree')
    parameter_name = 'duree'

    def lookups(self, request, model_admin):
        return (
                ('1 mois', ("moins d'un mois")),
                ('3 mois', ("plus qu'un mois"))
        )

    def queryset(self, request, queryset):
        if self.value() == '1 mois':
            return queryset.filter(duree_du_projet__lte=30)
        elif self.value() == '3 mois':
            return queryset.filter(duree_du_projet__lte=30, duree_du_projet__gte=90)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('nom_du_projet', 'duree_du_projet', 'description','est_valide', 'createur', 'total_allocated_by_members')
    actions = ['set_to_valid','set_to_no_valid']
    inlines = (MembershipInline,)

    fieldsets = (
        ('Etat', {'fields': ('est_valide',)}),
        ('A propos', {
            'fields': ('nom_du_projet', ('createur', 'superviseur'), 'besoins', 'description',),
        }),
        ('Durées', {
            'fields': (('duree_du_projet', 'temps_alloue_par_le_createur'),)
        }),
    )

    list_filter = ('createur',FiltreDuree)
    search_fields = ['nom_du_projet', 'createur__nom']
    #actions_on_bottom = True
    #actions_on_top = False
    list_per_page = 2

    def set_to_valid(self, request, queryset):
        queryset.update(est_valide=True)
    set_to_valid.short_description = "Valider"

    def set_to_no_valid(self, request, queryset):
        no_valid = queryset.filter(est_valide=False)
        if no_valid.count() > 0:
            messages.error(request, "%s project est_valid=false"%no_valid.count())
        else:
            rows_update = queryset.update(est_valid = False)
            if rows_update == 1:
                message = "1 project was updated "
            else:
                message = "%s projects were updated ="%rows_update
            self.message_user(request,message="%s successfully marked as not valid" %message)


class CoachAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email')
    fields = (('nom', 'prenom'), 'email')
    ordering = ['prenom']


class StudentAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email')
    fields = (('nom', 'prenom'), 'email')
    ordering = ['prenom']


admin.site.register(Coach, CoachAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Project, ProjectAdmin)

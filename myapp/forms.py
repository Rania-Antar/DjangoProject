from django import forms

from .models import Project

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('nom_du_projet',
                  'duree_du_projet',
                  'temps_alloue_par_le_createur',
                  'besoins',
                  'description',
                  'createur',
                  )


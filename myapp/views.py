from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.generic import DetailView

from myapp.forms import AddProjectForm
from myapp.models import Project, Student, Coach


def index(request):
    return render(request, 'index.html')


def list_projects(request):
    """projects_list = Project.objects.all()
    output = ', '.join([p.nom_du_projet for p in projects_list])
    return HttpResponse(output)"""
    #return HttpResponse("You're looking list projects")

    projects_list = Project.objects.all()
    return render(request, 'projects.html', {'projects_list': projects_list})


def project_details(request, pId):
    project = get_object_or_404(Project, pk=pId)
    return render(request, 'project_details.html', {'project': project})

    #return HttpResponse("You're looking to the project having ID: {}".format(pId))


def add_project(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = AddProjectForm()
            return render(request, 'add_project.html', {'form': form})
        if request.method == "POST":
            form = AddProjectForm(request.POST)
            if form.is_valid():
                postProject = form.save(commit=False)
                postProject.save()
                return HttpResponseRedirect(reverse('liste'))
            else:
                return render(request, 'add_project.html',
                              {'msg_erreur': 'Erreur lors de la création du projet',
                               'form':form})
    else:
        return HttpResponseForbidden()


def edit_project(request, pId):
    """
    Methode permettant à un étudiant de éditer son propre projet
    :param request:
    :param p_id:
    :return:
    """
    if request.user.is_authenticated:
        project = get_object_or_404(Project, pk=pId)
        genForm = AddProjectForm(instance=project)
        return render(request, 'edit_project.html', {'form': genForm, 'p_id': pId})
    else:
        return HttpResponseForbidden()


def submit_edition_project(request, p_id):
    """
    Méthode pemettant de saouvegarder les modifications apportés par un étudiant
    sur son propre projet
    :param request:
    :param p_id:
    :return:
    """
    project = get_object_or_404(Project, pk=p_id)
    if request.method == 'POST':
        genForm = AddProjectForm(request.POST or None, instance=project)
        if genForm.is_valid():
            genForm.save()
            return HttpResponseRedirect(reverse('liste'))
        else:
            return HttpResponseRedirect(reverse('liste'))
    else:
        return HttpResponseRedirect(reverse('liste'))


class ProjectsListView(generic.ListView):
    """
    Usage de classe générique ListView pour lister les projets
    Redéfinition de la méthode get_queryset afin de restreindre l'accées aux données
    aux utilisateurs authentifiées (Cas de Coach et d'étudiant
    """
    model = Project
    template_name = 'projects.html'
    context_object_name = 'projects_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return Project.objects.all()
            else:
                return Project.objects.filter(est_valide=True)
        else:
            return HttpResponseForbidden()


class ProjectDetailView(DetailView):
    """
    Usage de la classe générique DetailView pour afficher les détails relatifs à un projet
    Redéfinition de la méthode get_context_data afin d'envoyer une donnée supplémentaire
    dans le contexte qui permet de différencier côté template entre un coach et un étudiant
    """
    model = Project
    template_name = 'project_details.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = super(ProjectDetailView, self).get_object()
        context['project'] = project

        if not self.request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if self.request.user.is_superuser or (Coach.objects.filter(user=self.request.user).count() > 0):
                context['is_coach'] = True
            else:
                context['is_coach'] = False
        return context


def authenticate_user(request):
    """
    Méthode d'authentification d'un utiulisateur à partir du formulaire
    :param request:
    :return:
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))


def logout_view(request):
    """
    Méthode de déconnexion de l'utilisateur
    :param request:
    :return:
    """
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def join_project(request, project_id):
    """
    Méthode permettant à un étudiant de joindre un projet
    :param request:
    :param project_id:
    :return:
    """
    project = get_object_or_404(Project, pk=project_id)
    my_student = Student.objects.filter(user=request.user).first()
    if my_student not in project.get_related_members():
        project.membershipinproject_set.create(projet=project.pk ,
                                               etudiant = my_student,
                                               time_allocated_by_member=1)
    return HttpResponseRedirect(reverse('liste'))


def validate_project(request, project_id):
    """
    Méthode permettant à un coach ou un superutilisateur de valider un projet
    :param request:
    :param project_id:
    :return:
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        project = get_object_or_404(Project, pk=project_id)
        project.est_valide = True
        project.save()
        return HttpResponseRedirect(reverse('liste'))



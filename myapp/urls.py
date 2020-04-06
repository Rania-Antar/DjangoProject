from django.urls import re_path, path

from myapp import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    #path('projects/', views.projects, name='liste'),
    path('projects/<int:pId>/', views.project_details, name='details'),
    path('projects_liste/',views.list_projects,name='projet_liste'),
    #re_path(r'^projects/(?P<pId>[0-9]+)/edit/$', views.edit_project, name='edit')
    path('projects/<int:pId>/edit/', views.edit_project, name='edit'),
    path('projects/create/', views.add_project, name='create'),

]

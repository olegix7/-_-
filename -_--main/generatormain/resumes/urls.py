from django.urls import path
from . import views

urlpatterns = [
    # Catalog
    path('templates/', views.template_catalog, name='template_catalog'),

    # Admin
    path('admin/', views.admin_resume_list, name='admin_resume_list'),

    # Resume CRUD
    path('', views.resume_list, name='resume_list'),
    path('create/', views.resume_create, name='resume_create'),
    path('<int:pk>/', views.resume_detail, name='resume_detail'),
    path('<int:pk>/edit/', views.resume_edit, name='resume_edit'),
    path('<int:pk>/delete/', views.resume_delete, name='resume_delete'),
    path('<int:pk>/clone/', views.resume_clone, name='resume_clone'),

    # Export
    path('<int:pk>/export/pdf/', views.resume_export_pdf, name='resume_export_pdf'),
    path('<int:pk>/export/docx/', views.resume_export_docx, name='resume_export_docx'),

    # Sections
    path('<int:resume_pk>/sections/add/', views.section_add, name='section_add'),
    path('<int:resume_pk>/sections/<int:section_pk>/edit/', views.section_edit, name='section_edit'),
    path('<int:resume_pk>/sections/<int:section_pk>/delete/', views.section_delete, name='section_delete'),
]

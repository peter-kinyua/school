from django.urls import path

from . import views

urlpatterns = [
    path('student-login-page/', views.student_login_page, name='student_login_page'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('login-page/', views.teacher_login_page, name='teacher_login_page'),
    path('dashboard/add-student/', views.teacher_add_student, name='teacher_add_student'),
    path('dashboard/upload-paper/', views.teacher_upload_paper, name='teacher_upload_paper'),
    path('dashboard/add-zoom-link/', views.teacher_add_zoom_link, name='teacher_add_zoom_link'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('upload-paper/', views.upload_paper, name='upload_paper'),
    path('add-zoom-link/', views.add_zoom_link, name='add_zoom_link'),
    path('papers/', views.list_papers, name='list_papers'),
    path('papers/<int:paper_id>/edit/', views.edit_paper, name='edit_paper'),
    path('papers/<int:paper_id>/delete/', views.delete_paper, name='delete_paper'),
    path('zoom-links/', views.list_zoom_links, name='list_zoom_links'),
    path('zoom-links/<int:link_id>/edit/', views.edit_zoom_link, name='edit_zoom_link'),
    path('zoom-links/<int:link_id>/delete/', views.delete_zoom_link, name='delete_zoom_link'),
    path('login/', views.teacher_login, name='teacher_login'),
    path('student-login/', views.student_login, name='student_login'),
    path('add-student/', views.add_student, name='add_student'),
    path('teachers/', views.list_teachers, name='list_teachers'),
]

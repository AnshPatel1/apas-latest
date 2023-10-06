from django.contrib import admin
from django.urls import path, include
from Staff import views

urlpatterns = [
    path('staff/', views.StaffViewSet.dashboard, name='dashboard_staff'),
    # path('staff/profile/', views.StaffViewSet.profile, name='dashboard_staff'),
    path('staff/entry/', views.StaffViewSet.staff_show, name='staff_show'),
    path('staff/status/', views.StaffViewSet.status, name='staff_status'),
    path('staff/entry/save/', views.StaffViewSet.staff_entry, name='staff_entry'),
    path('mooc/upload/', views.StaffViewSet.upload_mooc, name='upload_mooc'),
    path('staff/certifications/upload/', views.StaffViewSet.upload_certifications, name='upload_certs'),
    path('staff/certifications/delete/', views.StaffViewSet.delete_certification, name='delete_cert'),
    path('staff/result/', views.StaffViewSet.staff_result, name='staff_result'),
]

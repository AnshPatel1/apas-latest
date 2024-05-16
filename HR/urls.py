from django.urls import path
from HR.views import *

urlpatterns = [
    path('', home, name='hr-home'),
    path('staff/', staff, name='hr-staff'),
    path('staff/track/', TrackGrade.staff, name='hr-staff-track'),
    path('staff/mooc/', TrackGrade.staff_mooc, name='hr-staff-mooc'),
    path('foet/track/', TrackGrade.faculty_foet, name='hr-foet-track'),
    path('fols/track/', TrackGrade.faculty_fols, name='hr-fols-track'),
    path('som/track/', TrackGrade.faculty_foem, name='hr-foem-track'),
    path('math/track/', TrackGrade.faculty_math, name='hr-math-track'),
    path('science/track/', TrackGrade.faculty_science, name='hr-science-track'),
    path('tally/', hr_data_tally, name='hr-tally'),
    path('detail/<str:goalsheet>/', inclusion_detail, name='hr-inclusion'),
    path('detail/<str:goalsheet>/<str:status>/', detail_status, name='hr-inclusion-filtered'),
]
from django.urls import path
from Faculty.FacultySoEM.views import *

urlpatterns = [
    path('', FacultyViewSet.dashboard, name='sot_faculty-home'),
    path('verify/', FacultyViewSet.verify_data, name='verify-data'),
    path('teaching/', FacultyViewSet.teaching_entry, name='teaching-entry'),
    path('research/', FacultyViewSet.research_entry, name='research-entry'),
    path('phd-guidance/', FacultyViewSet.phd_guidance_entry, name='phd-guidance-entry'),
    path('project/', FacultyViewSet.project_entry, name='project-entry'),
    path('dissertation/', FacultyViewSet.dissertation_entry, name='dissertation-entry'),
    path('patent/', FacultyViewSet.patent_entry, name='patent-entry'),
    path('award/', FacultyViewSet.award_entry, name='award-entry'),
    path('consultancy/', FacultyViewSet.consultancy_entry, name='consultancy-entry'),
    path('academia-collab/', FacultyViewSet.academia_collab_entry, name='academia-collab-entry'),
    path('arranging-conference/', FacultyViewSet.arranging_conference_entry, name='arranging-conference-entry'),
    path('mentorship/', FacultyViewSet.mentorship_entry, name='mentorship-entry'),
    path('attending-conference/', FacultyViewSet.attending_conference_entry, name='attending-conference-entry'),
    path('community-development/', FacultyViewSet.community_development_entry, name='community-development-entry'),
    path('extra-curricular/', FacultyViewSet.extra_curricular_entry, name='extra-curricular-entry'),
    path('additional/', FacultyViewSet.additional_entry, name='additional-entry'),
    path('review/', FacultyViewSet.review, name='review-entry'),
    path('submit/', FacultyViewSet.submit, name='submit-entry'),
    path('summary/', FacultyViewSet.summary, name='download-entry'),
    path('result/', FacultyViewSet.result, name='result-entry'),
]

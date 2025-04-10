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
    path('api/patent/finalize/', APIVerifyViews.finalize_verified_patent, name='hr-api-patent-finalize'),
    path('api/books/finalize/', APIVerifyViews.finalize_verified_books, name='hr-api-books-finalize'),
    path('api/paper/finalize/', APIVerifyViews.finalize_verified_paper, name='hr-api-paper-finalize'),
    path('detail/<str:goalsheet>/', inclusion_detail, name='hr-inclusion'),
    path('detail/<str:goalsheet>/<str:status>/', detail_status, name='hr-inclusion-filtered'),
    path('api/patent/<str:school>/', APIVerifyViews.patent, name='hr-api-patent'),
    path('api/patent/<str:school>/delete/<str:internal_id>/', APIVerifyViews.patent_reverse, name='hr-api-patent-reverse'),
    path('api/paper/<str:school>/', APIVerifyViews.paper, name='hr-api-paper'),
    path('api/paper/<str:school>/delete/<str:internal_id>/', APIVerifyViews.paper_reverse, name='hr-api-paper-reverse'),
    path('api/books/<str:school>/', APIVerifyViews.books, name='hr-api-books'),
    path('api/books/<str:school>/delete/<str:internal_id>/', APIVerifyViews.book_reverse, name='hr-api-book-reverse'),
    path('api/patent/', APIVerifyViews.patent_home, name='hr-api-patent-home'),
    path('api/paper/', APIVerifyViews.paper_home, name='hr-api-paper-home'),
    path('api/books/', APIVerifyViews.books_home, name='hr-api-books-home'),
]
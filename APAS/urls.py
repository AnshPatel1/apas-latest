"""APAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from MediaServe.views import serve_media
from Account.views import forgot_password, password_reset
from MediaServe import views as media_views
from apps.home.views import page_404, manintenance
from .views import FacultyRedirectViewSet

urlpatterns = [
    path('not-found/', page_404),
    re_path('^media/', serve_media, name="serve_media"),
    path('admin/', admin.site.urls),
    path('reset-password/', password_reset),
    path('forgot-password/', forgot_password, name="forgot_password"),
    path("", include("apps.authentication.urls")),  # Auth routes - login / register
    # path("maintenance/", manintenance),
    path('appraisee/', include('Staff.urls')),
    path('faculty/', FacultyRedirectViewSet.redirect, name='faculty-root'),
    path('faculty/sot/', include('Faculty.FacultyFOET.urls'), name='faculty-foet-root'),
    path('faculty/sls/', include('Faculty.FacultySLS.urls'), name='faculty-fols-root'),
    path('faculty/soem/', include('Faculty.FacultySoEM.urls'), name='faculty-soem-root'),
    path('faculty/maths/', include('Faculty.FacultyMaths.urls'), name='faculty-maths-root'),
    path('faculty/science/', include('Faculty.FacultyScience.urls'), name='faculty-science-root'),
    path('ro1/', include('RO1.urls')),
    path('ro2/', include('RO2.urls')),
    path('hr/', include('HR.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns.append(path("", include("apps.home.urls")))

handler404 = 'apps.home.views.page_404'

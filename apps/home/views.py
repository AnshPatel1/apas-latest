# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from MasterConfiguration.models import *
from APAS.views import FacultyHelperFunctions


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    if FacultyHelperFunctions.get_inclusion(request.user) in ['SOT', 'SLS', 'SPM', 'MATH', 'SCIENCE', 'STAFF']:
        context['appraisal_allowed'] = True
    user = request.user
    name = user.first_name
    context['name'] = name
    # context['staff_list'] = StaffAppraisalCycleInclusion.objects
    html_template = loader.get_template('html/home/main-home.html')

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('html/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def page_404(request, exception):
    context = {}
    html_template = loader.get_template('home/page-404.html')
    return HttpResponse(html_template.render(context, request))


def manintenance(request):
    context = {
                'error_code': "Maintenance Ongoing",
                "error_message": "This site is under maintenance. Please visit after 11 PM, May 10 2023. Sorry for the inconvinience"
            }
    return render(request, "html/error_pages/pages-error.html", context)

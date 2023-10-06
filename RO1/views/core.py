from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from Faculty.FacultyFOET.models import *
from Faculty.FacultySLS.models import *
from Faculty.FacultySoEM.models import *
from Faculty.FacultyScience.models import *
from Faculty.FacultyMaths.models import *
from Account.models import User
from RO1.views import HelperFunctions
from Staff.models import StaffAppraisalFile
from MasterConfiguration.models import *
import datetime as dt


class RO1MainView:
    @login_required(login_url='/login/')
    def dashboard(request):
        if request.method == 'GET':
            if request.user.is_ro1:
                context = {}
                context['pagename'] = 'ro1-dashboard'
                # try:
                #     file = StaffAppraisalFile.objects.filter(file_level=)
                #     context['file']
                # except StaffAppraisalFile.DoesNotExist:
                #     pass
                context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
                try:
                    context['file'] = StaffAppraisalFile.objects.get(user=request.user)
                except StaffAppraisalFile.DoesNotExist:
                    config = StaffAppraisalCycleConfiguration.objects.filter(is_active=True).first()
                    context['file'] = StaffAppraisalFile.create(config.year, request.user)

                    context['file'].save()

                # context['files'] = StaffAppraisalFile.objects.filter(file_level='RO1')
                return render(request, 'html/r1/ro1-dashboard.html', context)
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)

    # @login_required(login_url='/login/')
    # def profile(request):
    #     if request.method == 'GET':
    #         if request.user.is_ro1:
    #             context = {}
    #             context['pagename'] = 'ro1-profile'
    #             return render(request, 'html/r1/ro1-profile.html', context)
    #         else:
    #             context = {
    #                 'error_code': "Unauthorized Error",
    #                 "error_message": "You are not authorized to view this page."
    #             }
    #             return render(request, "html/error_pages/pages-error.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def review_main(request):
        if request.method == 'GET':
            if request.user.is_ro1:
                context = {}
                context['pagename'] = 'ro1-review-main'
                context['files'] = []
                included_appraisees = StaffAppraisalCycleInclusion.objects.first().appraisee.all()
                for i in StaffAppraisalFile.objects.all():
                    if i.user.ro1_id == request.user and i.user in included_appraisees:
                        context['files'].append(i)

                # get all users where ro1_id = request.user
                users = User.objects.filter(ro1_id=request.user)
                context['pending_files'] = []
                context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()

                for i in users:
                    try:
                        if i.roles == 'stf':
                            file = StaffAppraisalFile.objects.get(user=i)
                    except StaffAppraisalFile.DoesNotExist:
                        context['pending_files'].append(i)
                context['departments'] = []
                # for i in User.objects.all():
                #     if i.department not in context['departments']:
                #         context['departments'].append(i.department)

                for f in context['files']:
                    i = f.user
                    if i.department not in context['departments']:
                        context['departments'].append(i.department)
                context['designations'] = []
                for f in context['files']:
                    i = f.user
                    if i.designation not in context['designations']:
                        context['designations'].append(i.designation)
                for i in context['pending_files']:
                    if i.designation not in context['designations']:
                        context['designations'].append(i.designation)
                return render(request, 'html/r1/r1-review-main.html', context)
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def review_faculty(request):
        if request.user.is_ro1:
            context = {}
            context['pagename'] = 'ro1-review-faculty'
            user_foet = list(SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.filter(
                ro1_id=request.user))
            user_fols = list(SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.filter(
                ro1_id=request.user))
            user_foem = list(SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.filter(
                ro1_id=request.user))
            user_math = list(MathFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.filter(
                ro1_id=request.user))
            user_science = list(
                ScienceFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.filter(
                    ro1_id=request.user))
            included_appraisees = user_foet + user_fols + user_foem + user_math + user_science
            included_appraisees = set(included_appraisees)

            sot_files = []
            sls_files = []
            som_files = []
            math_files = []
            science_files = []
            context['cycles'] = {
                'foet': RO1MainView.get_cycle('foet'),
                'sls': RO1MainView.get_cycle('sls'),
                'som': RO1MainView.get_cycle('som'),
                'math': RO1MainView.get_cycle('math'),
                'science': RO1MainView.get_cycle('science'),
            }
            for i in list(FOETAssistantProfOnContractAppraisalFile.objects.all()) \
                     + list(FOETAssistantProfAppraisalFile.objects.all()) \
                     + list(FOETAssociateProfAppraisalFile.objects.all()) \
                     + list(FOETProfAppraisalFile.objects.all()):
                if i.user.ro1_id == request.user:
                    sot_files.append(i)

            for i in list(FOLSAssistantProfOnContractAppraisalFile.objects.all()) \
                     + list(FOLSAssistantProfAppraisalFile.objects.all()) \
                     + list(FOLSAssociateProfAppraisalFile.objects.all()) \
                     + list(FOLSProfAppraisalFile.objects.all()):
                if i.user.ro1_id == request.user:
                    sls_files.append(i)

            for i in list(FOEMAssistantProfOnContractAppraisalFile.objects.all()) \
                     + list(FOEMAssistantProfAppraisalFile.objects.all()) \
                     + list(FOEMAssociateProfAppraisalFile.objects.all()) \
                     + list(FOEMProfAppraisalFile.objects.all()):
                if i.user.ro1_id == request.user:
                    som_files.append(i)

            for i in list(MathAssistantProfOnContractAppraisalFile.objects.all()) \
                     + list(MathAssistantProfAppraisalFile.objects.all()) \
                     + list(MathAssociateProfAppraisalFile.objects.all()) \
                     + list(MathProfAppraisalFile.objects.all()):
                if i.user.ro1_id == request.user:
                    math_files.append(i)
            for i in list(ScienceAssistantProfOnContractAppraisalFile.objects.all()) \
                     + list(ScienceAssistantProfAppraisalFile.objects.all()) \
                     + list(ScienceAssociateProfAppraisalFile.objects.all()) \
                     + list(ScienceProfAppraisalFile.objects.all()):
                if i.user.ro1_id == request.user:
                    science_files.append(i)

            context['pending_files'] = list(included_appraisees - set(
                [file.user for file in sot_files + sls_files + som_files + math_files + science_files]))
            context['sot_files'] = sot_files
            context['sls_files'] = sls_files
            context['som_files'] = som_files
            context['math_files'] = math_files
            context['science_files'] = science_files

            context['designations'] = []
            context['departments'] = []
            for i in included_appraisees:
                if i.designation.upper() not in context['designations']:
                    context['designations'].append(i.designation.upper())

                if i.department.upper() not in context['departments']:
                    context['departments'].append(i.designation.upper())

            return render(request, 'html/r1/r1-review-faculty.html', context)
        else:
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

    @staticmethod
    def get_cycle(school):
        try:
            if school == "foet":
                config = FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first()
            elif school == "sls":
                config = SLSFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first()
            elif school == "som":
                config = SOEMFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first()
            elif school == "math":
                config = MathFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first()
            elif school == "science":
                config = ScienceFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first()
            return {'name': config.get_cycle(), 'config': config, 'current_date': CurrentDate.objects.first().date}
        except SOEMFacultyAppraisalCycleConfiguration.DoesNotExist:
            return HttpResponse("Problem while fetching cycles")

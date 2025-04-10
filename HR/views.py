from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Faculty.FacultyFOET.models.appraisal_files import *
import Faculty.FacultyFOET.models.appraisal_files.calculation_engine as foet_calc
from Faculty.FacultySLS.models.appraisal_files import *
import Faculty.FacultySLS.models.appraisal_files.calculation_engine as sls_calc
from Faculty.FacultySoEM.models.appraisal_files import *
import Faculty.FacultySoEM.models.appraisal_files.calculation_engine as som_calc
from Faculty.FacultyMaths.models.appraisal_files import *
import Faculty.FacultyMaths.models.appraisal_files.calculation_engine as maths_calc
from Faculty.FacultyScience.models.appraisal_files import *
import Faculty.FacultyScience.models.appraisal_files.calculation_engine as science_calc
from RO1.views import HelperFunctions
from Staff.models import *
from MasterConfiguration.models import *
import BulkUpload.BulkUploadFoEM.models as bulk_som
import BulkUpload.BulkUploadFoLS.models as bulk_sls
import BulkUpload.BulkUploadFoET.models as bulk_foet
import BulkUpload.BulkUploadMaths.models as bulk_math
import BulkUpload.BulkUploadScience.models as bulk_science
import json
import requests
import requests_cache
from xml.etree.ElementTree import fromstring
import hashlib
from HR.models import *


# Create your views here.
@login_required(login_url='/login/')
def staff(request):
    context = {}
    context['pagename'] = 'staff_review'
    if request.user.is_hr:
        context = {}
        context['pagename'] = 'staff_review'
        context['files'] = []
        # for i in StaffAppraisalFile.objects.all():
        # if i.user.ro2_id == request.user:
        # context['files'].append(i)
        context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
        users = list(StaffAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        context['pending_files'] = []
        for i in users:
            try:
                file = StaffAppraisalFile.objects.get(user=i)
                context['files'].append(file)
            except StaffAppraisalFile.DoesNotExist:
                context['pending_files'].append(i)
        context['departments'] = []
        for f in context['files']:
            i = f.user
            if i.department not in context['departments']:
                context['departments'].append(i.department)
        for i in context['pending_files']:
            if i.department.upper() not in context['departments']:
                context['departments'].append(i.department.upper())

        designations = []
        for i in context['files']:
            if i.user.designation.upper() not in designations:
                designations.append(i.user.designation.upper())
        for i in context['pending_files']:
            if i.designation.upper() not in designations:
                designations.append(i.designation.upper())

        context['designations'] = designations
        context['selection'] = 'staff'

        return render(request, 'html/hr/staff_review.html', context)
    else:
        context = {
            'error_code': "Unauthorized Error",
            "error_message": "You are not authorized to view this page."
        }
        return render(request, 'html/error_pages/pages-error.html', context)


@login_required(login_url='/login/')
def staff_grade(request):
    if request.user.is_hr:
        context = {}
        context['pagename'] = 'staff-track'
        context['files'] = []
        # for i in StaffAppraisalFile.objects.all():
        # if i.user.ro2_id == request.user:
        # context['files'].append(i)
        context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
        users = StaffAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
        context['pending_files'] = []
        context['files'] = StaffAppraisalFile.objects.filter(user__in=users, file_level__in=['RO2', 'HR'])
        context['count'] = {
            'r1': {
                'o': context['files'].filter(grade_received_ro1='Outstanding').count(),
                'g': context['files'].filter(grade_received_ro1='Good').count(),
                'a': context['files'].filter(grade_received_ro1='Average').count(),
                'b': context['files'].filter(grade_received_ro1='Below Average').count(),
            },
            'r2': {
                'o': context['files'].filter(grade_received_ro2='Outstanding', file_level='HR').count(),
                'g': context['files'].filter(grade_received_ro2='Good', file_level='HR').count(),
                'a': context['files'].filter(grade_received_ro2='Average', file_level='HR').count(),
                'b': context['files'].filter(grade_received_ro2='Below Average', file_level='HR').count(),
            },
        }
        context['departments'] = []
        for f in context['files']:
            i = f.user
            if i.department not in context['departments']:
                context['departments'].append(i.department)
        for i in context['pending_files']:
            if i.department.upper() not in context['departments']:
                context['departments'].append(i.department.upper())

        designations = []
        for i in context['files']:
            if i.user.designation.upper() not in designations:
                designations.append(i.user.designation.upper())
        for i in context['pending_files']:
            if i.designation.upper() not in designations:
                designations.append(i.designation.upper())

        context['designations'] = designations
        context['selection'] = 'staff'

        return render(request, 'html/hr/staff-grade-view.html', context)
    else:
        context = {
            'error_code': "Unauthorized Error",
            "error_message": "You are not authorized to view this page."
        }
        return render(request, 'html/error_pages/pages-error.html', context)


@login_required(login_url='/login/')
def home(request):
    if not request.user.is_hr:
        context = {
            'error_code': "Unauthorized Error",
            "error_message": "You are not authorized to view this page."
        }
        return render(request, 'html/error_pages/pages-error.html', context)
    context = {'pagename': 'hr_home',
               'staff_config': StaffAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'staff_inclusion': StaffAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all(),
               'foet_config': FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'foet_inclusion': SOTFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'sls_config': SLSFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'sls_inclusion': SLSFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'som_config': SOEMFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'som_inclusion': SPMFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'math_config': MathFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'math_inclusion': MathFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'science_config': ScienceFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'science_inclusion': ScienceFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'count': get_count(),
               }
    return render(request, 'html/hr/home.html', context)
    # return render(request, 'html/hr/home.html', context)


class TrackGrade:
    @staticmethod
    @login_required(login_url='/login/')
    def staff(request):
        if request.user.is_hr:
            context = {}
            context['pagename'] = 'staff-track'
            context['files'] = []
            # for i in StaffAppraisalFile.objects.all():
            # if i.user.ro2_id == request.user:
            # context['files'].append(i)
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            users = StaffAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
            context['pending_files'] = []
            context['files'] = StaffAppraisalFile.objects.filter(user__in=users, file_level__in=['RO2', 'HR'])
            context['count'] = {
                'r1': {
                    'o': context['files'].filter(grade_received_ro1='Outstanding').count(),
                    'g': context['files'].filter(grade_received_ro1='Good').count(),
                    'a': context['files'].filter(grade_received_ro1='Average').count(),
                    'b': context['files'].filter(grade_received_ro1='Below Average').count(),
                },
                'r2': {
                    'o': context['files'].filter(grade_received_ro2='Outstanding', file_level='HR').count(),
                    'g': context['files'].filter(grade_received_ro2='Good', file_level='HR').count(),
                    'a': context['files'].filter(grade_received_ro2='Average', file_level='HR').count(),
                    'b': context['files'].filter(grade_received_ro2='Below Average', file_level='HR').count(),
                },
            }
            context['departments'] = []
            for f in context['files']:
                i = f.user
                if i.department not in context['departments']:
                    context['departments'].append(i.department)
            for i in context['pending_files']:
                if i.department.upper() not in context['departments']:
                    context['departments'].append(i.department.upper())

            designations = []
            for i in context['files']:
                if i.user.designation.upper() not in designations:
                    designations.append(i.user.designation.upper())
            for i in context['pending_files']:
                if i.designation.upper() not in designations:
                    designations.append(i.designation.upper())

            context['designations'] = designations
            context['selection'] = 'staff'

            return render(request, 'html/hr/staff-grade-view.html', context)
        else:
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, 'html/error_pages/pages-error.html', context)

    @staticmethod
    @login_required(login_url='/login/')
    def staff_mooc(request):
        if request.user.is_hr:
            context = {}
            context['pagename'] = 'staff-mooc'
            context['files'] = []
            # for i in StaffAppraisalFile.objects.all():
            # if i.user.ro2_id == request.user:
            # context['files'].append(i)
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            users = StaffAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
            context['pending_files'] = []
            context['files'] = StaffAppraisalFile.objects.filter(user__in=users, file_level__in=['RO2', 'HR'])
            context['count'] = {
                'r1': {
                    'o': context['files'].filter(grade_received_ro1='Outstanding').count(),
                    'g': context['files'].filter(grade_received_ro1='Good').count(),
                    'a': context['files'].filter(grade_received_ro1='Average').count(),
                    'b': context['files'].filter(grade_received_ro1='Below Average').count(),
                },
                'r2': {
                    'o': context['files'].filter(grade_received_ro2='Outstanding', file_level='HR').count(),
                    'g': context['files'].filter(grade_received_ro2='Good', file_level='HR').count(),
                    'a': context['files'].filter(grade_received_ro2='Average', file_level='HR').count(),
                    'b': context['files'].filter(grade_received_ro2='Below Average', file_level='HR').count(),
                },
            }
            context['departments'] = []
            for f in context['files']:
                i = f.user
                if i.department not in context['departments']:
                    context['departments'].append(i.department)
            for i in context['pending_files']:
                if i.department.upper() not in context['departments']:
                    context['departments'].append(i.department.upper())

            designations = []
            for i in context['files']:
                if i.user.designation.upper() not in designations:
                    designations.append(i.user.designation.upper())
            for i in context['pending_files']:
                if i.designation.upper() not in designations:
                    designations.append(i.designation.upper())

            context['designations'] = designations
            context['selection'] = 'staff'

            return render(request, 'html/hr/staff-mooc-view.html', context)
        else:
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, 'html/error_pages/pages-error.html', context)

    @staticmethod
    @login_required(login_url='/login/')
    def faculty_foet(request):
        if not request.user.is_hr:
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
        valid_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(
            user__in=SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
        ).union(
            FOETAssistantProfAppraisalFile.objects.filter(
                user__in=SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        ).union(
            FOETAssociateProfAppraisalFile.objects.filter(
                user__in=SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        ).union(
            FOETProfAppraisalFile.objects.filter(
                user__in=SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        )
        r1_graded_files = [file for file in valid_files if file.file_level == "RO2"]
        r2_graded_files = [file for file in valid_files if file.file_level == "HR"]

        context = {
            'pagename': 'foet-track',
            'staff_config': SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first(),
            'staff_inclusion': SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all(),
            'r1': {
                'outstanding': [file for file in r1_graded_files if file.r1_grade == 'OUTSTANDING'],
                'good': [file for file in r1_graded_files if file.r1_grade == 'GOOD'],
                'average': [file for file in r1_graded_files if file.r1_grade == 'AVERAGE'],
                'below_average': [file for file in r1_graded_files if file.r1_grade == 'BELOW AVERAGE'],
            },
            'r2': {
                'outstanding': [file for file in r2_graded_files if file.r2_grade == 'OUTSTANDING'],
                'good': [file for file in r2_graded_files if file.r2_grade == 'GOOD'],
                'average': [file for file in r2_graded_files if file.r2_grade == 'AVERAGE'],
                'below_average': [file for file in r2_graded_files if file.r2_grade == 'BELOW AVERAGE'],
            }
        }
        context['count'] = {
            'r1': {
                'o': len(context['r1']['outstanding']),
                'g': len(context['r1']['good']),
                'a': len(context['r1']['average']),
                'b': len(context['r1']['below_average']),
            },

            'r2': {
                'o': len(context['r2']['outstanding']),
                'g': len(context['r2']['good']),
                'a': len(context['r2']['average']),
                'b': len(context['r2']['below_average']),
            }
        }
        graders = []
        for i in r2_graded_files:
            c = foet_calc.CalculationEngineR2(i)
            graders.append({
                'additional_r2': c.calculateAdditionalMarks(),
                'part_b_r2': c.calculatePartB()
            })

        context['files'] = zip(r2_graded_files, graders)
        context['graders'] = graders

        return render(request, 'html/hr/faculty-grade-view.html', context)

    @staticmethod
    @login_required(login_url='/login/')
    def faculty_fols(request):
        if not request.user.is_hr:
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
        valid_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(
            user__in=SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
        ).union(
            FOLSAssistantProfAppraisalFile.objects.filter(
                user__in=SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        ).union(
            FOLSAssociateProfAppraisalFile.objects.filter(
                user__in=SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        ).union(
            FOLSProfAppraisalFile.objects.filter(
                user__in=SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        )
        r1_graded_files = [file for file in valid_files if file.file_level == "RO2"]
        r2_graded_files = [file for file in valid_files if file.file_level == "HR"]

        context = {
            'pagename': 'fols-track',
            'staff_config': SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first(),
            'staff_inclusion': SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all(),
            'r1': {
                'outstanding': [file for file in r1_graded_files if file.r1_grade == 'OUTSTANDING'],
                'good': [file for file in r1_graded_files if file.r1_grade == 'GOOD'],
                'average': [file for file in r1_graded_files if file.r1_grade == 'AVERAGE'],
                'below_average': [file for file in r1_graded_files if file.r1_grade == 'BELOW AVERAGE'],
            },
            'r2': {
                'outstanding': [file for file in r2_graded_files if file.r2_grade == 'OUTSTANDING'],
                'good': [file for file in r2_graded_files if file.r2_grade == 'GOOD'],
                'average': [file for file in r2_graded_files if file.r2_grade == 'AVERAGE'],
                'below_average': [file for file in r2_graded_files if file.r2_grade == 'BELOW AVERAGE'],
            }
        }
        context['count'] = {
            'r1': {
                'o': len(context['r1']['outstanding']),
                'g': len(context['r1']['good']),
                'a': len(context['r1']['average']),
                'b': len(context['r1']['below_average']),
            },

            'r2': {
                'o': len(context['r2']['outstanding']),
                'g': len(context['r2']['good']),
                'a': len(context['r2']['average']),
                'b': len(context['r2']['below_average']),
            }
        }
        graders = []
        for i in r2_graded_files:
            c = sls_calc.CalculationEngineR2(i)
            graders.append({
                'additional_r2': c.calculateAdditionalMarks(),
                'part_b_r2': c.calculatePartB()
            })

        context['files'] = zip(r2_graded_files, graders)
        context['graders'] = graders

        return render(request, 'html/hr/faculty-grade-view.html', context)

    @staticmethod
    @login_required(login_url='/login/')
    def faculty_foem(request):
        if not request.user.is_hr:
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
        valid_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(
            user__in=SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
        ).union(
            FOEMAssistantProfAppraisalFile.objects.filter(
                user__in=SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        ).union(
            FOEMAssociateProfAppraisalFile.objects.filter(
                user__in=SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        ).union(
            FOEMProfAppraisalFile.objects.filter(
                user__in=SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        )
        r1_graded_files = [file for file in valid_files if file.file_level == "RO2"]
        r2_graded_files = [file for file in valid_files if file.file_level == "HR"]

        context = {
            'pagename': 'foem-track',
            'staff_config': SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first(),
            'staff_inclusion': SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all(),
            'r1': {
                'outstanding': [file for file in r1_graded_files if file.r1_grade == 'OUTSTANDING'],
                'good': [file for file in r1_graded_files if file.r1_grade == 'GOOD'],
                'average': [file for file in r1_graded_files if file.r1_grade == 'AVERAGE'],
                'below_average': [file for file in r1_graded_files if file.r1_grade == 'BELOW AVERAGE'],
            },
            'r2': {
                'outstanding': [file for file in r2_graded_files if file.r2_grade == 'OUTSTANDING'],
                'good': [file for file in r2_graded_files if file.r2_grade == 'GOOD'],
                'average': [file for file in r2_graded_files if file.r2_grade == 'AVERAGE'],
                'below_average': [file for file in r2_graded_files if file.r2_grade == 'BELOW AVERAGE'],
            }
        }
        context['count'] = {
            'r1': {
                'o': len(context['r1']['outstanding']),
                'g': len(context['r1']['good']),
                'a': len(context['r1']['average']),
                'b': len(context['r1']['below_average']),
            },

            'r2': {
                'o': len(context['r2']['outstanding']),
                'g': len(context['r2']['good']),
                'a': len(context['r2']['average']),
                'b': len(context['r2']['below_average']),
            }
        }
        graders = []
        for i in r2_graded_files:
            c = som_calc.CalculationEngineR2(i)
            graders.append({
                'additional_r2': c.calculateAdditionalMarks(),
                'part_b_r2': c.calculatePartB()
            })

        context['files'] = zip(r2_graded_files, graders)
        context['graders'] = graders

        return render(request, 'html/hr/faculty-grade-view.html', context)

    @staticmethod
    @login_required(login_url='/login/')
    def faculty_math(request):
        if not request.user.is_hr:
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
        valid_files = MathAssistantProfOnContractAppraisalFile.objects.filter(
            user__in=MathFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
        ).union(
            MathAssistantProfAppraisalFile.objects.filter(
                user__in=MathFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        ).union(
            MathAssociateProfAppraisalFile.objects.filter(
                user__in=MathFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        ).union(
            MathProfAppraisalFile.objects.filter(
                user__in=MathFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        )
        r1_graded_files = [file for file in valid_files if file.file_level == "RO2"]
        r2_graded_files = [file for file in valid_files if file.file_level == "HR"]

        context = {
            'pagename': 'math-track',
            'staff_config': MathFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first(),
            'staff_inclusion': MathFacultyAppraisalCycleInclusion.objects.filter(
                is_active=True).first().appraisee.all(),
            'r1': {
                'outstanding': [file for file in r1_graded_files if file.r1_grade == 'OUTSTANDING'],
                'good': [file for file in r1_graded_files if file.r1_grade == 'GOOD'],
                'average': [file for file in r1_graded_files if file.r1_grade == 'AVERAGE'],
                'below_average': [file for file in r1_graded_files if file.r1_grade == 'BELOW AVERAGE'],
            },
            'r2': {
                'outstanding': [file for file in r2_graded_files if file.r2_grade == 'OUTSTANDING'],
                'good': [file for file in r2_graded_files if file.r2_grade == 'GOOD'],
                'average': [file for file in r2_graded_files if file.r2_grade == 'AVERAGE'],
                'below_average': [file for file in r2_graded_files if file.r2_grade == 'BELOW AVERAGE'],
            }
        }
        context['count'] = {
            'r1': {
                'o': len(context['r1']['outstanding']),
                'g': len(context['r1']['good']),
                'a': len(context['r1']['average']),
                'b': len(context['r1']['below_average']),
            },

            'r2': {
                'o': len(context['r2']['outstanding']),
                'g': len(context['r2']['good']),
                'a': len(context['r2']['average']),
                'b': len(context['r2']['below_average']),
            }
        }
        graders = []
        for i in r2_graded_files:
            c = maths_calc.CalculationEngineR2(i)
            graders.append({
                'additional_r2': c.calculateAdditionalMarks(),
                'part_b_r2': c.calculatePartB()
            })

        context['files'] = zip(r2_graded_files, graders)
        context['graders'] = graders

        return render(request, 'html/hr/faculty-grade-view.html', context)

    @staticmethod
    @login_required(login_url='/login/')
    def faculty_science(request):
        if not request.user.is_hr:
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
        valid_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(
            user__in=ScienceFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
        ).union(
            ScienceAssistantProfAppraisalFile.objects.filter(
                user__in=ScienceFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        ).union(
            ScienceAssociateProfAppraisalFile.objects.filter(
                user__in=ScienceFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        ).union(
            ScienceProfAppraisalFile.objects.filter(
                user__in=ScienceFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())
        )
        r1_graded_files = [file for file in valid_files if file.file_level == "RO2"]
        r2_graded_files = [file for file in valid_files if file.file_level == "HR"]

        context = {
            'pagename': 'science-track',
            'staff_config': ScienceFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first(),
            'staff_inclusion': ScienceFacultyAppraisalCycleInclusion.objects.filter(
                is_active=True).first().appraisee.all(),
            'r1': {
                'outstanding': [file for file in r1_graded_files if file.r1_grade == 'OUTSTANDING'],
                'good': [file for file in r1_graded_files if file.r1_grade == 'GOOD'],
                'average': [file for file in r1_graded_files if file.r1_grade == 'AVERAGE'],
                'below_average': [file for file in r1_graded_files if file.r1_grade == 'BELOW AVERAGE'],
            },
            'r2': {
                'outstanding': [file for file in r2_graded_files if file.r2_grade == 'OUTSTANDING'],
                'good': [file for file in r2_graded_files if file.r2_grade == 'GOOD'],
                'average': [file for file in r2_graded_files if file.r2_grade == 'AVERAGE'],
                'below_average': [file for file in r2_graded_files if file.r2_grade == 'BELOW AVERAGE'],
            }
        }
        context['count'] = {
            'r1': {
                'o': len(context['r1']['outstanding']),
                'g': len(context['r1']['good']),
                'a': len(context['r1']['average']),
                'b': len(context['r1']['below_average']),
            },

            'r2': {
                'o': len(context['r2']['outstanding']),
                'g': len(context['r2']['good']),
                'a': len(context['r2']['average']),
                'b': len(context['r2']['below_average']),
            }
        }
        graders = []
        for i in r2_graded_files:
            c = science_calc.CalculationEngineR2(i)
            graders.append({
                'additional_r2': c.calculateAdditionalMarks(),
                'part_b_r2': c.calculatePartB()
            })

        context['files'] = zip(r2_graded_files, graders)
        context['graders'] = graders

        return render(request, 'html/hr/faculty-grade-view.html', context)


@login_required(login_url='/login/')
def inclusion_detail(request, goalsheet):
    if not request.user.is_hr:
        context = {
            'error_code': "Unauthorized Error",
            "error_message": "You are not authorized to view this page."
        }
        return render(request, 'html/error_pages/pages-error.html', context)
    context = {'pagename': 'hr_home',
               'staff_config': StaffAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'staff_inclusion': StaffAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all(),
               'foet_config': FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'foet_inclusion': SOTFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'sls_config': SLSFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'sls_inclusion': SLSFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'som_config': SOEMFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'som_inclusion': SPMFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'math_config': MathFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'math_inclusion': MathFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'science_config': ScienceFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'science_inclusion': ScienceFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'goalsheet': goalsheet,
               }
    if goalsheet == 'staff':
        context['title'] = f'Staff Appraisal {context["staff_config"].year}'
        context['users'] = context['staff_inclusion']
    elif goalsheet == 'foet':
        context['title'] = f'FOET Faculty Appraisal {context["foet_config"].year}'
        context['users'] = context['foet_inclusion']
    elif goalsheet == 'fols':
        context['title'] = f'FOLS Faculty Appraisal {context["sls_config"].year}'
        context['users'] = context['sls_inclusion']
    elif goalsheet == 'som':
        context['title'] = f'SOM Faculty Appraisal {context["som_config"].year}'
        context['users'] = context['som_inclusion']
    elif goalsheet == 'math':
        context['title'] = f'Math Faculty Appraisal {context["math_config"].year}'
        context['users'] = context['math_inclusion']
    elif goalsheet == 'science':
        context['title'] = f'Science Faculty Appraisal {context["science_config"].year}'
        context['users'] = context['science_inclusion']
    else:
        context = {
            'error_code': "404: Page not found 😔",
            "error_message": "The page you are trying to access does not exist."
        }
        return render(request, 'html/error_pages/pages-error.html', context)

    return render(request, 'html/hr/inclusion_details.html', context)
    # return render(request, 'html/hr/home.html', context)


@login_required(login_url='/login/')
def detail_status(request, goalsheet, status):
    if not request.user.is_hr:
        context = {
            'error_code': "Unauthorized Error",
            "error_message": "You are not authorized to view this page."
        }
        return render(request, 'html/error_pages/pages-error.html', context)
    context = {'pagename': 'hr_home',
               'staff_config': StaffAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'staff_inclusion': StaffAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all(),
               'foet_config': FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'foet_inclusion': SOTFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'sls_config': SLSFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'sls_inclusion': SLSFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'som_config': SOEMFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'som_inclusion': SPMFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'math_config': MathFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'math_inclusion': MathFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'science_config': ScienceFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'science_inclusion': ScienceFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'goalsheet': goalsheet,
               }
    if goalsheet == 'staff':
        context['title'] = f'Staff Appraisal {context["staff_config"].year}'
        if status == 'login-pending':
            files = set([file.user for file in StaffAppraisalFile.objects.filter(year=context["staff_config"].year)])
            context['users'] = set(context['staff_inclusion']) - files
        elif status == 'unverified':
            context['users'] = set([file.user for file in
                                    StaffAppraisalFile.objects.filter(year=context["staff_config"].year,
                                                                      is_all_parameters_approved=False)]).intersection(
                context['staff_inclusion'])
        elif status == 'verified':
            context['users'] = set([file.user for file in
                                    StaffAppraisalFile.objects.filter(year=context["staff_config"].year,
                                                                      is_all_parameters_approved=True)]
                                   ).intersection(context['staff_inclusion'])
        elif status == 'self-appraisal-pending':
            context['users'] = set(
                [file.user for file in
                 StaffAppraisalFile.objects.filter(year=context["staff_config"].year, file_level="APPRAISEE",
                                                   is_all_parameters_approved=True)]
            ).intersection(context['staff_inclusion'])
        elif status == 'self-appraisal-submitted' or status == 'r1-pending':
            context['users'] = set(
                [file.user for file in
                 StaffAppraisalFile.objects.filter(year=context["staff_config"].year, file_level="RO1",
                                                   is_all_parameters_approved=True)]
            ).intersection(context['staff_inclusion'])
        elif status == 'r2-pending' or status == 'r1-done':
            context['users'] = set(
                [file.user for file in
                 StaffAppraisalFile.objects.filter(year=context["staff_config"].year, file_level="RO2")]
            ).intersection(context['staff_inclusion'])
        elif status == 'r2-done' or status == 'r1-done':
            context['users'] = set(
                [file.user for file in
                 StaffAppraisalFile.objects.filter(year=context["staff_config"].year, file_level="HR")]
            ).intersection(context['staff_inclusion'])
        else:
            context = {
                'error_code': "404: Page not found 😔",
                "error_message": "The page you are trying to access does not exist."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
    elif goalsheet == 'foet':
        context['title'] = f'FOET Faculty Appraisal {context["foet_config"].year}'

        if status == 'login-pending':
            foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(
                year=context["foet_config"].year).union(
                FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year).union(
                    FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year).union(
                        FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year))))
            files = set([file.user for file in foet_files])
            context['users'] = set(context['foet_inclusion']) - files
        elif status == 'unverified':
            foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                                 has_verified_data=False).union(
                FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                              has_verified_data=False).union(
                    FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                  has_verified_data=False).union(
                        FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                             has_verified_data=False))))
            context['users'] = set([file.user for file in foet_files]).intersection(
                context['foet_inclusion'])
        elif status == 'verified' or status == 'self-appraisal-pending':
            foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                                 has_verified_data=True,
                                                                                 file_level="APPRAISEE").union(
                FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year, has_verified_data=True,
                                                              file_level="APPRAISEE").union(
                    FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                  has_verified_data=True, file_level="APPRAISEE").union(
                        FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year, has_verified_data=True,
                                                             file_level="APPRAISEE"))))
            context['users'] = set([file.user for file in foet_files]
                                   ).intersection(context['foet_inclusion'])
        elif status == 'self-appraisal-submitted' or status == 'r1-pending':
            foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                                 file_level="RO1").union(
                FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="RO1").union(
                    FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                  file_level="RO1").union(
                        FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="RO1"))))
            context['users'] = set(
                [file.user for file in foet_files]
            ).intersection(context['foet_inclusion'])
        elif status == 'r2-pending' or status == 'r1-done':
            foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                                 file_level="RO2").union(
                FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="RO2").union(
                    FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                  file_level="RO2").union(
                        FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="RO2"))))
            context['users'] = set(
                [file.user for file in foet_files]
            ).intersection(context['foet_inclusion'])
        elif status == 'r2-done' or status == 'r1-done':
            foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                                 file_level="HR").union(
                FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="HR").union(
                    FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                  file_level="HR").union(
                        FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="HR"))))
            context['users'] = set(
                [file.user for file in foet_files]
            ).intersection(context['foet_inclusion'])
        else:
            context = {
                'error_code': "404: Page not found 😔",
                "error_message": "The page you are trying to access does not exist."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
    elif goalsheet == 'fols':
        context['title'] = f'FOLS Faculty Appraisal {context["sls_config"].year}'
        if status == 'login-pending':
            sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year).union(
                FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year).union(
                    FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year).union(
                        FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year))))
            files = set([file.user for file in sls_files])
            context['users'] = set(context['sls_inclusion']) - files
        elif status == 'unverified':
            sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                                has_verified_data=False).union(
                FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                              has_verified_data=False).union(
                    FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                  has_verified_data=False).union(
                        FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                             has_verified_data=False))))
            context['users'] = set([file.user for file in sls_files]).intersection(
                context['sls_inclusion'])
        elif status == 'verified' or status == 'self-appraisal-pending':
            sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                                has_verified_data=True,
                                                                                file_level="APPRAISEE").union(
                FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year, has_verified_data=True,
                                                              file_level="APPRAISEE").union(
                    FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                  has_verified_data=True, file_level="APPRAISEE").union(
                        FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year, has_verified_data=True,
                                                             file_level="APPRAISEE"))))
            print(sls_files)
            context['users'] = set([file.user for file in sls_files]
                                   ).intersection(context['sls_inclusion'])
        elif status == 'self-appraisal-submitted' or status == 'r1-pending':
            sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                                file_level="RO1").union(
                FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="RO1").union(
                    FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                  file_level="RO1").union(
                        FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="RO1"))))
            print(sls_files)
            context['users'] = set(
                [file.user for file in sls_files]
            ).intersection(context['sls_inclusion'])
        elif status == 'r2-pending' or status == 'r1-done':
            sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                                file_level="RO2").union(
                FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="RO2").union(
                    FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                  file_level="RO2").union(
                        FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="RO2"))))
            context['users'] = set(
                [file.user for file in sls_files]
            ).intersection(context['sls_inclusion'])
        elif status == 'r2-done' or status == 'r1-done':
            sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                                file_level="HR").union(
                FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="HR").union(
                    FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                  file_level="HR").union(
                        FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="HR"))))
            context['users'] = set(
                [file.user for file in sls_files]
            ).intersection(context['sls_inclusion'])
        else:
            context = {
                'error_code': "404: Page not found 😔",
                "error_message": "The page you are trying to access does not exist."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
    elif goalsheet == 'som':
        context['title'] = f'SOM Faculty Appraisal {context["som_config"].year}'
        if status == 'login-pending':
            som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year).union(
                FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year).union(
                    FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year).union(
                        FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year))))
            files = set([file.user for file in som_files])
            context['users'] = set(context['som_inclusion']) - files
        elif status == 'unverified':
            som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                                has_verified_data=False).union(
                FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year,
                                                              has_verified_data=False).union(
                    FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                  has_verified_data=False).union(
                        FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year,
                                                             has_verified_data=False))))
            context['users'] = set([file.user for file in som_files]).intersection(
                context['som_inclusion'])
        elif status == 'verified' or status == 'self-appraisal-pending':
            som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                                has_verified_data=True,
                                                                                file_level="APPRAISEE").union(
                FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year, has_verified_data=True,
                                                              file_level="APPRAISEE").union(
                    FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                  has_verified_data=True, file_level="APPRAISEE").union(
                        FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year, has_verified_data=True,
                                                             file_level="APPRAISEE"))))
            context['users'] = set([file.user for file in som_files]
                                   ).intersection(context['som_inclusion'])
        elif status == 'self-appraisal-submitted' or status == 'r1-pending':
            som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                                file_level="RO1").union(
                FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="RO1").union(
                    FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                  file_level="RO1").union(
                        FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="RO1"))))
            context['users'] = set(
                [file.user for file in som_files]
            ).intersection(context['som_inclusion'])
        elif status == 'r2-pending' or status == 'r1-done':
            som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                                file_level="RO2").union(
                FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="RO2").union(
                    FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                  file_level="RO2").union(
                        FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="RO2"))))
            context['users'] = set(
                [file.user for file in som_files]
            ).intersection(context['som_inclusion'])
        elif status == 'r2-done' or status == 'r1-done':
            som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                                file_level="HR").union(
                FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="HR").union(
                    FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                  file_level="HR").union(
                        FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="HR"))))
            context['users'] = set(
                [file.user for file in som_files]
            ).intersection(context['som_inclusion'])
        else:
            context = {
                'error_code': "404: Page not found 😔",
                "error_message": "The page you are trying to access does not exist."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
    elif goalsheet == 'math':
        context['title'] = f'Math Faculty Appraisal {context["math_config"].year}'
        if status == 'login-pending':
            math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(
                year=context["math_config"].year).union(
                MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year).union(
                    MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year).union(
                        MathProfAppraisalFile.objects.filter(year=context["math_config"].year))))
            files = set([file.user for file in math_files])
            context['users'] = set(context['math_inclusion']) - files
        elif status == 'unverified':
            math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                                 has_verified_data=False).union(
                MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year,
                                                              has_verified_data=False).union(
                    MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                  has_verified_data=False).union(
                        MathProfAppraisalFile.objects.filter(year=context["math_config"].year,
                                                             has_verified_data=False))))
            context['users'] = set([file.user for file in math_files]).intersection(
                context['math_inclusion'])
        elif status == 'verified' or status == 'self-appraisal-pending':
            math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                                 has_verified_data=True,
                                                                                 file_level="APPRAISEE").union(
                MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year, has_verified_data=True,
                                                              file_level="APPRAISEE").union(
                    MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                  has_verified_data=True, file_level="APPRAISEE").union(
                        MathProfAppraisalFile.objects.filter(year=context["math_config"].year, has_verified_data=True,
                                                             file_level="APPRAISEE"))))
            context['users'] = set([file.user for file in math_files]
                                   ).intersection(context['math_inclusion'])
        elif status == 'self-appraisal-submitted' or status == 'r1-pending':
            math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                                 file_level="RO1").union(
                MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="RO1").union(
                    MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                  file_level="RO1").union(
                        MathProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="RO1"))))
            context['users'] = set(
                [file.user for file in math_files]
            ).intersection(context['math_inclusion'])
        elif status == 'r2-pending' or status == 'r1-done':
            math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                                 file_level="RO2").union(
                MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="RO2").union(
                    MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                  file_level="RO2").union(
                        MathProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="RO2"))))
            context['users'] = set(
                [file.user for file in math_files]
            ).intersection(context['math_inclusion'])
        elif status == 'r2-done' or status == 'r1-done':
            math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                                 file_level="HR").union(
                MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="HR").union(
                    MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                  file_level="HR").union(
                        MathProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="HR"))))
            context['users'] = set(
                [file.user for file in math_files]
            ).intersection(context['math_inclusion'])
        else:
            context = {
                'error_code': "404: Page not found 😔",
                "error_message": "The page you are trying to access does not exist."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
    elif goalsheet == 'science':
        context['title'] = f'Science Faculty Appraisal {context["science_config"].year}'
        if status == 'login-pending':
            science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(
                year=context["science_config"].year).union(
                ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year).union(
                    ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year).union(
                        ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year))))
            files = set([file.user for file in science_files])
            context['users'] = set(context['science_inclusion']) - files
        elif status == 'unverified':
            science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(
                year=context["science_config"].year, has_verified_data=False).union(
                ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                 has_verified_data=False).union(
                    ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                     has_verified_data=False).union(
                        ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                has_verified_data=False))))
            context['users'] = set([file.user for file in science_files]).intersection(
                context['science_inclusion'])
        elif status == 'verified' or status == 'self-appraisal-pending':
            science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(
                year=context["science_config"].year, has_verified_data=True, file_level="APPRAISEE").union(
                ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                 has_verified_data=True, file_level="APPRAISEE").union(
                    ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                     has_verified_data=True,
                                                                     file_level="APPRAISEE").union(
                        ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                has_verified_data=True, file_level="APPRAISEE"))))
            context['users'] = set([file.user for file in science_files]
                                   ).intersection(context['science_inclusion'])
        elif status == 'self-appraisal-submitted' or status == 'r1-pending':
            science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(
                year=context["science_config"].year, file_level="RO1").union(
                ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                 file_level="RO1").union(
                    ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                     file_level="RO1").union(
                        ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                file_level="RO1"))))
            context['users'] = set(
                [file.user for file in science_files]
            ).intersection(context['science_inclusion'])
        elif status == 'r2-pending' or status == 'r1-done':
            science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(
                year=context["science_config"].year, file_level="RO2").union(
                ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                 file_level="RO2").union(
                    ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                     file_level="RO2").union(
                        ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                file_level="RO2"))))
            context['users'] = set(
                [file.user for file in science_files]
            ).intersection(context['science_inclusion'])
        elif status == 'r2-done' or status == 'r1-done':
            science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(
                year=context["science_config"].year, file_level="HR").union(
                ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                 file_level="HR").union(
                    ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                     file_level="HR").union(
                        ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year, file_level="HR"))))
            context['users'] = set(
                [file.user for file in science_files]
            ).intersection(context['science_inclusion'])
        else:
            context = {
                'error_code': "404: Page not found 😔",
                "error_message": "The page you are trying to access does not exist."
            }
            return render(request, 'html/error_pages/pages-error.html', context)
    else:
        context = {
            'error_code': "404: Page not found 😔",
            "error_message": "The page you are trying to access does not exist."
        }
        return render(request, 'html/error_pages/pages-error.html', context)

    return render(request, 'html/hr/inclusion_details.html', context)
    # return render(request, 'html/hr/home.html', context)


@login_required(login_url='login')
def hr_data_tally(request):
    if not request.user.is_hr:
        context = {
            'error_code': "Unauthorized Error",
            "error_message": "You are not authorized to view this page."
        }
        return render(request, 'html/error_pages/pages-error.html', context)

    context = {'pagename': 'hr-tally', 'count': {}}

    context['count']['FOET'] = {
        'academia_collaboration': bulk_foet.ViewAcademiaCollaboration.objects.count(),
        'additional_marks': bulk_foet.ViewAdditionalMarks.objects.count(),
        'co_curricular': bulk_foet.ViewCoCurricular.objects.count(),
        'student_feedback': bulk_foet.ViewStudentFeedback.objects.count(),
        'exam_duty': bulk_foet.ViewExamDuty.objects.count(),
        'teaching_load': bulk_foet.ViewTeachingLoad.objects.count(),

        # variable below
        'books': bulk_foet.ViewBook.objects.count(),
        'awards': bulk_foet.ViewAward.objects.count(),
        'consultancy': bulk_foet.ViewConsultancy.objects.count(),
        'patent': bulk_foet.ViewPatent.objects.count(),
        'phd_guidance': bulk_foet.ViewPhDGuidance.objects.count(),
        'project': bulk_foet.ViewProject.objects.count(),
        'publication': bulk_foet.ViewScopusWos.objects.count(),

        # total
        'total_appraisee': SOTFacultyAppraisalCycleInclusion.objects.filter(
            is_active=True).first().appraisee.all().count()
    }

    context['count']['SLS'] = {
        'academia_collaboration': bulk_sls.ViewAcademiaCollaboration.objects.count(),
        'additional_marks': bulk_sls.ViewAdditionalMarks.objects.count(),
        'co_curricular': bulk_sls.ViewCoCurricular.objects.count(),
        'student_feedback': bulk_sls.ViewStudentFeedback.objects.count(),
        'exam_duty': bulk_sls.ViewExamDuty.objects.count(),
        'teaching_load': bulk_sls.ViewTeachingLoad.objects.count(),
        'international_admission': bulk_sls.ViewInternationalAdmission.objects.count(),

        # variable below
        'books': bulk_sls.ViewBook.objects.count(),
        'awards': bulk_sls.ViewAward.objects.count(),
        'consultancy': bulk_sls.ViewConsultancy.objects.count(),
        'phd_guidance': bulk_sls.ViewPhDGuidance.objects.count(),
        'project': bulk_sls.ViewProject.objects.count(),
        'publication': bulk_sls.ViewScopusWos.objects.count(),

        # total
        'total_appraisee': SLSFacultyAppraisalCycleInclusion.objects.filter(
            is_active=True).first().appraisee.all().count()
    }

    context['count']['SOM'] = {
        'academia_collaboration': bulk_som.ViewAcademiaCollaboration.objects.count(),
        'additional_marks': bulk_som.ViewAdditionalMarks.objects.count(),
        'co_curricular': bulk_som.ViewCoCurricular.objects.count(),
        'exam_duty': bulk_som.ViewExamDuty.objects.count(),
        'student_feedback': bulk_som.ViewStudentFeedback.objects.count(),
        'teaching_load': bulk_som.ViewTeachingLoad.objects.count(),

        # variable below
        'awards': bulk_som.ViewAward.objects.count(),
        'books': bulk_som.ViewBook.objects.count(),
        'consultancy': bulk_som.ViewConsultancy.objects.count(),
        'phd_guidance': bulk_som.ViewPhDGuidance.objects.count(),
        'project': bulk_som.ViewProject.objects.count(),
        'publication': bulk_som.ViewScopusWos.objects.count(),

        # total
        'total_appraisee': SPMFacultyAppraisalCycleInclusion.objects.filter(
            is_active=True).first().appraisee.all().count()
    }

    context['count']['MATHS'] = {
        'academia_collaboration': bulk_math.ViewAcademiaCollaboration.objects.count(),
        'additional_marks': bulk_math.ViewAdditionalMarks.objects.count(),
        'co_curricular': bulk_math.ViewCoCurricular.objects.count(),
        'exam_duty': bulk_math.ViewExamDuty.objects.count(),
        'student_feedback': bulk_math.ViewStudentFeedback.objects.count(),
        'teaching_load': bulk_math.ViewTeachingLoad.objects.count(),

        # variable below
        'awards': bulk_math.ViewAward.objects.count(),
        'books': bulk_math.ViewBook.objects.count(),
        'phd_guidance': bulk_math.ViewPhDGuidance.objects.count(),
        'project': bulk_math.ViewProject.objects.count(),
        'publication': bulk_math.ViewScopusWos.objects.count(),

        # total
        'total_appraisee': MathFacultyAppraisalCycleInclusion.objects.filter(
            is_active=True).first().appraisee.all().count()
    }

    context['count']['SCIENCE'] = {
        'academia_collaboration': bulk_science.ViewAcademiaCollaboration.objects.count(),
        'additional_marks': bulk_science.ViewAdditionalMarks.objects.count(),
        'co_curricular': bulk_science.ViewCoCurricular.objects.count(),
        'exam_duty': bulk_science.ViewExamDuty.objects.count(),
        'student_feedback': bulk_science.ViewStudentFeedback.objects.count(),
        'teaching_load': bulk_science.ViewTeachingLoad.objects.count(),

        # variable below
        'awards': bulk_science.ViewAward.objects.count(),
        'books': bulk_science.ViewBook.objects.count(),
        'phd_guidance': bulk_science.ViewPhDGuidance.objects.count(),
        'project': bulk_science.ViewProject.objects.count(),
        'publication': bulk_science.ViewScopusWos.objects.count(),
        'patent': bulk_science.ViewPatent.objects.count(),

        # total
        'total_appraisee': ScienceFacultyAppraisalCycleInclusion.objects.filter(
            is_active=True).first().appraisee.all().count()
    }

    return render(request, 'html/hr/tally.html', context)


def get_count():
    context = {'pagename': 'hr_home',
               'staff_config': StaffAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'staff_inclusion': StaffAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all(),
               'foet_config': FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'foet_inclusion': SOTFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'sls_config': SLSFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'sls_inclusion': SLSFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'som_config': SOEMFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'som_inclusion': SPMFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'math_config': MathFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'math_inclusion': MathFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'science_config': ScienceFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first(),
               'science_inclusion': ScienceFacultyAppraisalCycleInclusion.objects.filter(
                   is_active=True).first().appraisee.all(),
               'staff_count': {},
               'foet_count': {},
               'sls_count': {},
               'som_count': {},
               'math_count': {},
               'science_count': {}
               }

    # STAFF
    context['staff_count']["login_pending"] = len(
        set(context['staff_inclusion']) - set(
            [file.user for file in StaffAppraisalFile.objects.filter(year=context["staff_config"].year)]))
    context['staff_count']["unverified"] = len(
        set([file.user for file in StaffAppraisalFile.objects.filter(year=context["staff_config"].year,
                                                                     is_all_parameters_approved=False)]).intersection(
            context['staff_inclusion']))
    context['staff_count']['verified'] = len(set([file.user for file in
                                                  StaffAppraisalFile.objects.filter(year=context["staff_config"].year,
                                                                                    is_all_parameters_approved=True)]
                                                 ).intersection(context['staff_inclusion']))

    context['staff_count']['self_appraisal_pending'] = len(set(
        [file.user for file in
         StaffAppraisalFile.objects.filter(year=context["staff_config"].year, file_level="APPRAISEE",
                                           is_all_parameters_approved=True)]
    ).intersection(context['staff_inclusion']))
    context['staff_count']['self_appraisal_submitted'] = len(set(
        [file.user for file in StaffAppraisalFile.objects.filter(year=context["staff_config"].year, file_level="RO1",
                                                                 is_all_parameters_approved=True)]
    ).intersection(context['staff_inclusion']))
    context['staff_count']['r1_pending'] = context['staff_count']['self_appraisal_submitted']
    context['staff_count']['r1_done'] = len(set(
        [file.user for file in StaffAppraisalFile.objects.filter(year=context["staff_config"].year, file_level="RO2",
                                                                 is_all_parameters_approved=True)]
    ).intersection(context['staff_inclusion']))
    context['staff_count']['r2_pending'] = context['staff_count']['r1_done']

    context['staff_count']['r2_done'] = len(set(
        [file.user for file in StaffAppraisalFile.objects.filter(year=context["staff_config"].year, file_level="HR",
                                                                 is_all_parameters_approved=True)]
    ).intersection(context['staff_inclusion']))

    # FOET
    foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year).union(
        FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year).union(
            FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year).union(
                FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year))))
    files = set([file.user for file in foet_files])
    context['foet_count']['login_pending'] = len(set(context['foet_inclusion']) - files)
    foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                         has_verified_data=False).union(
        FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year, has_verified_data=False).union(
            FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                          has_verified_data=False).union(
                FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year, has_verified_data=False))))
    context['foet_count']['unverified'] = len(
        set([file.user for file in foet_files]).intersection(context['foet_inclusion']))
    foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                         has_verified_data=True,
                                                                         file_level="APPRAISEE").union(
        FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year, has_verified_data=True,
                                                      file_level="APPRAISEE").union(
            FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year, has_verified_data=True,
                                                          file_level="APPRAISEE").union(
                FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year, has_verified_data=True,
                                                     file_level="APPRAISEE"))))
    context['foet_count']['verified'] = len(
        set([file.user for file in foet_files]).intersection(context['foet_inclusion']))
    context['foet_count']['self_appraisal_pending'] = context['foet_count']['verified']
    foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                         file_level="RO1").union(
        FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="RO1").union(
            FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="RO1").union(
                FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="RO1"))))
    context['foet_count']['self_appraisal_submitted'] = len(
        set([file.user for file in foet_files]).intersection(context['foet_inclusion']))
    context['foet_count']['r1_pending'] = context['foet_count']['self_appraisal_submitted']
    foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                         file_level="RO2").union(
        FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="RO2").union(
            FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="RO2").union(
                FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="RO2"))))
    context['foet_count']['r1_done'] = len(
        set([file.user for file in foet_files]).intersection(context['foet_inclusion']))
    context['foet_count']['r2_pending'] = context['foet_count']['r1_done']
    foet_files = FOETAssistantProfOnContractAppraisalFile.objects.filter(year=context["foet_config"].year,
                                                                         file_level="HR").union(
        FOETAssistantProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="HR").union(
            FOETAssociateProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="HR").union(
                FOETProfAppraisalFile.objects.filter(year=context["foet_config"].year, file_level="HR"))))
    context['foet_count']['r2_done'] = len(
        set([file.user for file in foet_files]).intersection(context['foet_inclusion']))

    # FOLS

    sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year).union(
        FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year).union(
            FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year).union(
                FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year))))
    files = set([file.user for file in sls_files])
    context['sls_count']['login_pending'] = len(set(context['sls_inclusion']) - files)

    sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                        has_verified_data=False).union(
        FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year, has_verified_data=False).union(
            FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                          has_verified_data=False).union(
                FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year, has_verified_data=False))))
    context['sls_count']['unverified'] = len(
        set([file.user for file in sls_files]).intersection(context['sls_inclusion']))

    sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                        has_verified_data=True,
                                                                        file_level="APPRAISEE").union(
        FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year, has_verified_data=True,
                                                      file_level="APPRAISEE").union(
            FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year, has_verified_data=True,
                                                          file_level="APPRAISEE").union(
                FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year, has_verified_data=True,
                                                     file_level="APPRAISEE"))))
    context['sls_count']['verified'] = len(
        set([file.user for file in sls_files]).intersection(context['sls_inclusion']))
    context['sls_count']['self_appraisal_pending'] = context['sls_count']['verified']

    sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                        file_level="RO1").union(
        FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="RO1").union(
            FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="RO1").union(
                FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="RO1"))))
    context['sls_count']['self_appraisal_submitted'] = len(
        set([file.user for file in sls_files]).intersection(context['sls_inclusion']))
    context['sls_count']['r1_pending'] = context['sls_count']['self_appraisal_submitted']

    sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                        file_level="RO2").union(
        FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="RO2").union(
            FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="RO2").union(
                FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="RO2"))))
    context['sls_count']['r1_done'] = len(set([file.user for file in sls_files]).intersection(context['sls_inclusion']))
    context['sls_count']['r2_pending'] = context['sls_count']['r1_done']

    sls_files = FOLSAssistantProfOnContractAppraisalFile.objects.filter(year=context["sls_config"].year,
                                                                        file_level="HR").union(
        FOLSAssistantProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="HR").union(
            FOLSAssociateProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="HR").union(
                FOLSProfAppraisalFile.objects.filter(year=context["sls_config"].year, file_level="HR"))))
    context['sls_count']['r2_done'] = len(set([file.user for file in sls_files]).intersection(context['sls_inclusion']))

    # SOM

    som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year).union(
        FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year).union(
            FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year).union(
                FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year))))
    files = set([file.user for file in som_files])
    context['som_count']['login_pending'] = len(set(context['som_inclusion']) - files)

    som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                        has_verified_data=False).union(
        FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year, has_verified_data=False).union(
            FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year,
                                                          has_verified_data=False).union(
                FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year, has_verified_data=False))))
    context['som_count']['unverified'] = len(
        set([file.user for file in som_files]).intersection(context['som_inclusion']))

    som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                        has_verified_data=True,
                                                                        file_level="APPRAISEE").union(
        FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year, has_verified_data=True,
                                                      file_level="APPRAISEE").union(
            FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year, has_verified_data=True,
                                                          file_level="APPRAISEE").union(
                FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year, has_verified_data=True,
                                                     file_level="APPRAISEE"))))
    context['som_count']['verified'] = len(
        set([file.user for file in som_files]).intersection(context['som_inclusion']))
    context['som_count']['self_appraisal_pending'] = context['som_count']['verified']

    som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                        file_level="RO1").union(
        FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="RO1").union(
            FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="RO1").union(
                FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="RO1"))))
    context['som_count']['self_appraisal_submitted'] = len(
        set([file.user for file in som_files]).intersection(context['som_inclusion']))
    context['som_count']['r1_pending'] = context['som_count']['self_appraisal_submitted']

    som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                        file_level="RO2").union(
        FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="RO2").union(
            FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="RO2").union(
                FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="RO2"))))
    context['som_count']['r1_done'] = len(set([file.user for file in som_files]).intersection(context['som_inclusion']))
    context['som_count']['r2_pending'] = context['som_count']['r1_done']

    som_files = FOEMAssistantProfOnContractAppraisalFile.objects.filter(year=context["som_config"].year,
                                                                        file_level="HR").union(
        FOEMAssistantProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="HR").union(
            FOEMAssociateProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="HR").union(
                FOEMProfAppraisalFile.objects.filter(year=context["som_config"].year, file_level="HR"))))
    context['som_count']['r2_done'] = len(set([file.user for file in som_files]).intersection(context['som_inclusion']))

    # MATHS

    math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year).union(
        MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year).union(
            MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year).union(
                MathProfAppraisalFile.objects.filter(year=context["math_config"].year))))
    files = set([file.user for file in math_files])
    context['math_count']['login_pending'] = len(set(context['math_inclusion']) - files)

    math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                         has_verified_data=False).union(
        MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year, has_verified_data=False).union(
            MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year,
                                                          has_verified_data=False).union(
                MathProfAppraisalFile.objects.filter(year=context["math_config"].year, has_verified_data=False))))
    context['math_count']['unverified'] = len(set([file.user for file in math_files]).intersection(
        context['math_inclusion']))

    math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                         has_verified_data=True,
                                                                         file_level="APPRAISEE").union(
        MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year, has_verified_data=True,
                                                      file_level="APPRAISEE").union(
            MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year, has_verified_data=True,
                                                          file_level="APPRAISEE").union(
                MathProfAppraisalFile.objects.filter(year=context["math_config"].year, has_verified_data=True,
                                                     file_level="APPRAISEE"))))
    context['math_count']['verified'] = len(
        set([file.user for file in math_files]).intersection(context['math_inclusion']))
    context['math_count']['self_appraisal_pending'] = context['math_count']['verified']

    math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                         file_level="RO1").union(
        MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="RO1").union(
            MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="RO1").union(
                MathProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="RO1"))))
    context['math_count']['self_appraisal_submitted'] = len(
        set([file.user for file in math_files]).intersection(context['math_inclusion']))
    context['math_count']['r1_pending'] = context['math_count']['self_appraisal_submitted']

    math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                         file_level="RO2").union(
        MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="RO2").union(
            MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="RO2").union(
                MathProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="RO2"))))
    context['math_count']['r1_done'] = len(
        set([file.user for file in math_files]).intersection(context['math_inclusion']))
    context['math_count']['r2_pending'] = context['math_count']['r1_done']

    math_files = MathAssistantProfOnContractAppraisalFile.objects.filter(year=context["math_config"].year,
                                                                         file_level="HR").union(
        MathAssistantProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="HR").union(
            MathAssociateProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="HR").union(
                MathProfAppraisalFile.objects.filter(year=context["math_config"].year, file_level="HR"))))
    context['math_count']['r2_done'] = len(
        set([file.user for file in math_files]).intersection(context['math_inclusion']))

    # SCIENCE

    science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(
        year=context["science_config"].year).union(
        ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year).union(
            ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year).union(
                ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year))))
    files = set([file.user for file in science_files])
    context['science_count']['login_pending'] = len(set(context['science_inclusion']) - files)

    science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                               has_verified_data=False).union(
        ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                         has_verified_data=False).union(
            ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                             has_verified_data=False).union(
                ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year, has_verified_data=False))))
    context['science_count']['unverified'] = len(set([file.user for file in science_files]).intersection(
        context['science_inclusion']))

    science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                               has_verified_data=True,
                                                                               file_level="APPRAISEE").union(
        ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year, has_verified_data=True,
                                                         file_level="APPRAISEE").union(
            ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                             has_verified_data=True, file_level="APPRAISEE").union(
                ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year, has_verified_data=True,
                                                        file_level="APPRAISEE"))))
    context['science_count']['verified'] = len(
        set([file.user for file in science_files]).intersection(context['science_inclusion']))
    context['science_count']['self_appraisal_pending'] = context['science_count']['verified']

    science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                               file_level="RO1").union(
        ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year, file_level="RO1").union(
            ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                             file_level="RO1").union(
                ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year, file_level="RO1"))))
    context['science_count']['self_appraisal_submitted'] = len(
        set([file.user for file in science_files]).intersection(context['science_inclusion']))
    context['science_count']['r1_pending'] = context['science_count']['self_appraisal_submitted']

    science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                               file_level="RO2").union(
        ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year, file_level="RO2").union(
            ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                             file_level="RO2").union(
                ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year, file_level="RO2"))))
    context['science_count']['r1_done'] = len(
        set([file.user for file in science_files]).intersection(context['science_inclusion']))
    context['science_count']['r2_pending'] = context['science_count']['r1_done']

    science_files = ScienceAssistantProfOnContractAppraisalFile.objects.filter(year=context["science_config"].year,
                                                                               file_level="HR").union(
        ScienceAssistantProfAppraisalFile.objects.filter(year=context["science_config"].year, file_level="HR").union(
            ScienceAssociateProfAppraisalFile.objects.filter(year=context["science_config"].year,
                                                             file_level="HR").union(
                ScienceProfAppraisalFile.objects.filter(year=context["science_config"].year, file_level="HR"))))
    context['science_count']['r2_done'] = len(
        set([file.user for file in science_files]).intersection(context['science_inclusion']))

    return {'staff': context['staff_count'],
            'foet': context['foet_count'],
            'sls': context['sls_count'],
            'som': context['som_count'],
            'math': context['math_count'],
            'science': context['science_count'],
            }


class APIVerifyViews:
    @staticmethod
    def patent_home(request):
        context = {
            'pagename': 'hr-api-patent-home',
            'request': request,
            'title': "Verify Patent Data from API",
            'child_view': 'hr-api-patent'
        }
        school_wise_inclusion = SOTFacultyAppraisalCycleInclusion.objects.filter(
            is_active=True).first().appraisee.all().union(
            SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()).union(
            SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()).union(
            MathFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()).union(
            ScienceFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())

        included_appraisees = {}
        for i in school_wise_inclusion:
            included_appraisees[i.email.lower()] = i
        data = get_patents(FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year)
        unmatched_records = []
        for i in data:
            if i['Email'].lower() not in included_appraisees:
                unmatched_records.append(i.values())
        context['unmatched_records'] = unmatched_records
        context['total_records'] = len(data)
        context['headers'] = data[0].keys()
        return render(request, 'html/hr/verify_home.html', context)

    @staticmethod
    @login_required(login_url='/')
    def patent(request, school):
        school_active_year_map = {
            'sot': FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'sls': SLSFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'som': SOEMFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'math': MathFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'science': ScienceFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
        }
        school_wise_inclusion = {
            'sot': SOTFacultyAppraisalCycleInclusion,
            'sls': SLSFacultyAppraisalCycleInclusion,
            'som': SPMFacultyAppraisalCycleInclusion,
            'math': MathFacultyAppraisalCycleInclusion,
            'science': ScienceFacultyAppraisalCycleInclusion
        }
        included_appraisees = {}
        for i in school_wise_inclusion[school].objects.filter(is_active=True).first().appraisee.all():
            included_appraisees[i.email.lower()] = i
        data = get_patents(school_active_year_map[school])
        context = {
            'pagename': 'hr-api-patent-home',
            'request': request,
            'title': "Verify Patent Data from API",
            'headers': data[0].keys(),
            'data': []
        }
        hash_pragma = [
            'internal_ID',
            'uid',
            'Email',
            'department',
            'school',
            'brief_school',
            'ptn_type',
            'ptn_desc',
            'month',
            'yr',
            'application_no',
        ]
        for i in list(data):
            if i['Email'].lower() in included_appraisees:
                i['hash'] = hashlib.md5('|'.join([i[j] for j in hash_pragma]).encode()).hexdigest()
                verified = PatentRecords.objects.filter(internal_id=i['internal_ID']).first()
                if verified:
                    i['remarks'] = verified.remarks
                    i['is_verified'] = verified.is_verified
                    i['is_rejected'] = verified.is_rejected
                    i['is_finalized'] = verified.is_finalized
                    if i['hash'] == verified.hash:
                        if verified.is_verified:
                            i['status'] = 'verified'
                            i['status_code'] = 0
                        if verified.is_rejected:
                            i['status'] = 'rejected'
                            i['status_code'] = 1
                    else:
                        if verified.is_verified:
                            i['status'] = 'modified_after_verification'
                            i['status_code'] = 4
                        if verified.is_rejected:
                            i['status'] = 'modified'
                            i['status_code'] = 3
                        i['old_data'] = verified.to_dict()
                else:
                    i['status'] = 'unverified'
                    i['status_code'] = 2
                context['data'].append(i)
        context['data_json'] = json.dumps(context['data'])
        if request.method == 'POST':
            for d in context['data']:
                if request.POST.get(f'patent-record-{d["internal_ID"]}') is None:
                    continue
                decision = request.POST.get(f'patent-record-{d["internal_ID"]}').strip()
                remarks = request.POST.get(f'patent-record-{d["internal_ID"]}-remarks').strip()
                if d['status'] == 'unverified':
                    v = PatentRecords()
                else:
                    v = PatentRecords.objects.filter(internal_id=d['internal_ID']).first()
                v.internal_id = d['internal_ID']
                v.faculty = included_appraisees[d['Email'].lower()]
                v.uid = d['uid']
                v.Email = d['Email']
                v.department = d['department']
                v.school = d['school']
                v.brief_school = d['brief_school']
                v.ptn_type = d['ptn_type'].lower()
                v.ptn_desc = d['ptn_desc']
                v.month = d['month']
                v.yr = d['yr']
                v.application_no = d['application_no']
                v.hash = d['hash']
                if decision == "reject":
                    v.is_rejected = True
                    v.is_verified = False
                    v.rejected_by = request.user
                if decision == 'accept':
                    v.is_rejected = False
                    v.is_verified = True
                    v.verified_by = request.user
                v.remarks = remarks
                v.save()
            return redirect('hr-api-patent', school=school)
        return render(request, 'html/hr/verify_patent.html', context)

    @staticmethod
    @login_required(login_url='/')
    def patent_reverse(request, school, internal_id):
        try:
            patent_record = PatentRecords.objects.get(internal_id=internal_id)
            if patent_record:
                patent_record.delete()
        except Exception as e:
            print(e)
        return redirect('hr-api-patent', school=school)

    @staticmethod
    def paper_home(request):
        context = {
            'pagename': 'hr-api-paper-home',
            'request': request,
            'title': "Verify Paper Data from API",
            'child_view': 'hr-api-paper'
        }
        school_wise_inclusion = SOTFacultyAppraisalCycleInclusion.objects.filter(
            is_active=True).first().appraisee.all().union(
            SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()).union(
            SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()).union(
            MathFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()).union(
            ScienceFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())

        included_appraisees = {}
        for i in school_wise_inclusion:
            included_appraisees[i.email.lower()] = i
        data = get_papers(FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year)
        unmatched_records = []
        for i in data:
            if i['Email'].lower() not in included_appraisees:
                unmatched_records.append(i.values())
        context['unmatched_records'] = unmatched_records
        context['total_records'] = len(data)
        context['headers'] = data[0].keys()
        return render(request, 'html/hr/verify_home.html', context)

    @staticmethod
    @login_required(login_url='/')
    def paper(request, school):
        school_active_year_map = {
            'sot': FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'sls': SLSFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'som': SOEMFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'math': MathFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'science': ScienceFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
        }
        school_wise_inclusion = {
            'sot': SOTFacultyAppraisalCycleInclusion,
            'sls': SLSFacultyAppraisalCycleInclusion,
            'som': SPMFacultyAppraisalCycleInclusion,
            'math': MathFacultyAppraisalCycleInclusion,
            'science': ScienceFacultyAppraisalCycleInclusion
        }
        included_appraisees = {}
        for i in school_wise_inclusion[school].objects.filter(is_active=True).first().appraisee.all():
            included_appraisees[i.email.lower()] = i
        data = get_papers(school_active_year_map[school])
        # f = open(f"HR/paper.json", "r")
        # data = json.load(f)
        # f.close()
        context = {
            'pagename': 'hr-api-paper-home',
            'request': request,
            'title': "Verify Paper Data from API",
            'headers': data[0].keys(),
            'data': []
        }
        for i in list(data):
            if i['Email'].lower() in included_appraisees:
                i['hash'] = PaperRecords.calculate_hash(i)
                verified = PaperRecords.objects.filter(internal_id=i['internal_ID']).first()
                if verified:
                    i['remarks'] = verified.remarks
                    i['is_verified'] = verified.is_verified
                    i['is_rejected'] = verified.is_rejected
                    i['is_finalized'] = verified.is_finalized
                    if i['hash'] == verified.hash:
                        if verified.is_verified:
                            i['status'] = 'verified'
                            i['status_code'] = 0
                        if verified.is_rejected:
                            i['status'] = 'rejected'
                            i['status_code'] = 1
                    else:
                        if verified.is_verified:
                            i['status'] = 'modified_after_verification'
                            i['status_code'] = 4
                        if verified.is_rejected:
                            i['status'] = 'modified'
                            i['status_code'] = 3
                        i['old_data'] = verified.to_dict()
                else:
                    i['status'] = 'unverified'
                    i['status_code'] = 2
                context['data'].append(i)
        context['data_json'] = json.dumps(context['data'])
        if request.method == 'POST':
            errors = []
            for d in context['data']:
                if request.POST.get(f'paper-record-{d["internal_ID"]}') is None:
                    continue
                decision = request.POST.get(f'paper-record-{d["internal_ID"]}').strip()
                remarks = request.POST.get(f'paper-record-{d["internal_ID"]}-remarks').strip()
                if d['status'] == 'unverified':
                    v = PaperRecords()
                else:
                    v = PaperRecords.objects.filter(internal_id=d['internal_ID']).first()
                v.populate(d)
                v.faculty = included_appraisees[d['Email'].lower()]
                v.hash = d['hash']
                if decision == "reject":
                    v.is_rejected = True
                    v.is_verified = False
                    v.rejected_by = request.user
                if decision == 'accept':
                    v.is_rejected = False
                    v.is_verified = True
                    v.verified_by = request.user
                v.remarks = remarks
                try:
                    v.save()
                except Exception as e:
                    errors.append(f"Error saving record {d['internal_ID']}: {str(e)}")
            if errors:
                errors = '\n\n\n'.join(errors).replace('\n', '<br>')
                return HttpResponse(f"<p>The following records werernt saved due to data errors<br><br>{errors}:</p>")
            return redirect('hr-api-paper', school=school)
        return render(request, 'html/hr/verify_paper.html', context)

    @staticmethod
    @login_required(login_url='/')
    def paper_reverse(request, school, internal_id):
        try:
            paper_record = PaperRecords.objects.get(internal_id=internal_id)
            if paper_record:
                paper_record.delete()
        except Exception as e:
            print(e)
        return redirect('hr-api-paper', school=school)

    @staticmethod
    @login_required(login_url='/')
    def books_home(request):
        context = {
            'pagename': 'hr-api-books-home',
            'request': request,
            'title': "Verify Books Data from API",
            'child_view': 'hr-api-books'
        }
        school_wise_inclusion = SOTFacultyAppraisalCycleInclusion.objects.filter(
            is_active=True).first().appraisee.all().union(
            SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()).union(
            SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()).union(
            MathFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()).union(
            ScienceFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all())

        included_appraisees = {}
        for i in school_wise_inclusion:
            included_appraisees[i.email.lower()] = i
        data = get_books(FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year)
        unmatched_records = []
        for i in data:
            if i['Email'].lower() not in included_appraisees:
                unmatched_records.append(i.values())
        context['unmatched_records'] = unmatched_records
        context['total_records'] = len(data)
        context['headers'] = data[0].keys()
        return render(request, 'html/hr/verify_home.html', context)

    @staticmethod
    @login_required(login_url='/')
    def books(request, school):
        school_active_year_map = {
            'sot': FOETFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'sls': SLSFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'som': SOEMFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'math': MathFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
            'science': ScienceFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first().year,
        }
        school_wise_inclusion = {
            'sot': SOTFacultyAppraisalCycleInclusion,
            'sls': SLSFacultyAppraisalCycleInclusion,
            'som': SPMFacultyAppraisalCycleInclusion,
            'math': MathFacultyAppraisalCycleInclusion,
            'science': ScienceFacultyAppraisalCycleInclusion
        }
        included_appraisees = {}
        for i in school_wise_inclusion[school].objects.filter(is_active=True).first().appraisee.all():
            included_appraisees[i.email.lower()] = i
        data = get_books(school_active_year_map[school])
        # f = open(f"HR/books.json", "r")
        # data = json.load(f)
        # f.close()
        context = {
            'pagename': 'hr-api-books-home',
            'request': request,
            'title': "Verify Book Data from API",
            'headers': data[0].keys(),
            'data': []
        }
        for i in list(data):
            if i['Email'].lower() in included_appraisees:
                i['hash'] = BookRecords.calculate_hash(i)
                verified = BookRecords.objects.filter(internal_id=i['internal_ID']).first()
                if verified:
                    i['remarks'] = verified.remarks
                    i['is_verified'] = verified.is_verified
                    i['is_rejected'] = verified.is_rejected
                    i['is_finalized'] = verified.is_finalized
                    if i['hash'] == verified.hash:
                        if verified.is_verified:
                            i['status'] = 'verified'
                            i['status_code'] = 0
                        if verified.is_rejected:
                            i['status'] = 'rejected'
                            i['status_code'] = 1
                    else:
                        if verified.is_verified:
                            i['status'] = 'modified_after_verification'
                            i['status_code'] = 4
                        if verified.is_rejected:
                            i['status'] = 'modified'
                            i['status_code'] = 3
                        i['old_data'] = verified.to_dict()
                else:
                    i['status'] = 'unverified'
                    i['status_code'] = 2
                context['data'].append(i)
        context['data_json'] = json.dumps(context['data'])
        if request.method == 'POST':
            errors = []
            for d in context['data']:
                if request.POST.get(f'book-record-{d["internal_ID"]}') is None:
                    continue
                decision = request.POST.get(f'book-record-{d["internal_ID"]}').strip()
                remarks = request.POST.get(f'book-record-{d["internal_ID"]}-remarks').strip()
                if d['status'] == 'unverified':
                    v = BookRecords()
                else:
                    v = BookRecords.objects.filter(internal_id=d['internal_ID']).first()
                v.populate(d)
                v.faculty = included_appraisees[d['Email'].lower()]
                v.hash = d['hash']
                if decision == "reject":
                    v.is_rejected = True
                    v.is_verified = False
                    v.rejected_by = request.user
                if decision == 'accept':
                    v.is_rejected = False
                    v.is_verified = True
                    v.verified_by = request.user
                v.remarks = remarks
                try:
                    v.save()
                except Exception as e:
                    errors.append(f"Error saving record {d['internal_ID']}: {str(e)}")
            if errors:
                errors = '\n\n\n'.join(errors).replace('\n', '<br>')
                return HttpResponse(f"<p>The following records werernt saved due to data errors<br><br>{errors}:</p>")
            return redirect('hr-api-books', school=school)
        return render(request, 'html/hr/verify_book.html', context)

    @staticmethod
    @login_required(login_url='/')
    def book_reverse(request, school, internal_id):
        try:
            paper_record = BookRecords.objects.get(internal_id=internal_id)
            if paper_record:
                paper_record.delete()
        except Exception as e:
            print(e)
        return redirect('hr-api-books', school=school)

    @staticmethod
    @login_required(login_url='/')
    def finalize_verified_patent(request):
        # PatentRecords.objects.all().update(is_finalized=False)
        if request.method == "POST":
            from BulkUpload.BulkUploadFoET.models import ViewPatent as SOTViewPatent
            from BulkUpload.BulkUploadFoLS.models import ViewPatent as SLSViewPatent
            from BulkUpload.BulkUploadFoEM.models import ViewPatent as SOMViewPatent
            from BulkUpload.BulkUploadScience.models import ViewPatent as ScienceViewPatent
            school_map = {
                'sot': SOTViewPatent,
                'sls': SLSViewPatent,
                'som': SOMViewPatent,
                'math': None,
                'science': ScienceViewPatent
            }
            school_wise_inclusion = {
                'sot': SOTFacultyAppraisalCycleInclusion,
                'sls': SLSFacultyAppraisalCycleInclusion,
                'som': SPMFacultyAppraisalCycleInclusion,
                'math': MathFacultyAppraisalCycleInclusion,
                'science': ScienceFacultyAppraisalCycleInclusion
            }
            user_map = {}
            for school, inclusion in school_wise_inclusion.items():
                for i in inclusion.objects.filter(is_active=True).first().appraisee.all():
                    user_map[i] = school
            PatentRecords.bulk_create_prepopulated_data(
                PatentRecords.objects.filter(is_verified=True, is_finalized=False),
                school_map,
                user_map
            )
            PatentRecords.objects.filter(is_verified=True, is_finalized=False).update(is_finalized=True)
        context = {
            'pagename': 'hr-api-patent-finalize',
            'request': request,
            'title': "Finalize Verified Patents",
            'child_view': 'hr-api-patent',
            'data': [i.to_dict().values() for i in PatentRecords.objects.filter(is_verified=True, is_finalized=False)],
            'headers': PatentRecords.objects.filter(is_verified=True).first().to_dict().keys()
        }
        return render(request, 'html/hr/finalize_records.html', context)

    @staticmethod
    @login_required(login_url='/')
    def finalize_verified_paper(request):
        # PatentRecords.objects.all().update(is_finalized=False)
        if request.method == "POST":
            from BulkUpload.BulkUploadFoET.models import ViewScopusWos as SOTViewScopusWos
            from BulkUpload.BulkUploadFoLS.models import ViewScopusWos as SLSViewScopusWos
            from BulkUpload.BulkUploadFoEM.models import ViewScopusWos as SOMViewScopusWos
            from BulkUpload.BulkUploadScience.models import ViewScopusWos as ScienceViewScopusWos
            from BulkUpload.BulkUploadMaths.models import ViewScopusWos as MathViewScopusWos
            school_map = {
                'sot': SOTViewScopusWos,
                'sls': SLSViewScopusWos,
                'som': SOMViewScopusWos,
                'math': MathViewScopusWos,
                'science': ScienceViewScopusWos
            }
            school_wise_inclusion = {
                'sot': SOTFacultyAppraisalCycleInclusion,
                'sls': SLSFacultyAppraisalCycleInclusion,
                'som': SPMFacultyAppraisalCycleInclusion,
                'math': MathFacultyAppraisalCycleInclusion,
                'science': ScienceFacultyAppraisalCycleInclusion
            }
            user_map = {}
            for school, inclusion in school_wise_inclusion.items():
                for i in inclusion.objects.filter(is_active=True).first().appraisee.all():
                    user_map[i] = school
            PaperRecords.bulk_create_prepopulated_data(
                PaperRecords.objects.filter(is_verified=True, is_finalized=False),
                school_map,
                user_map
            )
            PaperRecords.objects.filter(is_verified=True, is_finalized=False).update(is_finalized=True)
        context = {
            'pagename': 'hr-api-paper-finalize',
            'request': request,
            'title': "Finalize Verified Papers",
            'child_view': 'hr-api-paper',
            'data': [i.to_dict().values() for i in PaperRecords.objects.filter(is_verified=True, is_finalized=False)],
            'headers': PaperRecords.objects.filter(is_verified=True).first().to_dict().keys()
        }
        return render(request, 'html/hr/finalize_records.html', context)

    @staticmethod
    @login_required(login_url='/')
    def finalize_verified_books(request):
        # PatentRecords.objects.all().update(is_finalized=False)
        if request.method == "POST":
            from BulkUpload.BulkUploadFoET.models import ViewBook as SOTViewBook
            from BulkUpload.BulkUploadFoLS.models import ViewBook as SLSViewBook
            from BulkUpload.BulkUploadFoEM.models import ViewBook as SOMViewBook
            from BulkUpload.BulkUploadScience.models import ViewBook as ScienceViewBook
            from BulkUpload.BulkUploadMaths.models import ViewBook as MathViewBook
            school_map = {
                'sot': SOTViewBook,
                'sls': SLSViewBook,
                'som': SOMViewBook,
                'math': MathViewBook,
                'science': ScienceViewBook
            }
            school_wise_inclusion = {
                'sot': SOTFacultyAppraisalCycleInclusion,
                'sls': SLSFacultyAppraisalCycleInclusion,
                'som': SPMFacultyAppraisalCycleInclusion,
                'math': MathFacultyAppraisalCycleInclusion,
                'science': ScienceFacultyAppraisalCycleInclusion
            }
            user_map = {}
            for school, inclusion in school_wise_inclusion.items():
                for i in inclusion.objects.filter(is_active=True).first().appraisee.all():
                    user_map[i] = school
            BookRecords.bulk_create_prepopulated_data(
                BookRecords.objects.filter(is_verified=True, is_finalized=False),
                school_map,
                user_map
            )
            BookRecords.objects.filter(is_verified=True, is_finalized=False).update(is_finalized=True)
        context = {
            'pagename': 'hr-api-books-finalize',
            'request': request,
            'title': "Finalize Verified Books",
            'child_view': 'hr-api-books',
            'data': [i.to_dict().values() for i in BookRecords.objects.filter(is_verified=True, is_finalized=False)],
            'headers': BookRecords.objects.filter(is_verified=True).first().to_dict().keys()
        }
        return render(request, 'html/hr/finalize_records.html', context)


def get_patents(year):
    session = requests_cache.CachedSession('orsp_cache', expire_after=360)
    api_endpoint = f"https://orsp.pdpu.ac.in/API/APAS.asmx/Getpatent?key=B77A5C561934E089&year={year}"
    resp = session.get(api_endpoint)
    return json.loads(fromstring(resp.content).text)


def get_papers(year):
    session = requests_cache.CachedSession('orsp_cache', expire_after=360)
    api_endpoint = f"https://orsp.pdpu.ac.in/API/APAS.asmx/Getpaper?key=B77A5C561934E089&year={year}"
    resp = session.get(api_endpoint)
    return json.loads(fromstring(resp.content).text)


def get_books(year):
    session = requests_cache.CachedSession('orsp_cache', expire_after=360)
    api_endpoint = f"https://orsp.pdpu.ac.in/API/APAS.asmx/Getbook?key=B77A5C561934E089&year={year}"
    resp = session.get(api_endpoint)
    return json.loads(fromstring(resp.content).text)

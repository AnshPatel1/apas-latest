from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from MasterConfiguration.models import StaffAppraisalCycleInclusion
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

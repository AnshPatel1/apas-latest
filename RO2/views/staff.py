import json

from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render

from Account.models import User
from RO1.views import HelperFunctions
from Staff.models import *


class RO2StaffView:
    def __init__(self):
        pass

    @login_required(login_url='/login/')
    def staff_review(request, pk):

        if request.method == 'GET' and not request.user.is_anonymous and request.user.is_authenticated:
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'staff-review-home'
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            context['can_submit'] = HelperFunctions.can_submit(None, file)
            return render(request, 'html/r2/staff/staff-review-home.html', context)

    @login_required(login_url='/login/')
    def test(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')

            return render(request, 'html/r2/staff/staff-review-home.html', context)

    @login_required(login_url='/login/')
    def approve_parameters(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'approve-parameters'
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            context['can_submit'] = HelperFunctions.can_submit(None, file)
            return render(request, 'html/r2/staff/parameter-approve.html', context)

        if request.method == 'POST':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            data = json.loads(request.POST.get('data'))
            key_data = data['key']
            saved_key_data = list(file.key_parameter.all())
            for i in range(file.key_parameter_count):
                saved_key_data[i].ro_remakrs = key_data[i]['remarks']
                if key_data[i]['status']:
                    saved_key_data[i].is_approved = True
                    saved_key_data[i].is_rejected = False
                else:
                    saved_key_data[i].is_approved = False
                    saved_key_data[i].is_rejected = True
                saved_key_data[i].save()
            maj_data = data['maj']
            saved_major_data = list(file.major_parameter.all())
            for i in range(file.major_parameter_count):
                saved_major_data[i].ro_remakrs = maj_data[i]['remarks']
                if maj_data[i]['status']:
                    saved_major_data[i].is_approved = True
                    saved_major_data[i].is_rejected = False
                else:
                    saved_major_data[i].is_approved = False
                    saved_major_data[i].is_rejected = True
                saved_major_data[i].save()

            min_data = data['min']
            saved_minor_data = list(file.minor_parameter.all())
            for i in range(file.minor_parameter_count):
                saved_minor_data[i].ro_remakrs = min_data[i]['remarks']
                if min_data[i]['status']:
                    saved_minor_data[i].is_approved = True
                    saved_minor_data[i].is_rejected = False
                else:
                    saved_minor_data[i].is_approved = False
                    saved_minor_data[i].is_rejected = True
                saved_minor_data[i].save()
            file.save()
            all_approved = True
            for i in range(file.key_parameter_count):
                if not saved_key_data[i].is_approved:
                    all_approved = False
                else:
                    if data['is_submit']:
                        saved_key_data[i].is_finalized = True
                        saved_key_data[i].save()
            for i in range(file.major_parameter_count):
                if not saved_major_data[i].is_approved:
                    all_approved = False
                else:
                    if data['is_submit']:
                        saved_major_data[i].is_finalized = True
                        saved_major_data[i].save()
            for i in range(file.minor_parameter_count):
                if not saved_minor_data[i].is_approved:
                    all_approved = False
                else:
                    if data['is_submit']:
                        saved_minor_data[i].is_finalized = True
                        saved_minor_data[i].save()
            if data['is_submit']:
                file.file_level = 'APPRAISEE'
                file.file_with = file.user
                file.ro2_validation.is_parameters_approved = all_approved
                file.ro2_validation.save()
                file.save()

            file.is_all_parameters_approved = all_approved
            file.save()

            return JsonResponse({'status': 'success'})

    @login_required(login_url='/login/')
    def grade_parameters(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'grade-parameters'
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            context['can_submit'] = HelperFunctions.can_submit(None, file)
            return render(request, 'html/r2/staff/parameter-grade.html', context)
        if request.method == 'POST':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            data = json.loads(request.POST.get('data'))

            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            key_data = data['key']
            saved_key_data = list(file.key_parameter.all())
            for i in range(file.key_parameter_count):
                saved_key_data[i].marks.ro2 = float(key_data[i]['marks'])
                saved_key_data[i].marks.ro2_remarks = key_data[i]['remarks']
                saved_key_data[i].marks.ro2_agrees_with_ro1 = key_data[i]['r2_agrees']

                saved_key_data[i].marks.save()

            maj_data = data['maj']
            saved_major_data = list(file.major_parameter.all())
            for i in range(file.major_parameter_count):
                saved_major_data[i].marks.ro2 = float(maj_data[i]['marks'])
                saved_major_data[i].marks.ro2_remarks = maj_data[i]['remarks']
                saved_major_data[i].marks.ro2_agrees_with_ro1 = maj_data[i]['r2_agrees']
                saved_major_data[i].marks.save()

            min_data = data['min']
            saved_minor_data = list(file.minor_parameter.all())
            for i in range(file.minor_parameter_count):
                saved_minor_data[i].marks.ro2 = float(min_data[i]['marks'])
                saved_minor_data[i].marks.ro2_remarks = min_data[i]['remarks']
                saved_minor_data[i].marks.ro2_agrees_with_ro1 = min_data[i]['r2_agrees']
                saved_minor_data[i].marks.save()

            if data['is_submit']:
                file.ro2_validation.is_parameters_valid = True
                file.ro2_validation.save()
            else:
                file.ro2_validation.is_parameters_valid = False
                file.ro2_validation.save()
            return JsonResponse({'status': 'success'})

    @login_required(login_url='/login/')
    def grade_self_development(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'grade-self-development'
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            context['can_submit'] = HelperFunctions.can_submit(None, file)
            return render(request, 'html/r2/staff/grade-self-development.html', context)

        if request.method == 'POST':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            data = json.loads(request.POST.get('data'))
            is_submit = json.loads(request.POST.get('is_submit'))
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')

            for index, i in enumerate(list(file.self_development_parameter.all())):
                if i.marks is None:
                    i.marks = MarkField()
                    i.marks.save()
                    i.save()
                i.marks.ro2 = float(data[index]['marks'])
                i.marks.ro2_remarks = data[index]['remarks']
                i.marks.ro2_agrees_with_ro1 = data[index]['r2_agrees']
                i.marks.save()

            if is_submit:
                file.ro2_validation.is_training_valid = True
                file.ro2_validation.save()
            else:
                file.ro2_validation.is_training_valid = False
                file.ro2_validation.save()
            return JsonResponse({'status': 'success'})

    @login_required(login_url='/login/')
    def grade_other_activities(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'grade-other-activities'
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            context['can_submit'] = HelperFunctions.can_submit(None, file)
            return render(request, 'html/r2/staff/grade-other-activities.html', context)
        if request.method == 'POST':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            data = json.loads(request.POST.get('data'))
            is_submit = json.loads(request.POST.get('is_submit'))
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            file.other_activities_parameter_marks.ro2 = float(data['marks'])
            file.other_activities_parameter_marks.ro2_remarks = data['remarks']
            file.other_activities_parameter_marks.ro2_agrees_with_ro1 = data['r2_agrees']
            file.other_activities_parameter_marks.save()
            #
            if is_submit:
                file.ro2_validation.is_other_activities_valid = True
                file.ro2_validation.save()
            else:
                file.ro2_validation.is_other_activities_valid = False
                file.ro2_validation.save()
            return JsonResponse({'status': 'success'})

    @login_required(login_url='/login/')
    def review_self_evaluation(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'review-self-evaluation'
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            context['can_submit'] = HelperFunctions.can_submit(None, file)
            return render(request, 'html/r2/staff/review-self-evaluation.html', context)

    @login_required(login_url='/login/')
    def grade_mooc(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'grade-mooc'
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            context['can_submit'] = HelperFunctions.can_submit(None, file)
            return render(request, 'html/r2/staff/grade-mooc.html', context)
        if request.method == 'POST':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            data = json.loads(request.POST.get('data'))
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            if data['marks']:
                config = StaffConfiguration.objects.get(name='master')
                file.mooc_marks_awarded.ro2 = config.max_mooc_marks
                file.mooc_marks_awarded.ro2_remarks = data['remarks']
                file.mooc_accepted = True
                file.mooc_marks_awarded.save()
                file.save()
            else:
                file.mooc_marks_awarded.ro2 = 0
                file.mooc_marks_awarded.ro2_remarks = data['remarks']
                file.mooc_accepted = False
                file.mooc_marks_awarded.save()
                file.save()
            file.mooc_marks_awarded.ro2_agrees_with_ro1 = data['r2_agrees']
            file.mooc_marks_awarded.save()
            #
            if data['is_submit']:
                file.ro2_validation.is_mooc_valid = True
                file.ro2_validation.save()
            else:
                file.ro2_validation.is_mooc_valid = False
                file.ro2_validation.save()
            return JsonResponse({'status': 'success'})

    @login_required(login_url='/login/')
    def grade_section_2(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'grade-section-2'
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            context['can_submit'] = HelperFunctions.can_submit(None, file)
            return render(request, 'html/r2/staff/grade-section-2.html', context)
        if request.method == 'POST':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            data = json.loads(request.POST.get('data'))
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')

            #  Productivity
            file.consistency_in_work.ro2 = float(data['productivity'][0]['marks'])
            file.consistency_in_work.ro2_remarks = data['productivity'][0]['remarks']
            file.consistency_in_work.ro2_agrees_with_ro1 = data['productivity'][0]['r2_agrees']
            file.consistency_in_work.save()

            file.planning_and_organization_skills.ro2 = float(data['productivity'][1]['marks'])
            file.planning_and_organization_skills.ro2_remarks = data['productivity'][1]['remarks']
            file.planning_and_organization_skills.ro2_agrees_with_ro1 = data['productivity'][1]['r2_agrees']
            file.planning_and_organization_skills.save()

            file.productivity_marks_total.ro2 = file.consistency_in_work.ro2 + file.planning_and_organization_skills.ro2
            file.productivity_marks_total.save()

            # Quality of Work
            file.flexibility_and_adaptability.ro2 = float(data['quality_of_work'][0]['marks'])
            file.flexibility_and_adaptability.ro2_remarks = data['quality_of_work'][0]['remarks']
            file.flexibility_and_adaptability.ro2_agrees_with_ro1 = data['quality_of_work'][0]['r2_agrees']
            file.flexibility_and_adaptability.save()

            file.accuracy_and_thoroughness_of_work.ro2 = float(data['quality_of_work'][1]['marks'])
            file.accuracy_and_thoroughness_of_work.ro2_remarks = data['quality_of_work'][1]['remarks']
            file.accuracy_and_thoroughness_of_work.ro2_agrees_with_ro1 = data['quality_of_work'][1]['r2_agrees']
            file.accuracy_and_thoroughness_of_work.save()

            file.quality_of_work_marks_total.ro2 = file.flexibility_and_adaptability.ro2 + file.accuracy_and_thoroughness_of_work.ro2
            file.quality_of_work_marks_total.save()

            # Domain of Expertise
            file.awareness.ro2 = float(data['domain_expertise'][0]['marks'])
            file.awareness.ro2_remarks = data['domain_expertise'][0]['remarks']
            file.awareness.ro2_agrees_with_ro1 = data['domain_expertise'][0]['r2_agrees']
            file.awareness.save()

            file.handling_unexpected_problems.ro2 = float(data['domain_expertise'][1]['marks'])
            file.handling_unexpected_problems.ro2_remarks = data['domain_expertise'][1]['remarks']
            file.handling_unexpected_problems.ro2_agrees_with_ro1 = data['domain_expertise'][1]['r2_agrees']
            file.handling_unexpected_problems.save()

            file.domain_expertise_marks_total.ro2 = file.awareness.ro2 + file.handling_unexpected_problems.ro2
            file.domain_expertise_marks_total.save()

            # Teamwork
            file.positive_approach.ro2 = float(data['teamwork'][0]['marks'])
            file.positive_approach.ro2_remarks = data['teamwork'][0]['remarks']
            file.positive_approach.ro2_agrees_with_ro1 = data['teamwork'][0]['r2_agrees']
            file.positive_approach.save()

            file.team_building_skills.ro2 = float(data['teamwork'][1]['marks'])
            file.team_building_skills.ro2_remarks = data['teamwork'][1]['remarks']
            file.team_building_skills.ro2_agrees_with_ro1 = data['teamwork'][1]['r2_agrees']
            file.team_building_skills.save()

            file.teamwork_marks_total.ro2 = file.positive_approach.ro2 + file.team_building_skills.ro2
            file.teamwork_marks_total.save()

            # Key Skills
            file.integrity.ro2 = float(data['key_skills'][0]['marks'])
            file.integrity.ro2_remarks = data['key_skills'][0]['remarks']
            file.integrity.ro2_agrees_with_ro1 = data['key_skills'][0]['r2_agrees']
            file.integrity.save()

            file.sincerity.ro2 = float(data['key_skills'][1]['marks'])
            file.sincerity.ro2_remarks = data['key_skills'][1]['remarks']
            file.sincerity.ro2_agrees_with_ro1 = data['key_skills'][1]['r2_agrees']
            file.sincerity.save()

            file.initiative_taking_skills.ro2 = float(data['key_skills'][2]['marks'])
            file.initiative_taking_skills.ro2_remarks = data['key_skills'][2]['remarks']
            file.initiative_taking_skills.ro2_agrees_with_ro1 = data['key_skills'][2]['r2_agrees']
            file.initiative_taking_skills.save()

            file.leadership_skills.ro2 = float(data['key_skills'][3]['marks'])
            file.leadership_skills.ro2_remarks = data['key_skills'][3]['remarks']
            file.leadership_skills.ro2_agrees_with_ro1 = data['key_skills'][3]['r2_agrees']
            file.leadership_skills.save()

            file.communication_skills.ro2 = float(data['key_skills'][4]['marks'])
            file.communication_skills.ro2_remarks = data['key_skills'][4]['remarks']
            file.communication_skills.ro2_agrees_with_ro1 = data['key_skills'][4]['r2_agrees']
            file.communication_skills.save()

            file.key_skills_marks_total.ro2 = file.integrity.ro2 + \
                                              file.sincerity.ro2 + \
                                              file.initiative_taking_skills.ro2 + \
                                              file.leadership_skills.ro2 + \
                                              file.communication_skills.ro2
            file.key_skills_marks_total.save()

            file.disciplinary_action_ro2 = data['disciplinary_action']
            file.disciplinary_action_ro2_agrees_with_ro1 = data['r2_agrees_disciplinary']
            file.save()
            if not file.disciplinary_action_marks:
                file.disciplinary_action_marks = MarkField()
            if data['disciplinary_action']:
                config = StaffConfiguration.objects.get(name='master')
                file.disciplinary_action_marks.ro2 = config.disciplinary_action_deductable
            else:
                file.disciplinary_action_marks.ro2 = 0
            file.disciplinary_action_marks.ro2_remarks = data['disciplinary_action_remarks']
            file.disciplinary_action_marks.save()
            file.productivity_marks_total.ro2 = round(file.productivity_marks_total.ro2, 2)
            file.productivity_marks_total.save()
            file.domain_expertise_marks_total.ro2 = round(file.domain_expertise_marks_total.ro2, 2)
            file.domain_expertise_marks_total.save()
            file.key_skills_marks_total.ro2 = round(file.key_skills_marks_total.ro2, 2)
            file.key_skills_marks_total.save()
            file.quality_of_work_marks_total.ro2 = round(file.quality_of_work_marks_total.ro2, 2)
            file.quality_of_work_marks_total.save()
            file.teamwork_marks_total.ro2 = round(file.teamwork_marks_total.ro2, 2)
            file.teamwork_marks_total.save()
            file.save()
            if data['is_submit']:
                file.ro2_validation.is_section_2_valid = True
                file.ro2_validation.save()
            else:
                file.ro2_validation.is_section_2_valid = False
                file.ro2_validation.save()
            return HttpResponse('success')

    @login_required(login_url='/login/')
    def staff_review_all(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'staff-review-all'
            context['key_total'] = 0
            context['key_params'] = []
            for i in range(file.key_parameter_count):
                context['key_total'] += float(list(file.key_parameter.all())[i].marks.ro2)
                context['key_params'].append(list(file.key_parameter.all())[i])
            context['key_total_r1'] = 0
            context['key_params_r1'] = []
            for i in range(file.key_parameter_count):
                context['key_total_r1'] += float(list(file.key_parameter.all())[i].marks.ro1)
                context['key_params_r1'].append(list(file.key_parameter.all())[i])
            context['major_total'] = 0
            context['major_params'] = []
            for i in range(file.major_parameter_count):
                context['major_total'] += float(list(file.major_parameter.all())[i].marks.ro2)
                context['major_params'].append(list(file.major_parameter.all())[i])
            context['major_total_r1'] = 0
            context['major_params_r1'] = []
            for i in range(file.major_parameter_count):
                context['major_total_r1'] += float(list(file.major_parameter.all())[i].marks.ro1)
                context['major_params_r1'].append(list(file.major_parameter.all())[i])
            context['minor_total'] = 0
            context['minor_params'] = []
            for i in range(file.minor_parameter_count):
                context['minor_total'] += float(list(file.minor_parameter.all())[i].marks.ro2)
                context['minor_params'].append(list(file.minor_parameter.all())[i])
            context['minor_total_r1'] = 0
            context['minor_params_r1'] = []
            for i in range(file.minor_parameter_count):
                context['minor_total_r1'] += float(list(file.minor_parameter.all())[i].marks.ro1)
                context['minor_params_r1'].append(list(file.minor_parameter.all())[i])

            context['self_development_total'] = 0
            for i in file.self_development_parameter.all():
                if not i.marks:
                    i.marks = MarkField()
                    i.marks.save()
                context['self_development_total'] += float(i.marks.ro2)
            context['self_development_total_r1'] = 0
            for i in file.self_development_parameter.all():
                if not i.marks:
                    i.marks = MarkField()
                    i.marks.save()
                context['self_development_total_r1'] += float(i.marks.ro1)
            context['self_development_total'] = round(context['self_development_total'], 2)
            context['self_development_total_r1'] = round(context['self_development_total_r1'], 2)
            context['section_1_total'] = context['key_total'] + context['major_total'] + context['minor_total']
            context['section_1_total_r1'] = context['key_total_r1'] + context['major_total_r1'] + context['minor_total_r1']
            if file.training_taken:
                context['section_1_total'] += context['self_development_total']
                context['section_1_total_r1'] += context['self_development_total_r1']

            if file.other_activities_parameter_available:
                context['section_1_total'] += file.other_activities_parameter_marks.ro2
                context['section_1_total_r1'] += file.other_activities_parameter_marks.ro1

            context['section_2_total'] = file.teamwork_marks_total.ro2 + \
                                         file.quality_of_work_marks_total.ro2 + \
                                         file.key_skills_marks_total.ro2 + \
                                         file.domain_expertise_marks_total.ro2 + \
                                         file.productivity_marks_total.ro2
            context['section_2_total_r1'] = file.teamwork_marks_total.ro1 + \
                                            file.quality_of_work_marks_total.ro1 + \
                                            file.key_skills_marks_total.ro1 + \
                                            file.domain_expertise_marks_total.ro1 + \
                                            file.productivity_marks_total.ro1

            context['grand_total'] = context['section_1_total'] + context['section_2_total']
            context['grand_total_r1'] = context['section_1_total_r1'] + context['section_2_total_r1']
            if file.disciplinary_action_ro2:
                context['grand_total'] -= context['config'].disciplinary_action_deductable
            if file.disciplinary_action:
                context['grand_total_r1'] -= context['config'].disciplinary_action_deductable
            if file.was_mooc_completed:
                context['grand_total'] += file.mooc_marks_awarded.ro2
                context['grand_total_r1'] += file.mooc_marks_awarded.ro1
            context['section_2_total'] = round(context['section_2_total'], 2)
            context['section_2_total_r1'] = round(context['section_2_total_r1'], 2)
            context['section_1_total'] = round(context['section_1_total'], 2)
            context['section_1_total_r1'] = round(context['section_1_total_r1'], 2)
            context['grand_total'] = round(context['grand_total'], 2)
            context['grand_total_r1'] = round(context['grand_total_r1'], 2)
            context['can_submit'] = HelperFunctions.can_submit_ro2(None, file)
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()

            return render(request, 'html/r2/staff/staff-review-master.html', context)

    @login_required(login_url='/login/')
    def staff_review_save(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'staff-review-all'
            context['key_total'] = 0
            context['key_params'] = []
            for i in range(file.key_parameter_count):
                context['key_total'] += float(list(file.key_parameter.all())[i].marks.ro2)
                context['key_params'].append(list(file.key_parameter.all())[i])
            context['key_total_r1'] = 0
            context['key_params_r1'] = []
            for i in range(file.key_parameter_count):
                context['key_total_r1'] += float(list(file.key_parameter.all())[i].marks.ro1)
                context['key_params_r1'].append(list(file.key_parameter.all())[i])
            context['major_total'] = 0
            context['major_params'] = []
            for i in range(file.major_parameter_count):
                context['major_total'] += float(list(file.major_parameter.all())[i].marks.ro2)
                context['major_params'].append(list(file.major_parameter.all())[i])
            context['major_total_r1'] = 0
            context['major_params_r1'] = []
            for i in range(file.major_parameter_count):
                context['major_total_r1'] += float(list(file.major_parameter.all())[i].marks.ro1)
                context['major_params_r1'].append(list(file.major_parameter.all())[i])
            context['minor_total'] = 0
            context['minor_params'] = []
            for i in range(file.minor_parameter_count):
                context['minor_total'] += float(list(file.minor_parameter.all())[i].marks.ro2)
                context['minor_params'].append(list(file.minor_parameter.all())[i])
            context['minor_total_r1'] = 0
            context['minor_params_r1'] = []
            for i in range(file.minor_parameter_count):
                context['minor_total_r1'] += float(list(file.minor_parameter.all())[i].marks.ro1)
                context['minor_params_r1'].append(list(file.minor_parameter.all())[i])

            context['self_development_total'] = 0
            for i in file.self_development_parameter.all():
                if not i.marks:
                    i.marks = MarkField()
                    i.marks.save()
                context['self_development_total'] += float(i.marks.ro2)
            context['self_development_total_r1'] = 0
            for i in file.self_development_parameter.all():
                if not i.marks:
                    i.marks = MarkField()
                    i.marks.save()
                context['self_development_total_r1'] += float(i.marks.ro1)
            context['self_development_total'] = round(context['self_development_total'], 2)
            context['self_development_total_r1'] = round(context['self_development_total_r1'], 2)
            context['section_1_total'] = context['key_total'] + context['major_total'] + context['minor_total']
            context['section_1_total_r1'] = context['key_total_r1'] + context['major_total_r1'] + context['minor_total_r1']
            if file.training_taken:
                context['section_1_total'] += context['self_development_total']
                context['section_1_total_r1'] += context['self_development_total_r1']

            if file.other_activities_parameter_available:
                context['section_1_total'] += file.other_activities_parameter_marks.ro2
                context['section_1_total_r1'] += file.other_activities_parameter_marks.ro1

            context['section_2_total'] = file.teamwork_marks_total.ro2 + \
                                         file.quality_of_work_marks_total.ro2 + \
                                         file.key_skills_marks_total.ro2 + \
                                         file.domain_expertise_marks_total.ro2 + \
                                         file.productivity_marks_total.ro2
            context['section_2_total_r1'] = file.teamwork_marks_total.ro1 + \
                                            file.quality_of_work_marks_total.ro1 + \
                                            file.key_skills_marks_total.ro1 + \
                                            file.domain_expertise_marks_total.ro1 + \
                                            file.productivity_marks_total.ro1

            context['grand_total'] = context['section_1_total'] + context['section_2_total']
            context['grand_total_r1'] = context['section_1_total_r1'] + context['section_2_total_r1']
            if file.disciplinary_action_ro2:
                context['grand_total'] -= context['config'].disciplinary_action_deductable
            if file.disciplinary_action:
                context['grand_total_r1'] -= context['config'].disciplinary_action_deductable
            if file.was_mooc_completed:
                context['grand_total'] += file.mooc_marks_awarded.ro2
                context['grand_total_r1'] += file.mooc_marks_awarded.ro1
            context['section_2_total'] = round(context['section_2_total'], 2)
            context['section_2_total_r1'] = round(context['section_2_total_r1'], 2)
            context['section_1_total'] = round(context['section_1_total'], 2)
            context['section_1_total_r1'] = round(context['section_1_total_r1'], 2)
            context['grand_total'] = round(context['grand_total'], 2)
            context['grand_total_r1'] = round(context['grand_total_r1'], 2)
            context['can_submit'] = HelperFunctions.can_submit_ro2(None, file)
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()

            return render(request, 'html/r2/staff/staff-review-save.html', context)

    @login_required(login_url='/login/')
    def staff_final_submit(request, pk):
        if request.method == 'GET':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'staff-review-all'
            context['key_total'] = 0
            context['key_params'] = []
            for i in range(file.key_parameter_count):
                context['key_total'] += float(list(file.key_parameter.all())[i].marks.ro2)
                context['key_params'].append(list(file.key_parameter.all())[i])
            context['key_total_r1'] = 0
            context['key_params_r1'] = []
            for i in range(file.key_parameter_count):
                context['key_total_r1'] += float(list(file.key_parameter.all())[i].marks.ro1)
                context['key_params_r1'].append(list(file.key_parameter.all())[i])
            context['major_total'] = 0
            context['major_params'] = []
            for i in range(file.major_parameter_count):
                context['major_total'] += float(list(file.major_parameter.all())[i].marks.ro2)
                context['major_params'].append(list(file.major_parameter.all())[i])
            context['major_total_r1'] = 0
            context['major_params_r1'] = []
            for i in range(file.major_parameter_count):
                context['major_total_r1'] += float(list(file.major_parameter.all())[i].marks.ro1)
                context['major_params_r1'].append(list(file.major_parameter.all())[i])
            context['minor_total'] = 0
            context['minor_params'] = []
            for i in range(file.minor_parameter_count):
                context['minor_total'] += float(list(file.minor_parameter.all())[i].marks.ro2)
                context['minor_params'].append(list(file.minor_parameter.all())[i])
            context['minor_total_r1'] = 0
            context['minor_params_r1'] = []
            for i in range(file.minor_parameter_count):
                context['minor_total_r1'] += float(list(file.minor_parameter.all())[i].marks.ro1)
                context['minor_params_r1'].append(list(file.minor_parameter.all())[i])

            context['self_development_total'] = 0
            for i in file.self_development_parameter.all():
                if not i.marks:
                    i.marks = MarkField()
                    i.marks.save()
                context['self_development_total'] += float(i.marks.ro2)
            context['self_development_total_r1'] = 0
            for i in file.self_development_parameter.all():
                if not i.marks:
                    i.marks = MarkField()
                    i.marks.save()
                context['self_development_total_r1'] += float(i.marks.ro1)
            context['self_development_total'] = round(context['self_development_total'], 2)
            context['self_development_total_r1'] = round(context['self_development_total_r1'], 2)
            context['section_1_total'] = context['key_total'] + context['major_total'] + context['minor_total']
            context['section_1_total_r1'] = context['key_total_r1'] + context['major_total_r1'] + context['minor_total_r1']
            if file.training_taken:
                context['section_1_total'] += context['self_development_total']
                context['section_1_total_r1'] += context['self_development_total_r1']

            if file.other_activities_parameter_available:
                context['section_1_total'] += file.other_activities_parameter_marks.ro2
                context['section_1_total_r1'] += file.other_activities_parameter_marks.ro1

            context['section_2_total'] = file.teamwork_marks_total.ro2 + \
                                         file.quality_of_work_marks_total.ro2 + \
                                         file.key_skills_marks_total.ro2 + \
                                         file.domain_expertise_marks_total.ro2 + \
                                         file.productivity_marks_total.ro2
            context['section_2_total_r1'] = file.teamwork_marks_total.ro1 + \
                                            file.quality_of_work_marks_total.ro1 + \
                                            file.key_skills_marks_total.ro1 + \
                                            file.domain_expertise_marks_total.ro1 + \
                                            file.productivity_marks_total.ro1

            context['grand_total'] = context['section_1_total'] + context['section_2_total']
            context['grand_total_r1'] = context['section_1_total_r1'] + context['section_2_total_r1']
            if file.disciplinary_action_ro2:
                context['grand_total'] -= context['config'].disciplinary_action_deductable
            if file.disciplinary_action:
                context['grand_total_r1'] -= context['config'].disciplinary_action_deductable
            if file.was_mooc_completed:
                context['grand_total'] += file.mooc_marks_awarded.ro2
                context['grand_total_r1'] += file.mooc_marks_awarded.ro1
            context['section_2_total'] = round(context['section_2_total'], 2)
            context['section_2_total_r1'] = round(context['section_2_total_r1'], 2)
            context['section_1_total'] = round(context['section_1_total'], 2)
            context['section_1_total_r1'] = round(context['section_1_total_r1'], 2)
            context['grand_total'] = round(context['grand_total'], 2)
            context['grand_total_r1'] = round(context['grand_total_r1'], 2)
            context['can_submit'] = HelperFunctions.can_submit_ro2(None, file)

            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            context['grade'] = GradeConfiguration.objects.filter(is_active=True).first().get_grade(context['grand_total'])

            return render(request, 'html/r2/staff/final-submit.html', context)
        if request.method == 'POST':
            if HelperFunctions.check_if_ro2_is_authorized(None, request, pk):
                pass
            else:
                context = {
                    'error_code': "Unauthorized Error",
                    "error_message": "You are not authorized to view this page."
                }
                return render(request, "html/error_pages/pages-error.html", context)
            try:
                file = StaffAppraisalFile.objects.get(user=User.objects.get(id=pk))
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'staff-final-submit'
            context['key_total'] = 0
            context['key_params'] = []
            for i in range(file.key_parameter_count):
                context['key_total'] += float(list(file.key_parameter.all())[i].marks.ro2)
                context['key_params'].append(list(file.key_parameter.all())[i])
            context['major_total'] = 0
            context['major_params'] = []
            for i in range(file.major_parameter_count):
                context['major_total'] += float(list(file.major_parameter.all())[i].marks.ro2)
                context['major_params'].append(list(file.major_parameter.all())[i])
            context['minor_total'] = 0
            context['minor_params'] = []
            for i in range(file.minor_parameter_count):
                context['minor_total'] += float(list(file.minor_parameter.all())[i].marks.ro2)
                context['minor_params'].append(list(file.minor_parameter.all())[i])

            context['self_development_total'] = 0
            for i in file.self_development_parameter.all():
                if not i.marks:
                    i.marks = MarkField()
                    i.marks.save()
                context['self_development_total'] += float(i.marks.ro2)

            context['section_1_total'] = context['key_total'] + context['major_total'] + context['minor_total']
            if file.training_taken:
                context['section_1_total'] += context['self_development_total']
            if file.other_activities_parameter_available:
                context['section_1_total'] += file.other_activities_parameter_marks.ro2

            context['section_2_total'] = file.teamwork_marks_total.ro2 + \
                                         file.quality_of_work_marks_total.ro2 + \
                                         file.key_skills_marks_total.ro2 + \
                                         file.domain_expertise_marks_total.ro2 + \
                                         file.productivity_marks_total.ro2
            context['grand_total'] = context['section_1_total'] + context['section_2_total']
            if file.disciplinary_action:
                context['grand_total'] -= context['config'].disciplinary_action_deductable
            if file.was_mooc_completed:
                context['grand_total'] += file.mooc_marks_awarded.ro2
            context['section_2_total'] = round(context['section_2_total'], 2)
            context['section_1_total'] = round(context['section_1_total'], 2)
            context['grand_total'] = round(context['grand_total'], 2)

            file.file_level = "HR"
            file.file_with = file.user.ro2_id
            file.ro2_grading_done = True
            if not file.total_marks:
                file.total_marks = MarkField()
                file.total_marks.save()
            file.total_marks.ro2 = context['grand_total']
            file.total_marks.save()
            file.grade_received_ro2 = GradeConfiguration.objects.filter(is_active=True).first().get_grade(context['grand_total'])
            file.save()
            return JsonResponse({'success': True})

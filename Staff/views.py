import json
import os
from datetime import datetime as dt

from django.contrib.auth.decorators import *
from django.http import *
from django.shortcuts import render

from MasterConfiguration.models import *
# from datetime import date
from RO1.views import HelperFunctions
from .models import *


# api views for staff-appraisal related stuff

class StaffViewSet:
    @staticmethod
    @login_required(login_url='/login/')
    def dashboard(request):
        StaffHelperFunctions.check_authorized_user(request)
        if request.method == 'GET':
            # check if any parameter is not approved
            if request.user.roles == 'stf':
                try:
                    file = StaffAppraisalFile.objects.get(user=request.user)
                except StaffAppraisalFile.DoesNotExist:
                    year = dt.now().year
                    file = StaffAppraisalFile.create(year, request.user)
                    file.save()
                context = {}
                context['file'] = file
                context['config'] = StaffConfiguration.objects.get(name='master')
                context['pagename'] = 'staff-dashboard'

                try:
                    cycle = StaffAppraisalCycleConfiguration.objects.filter(is_active=True).first()
                    date_today = CurrentDate.objects.first().get_date()
                    if cycle:
                        if cycle.parameter_approval_start_date <= date_today <= cycle.parameter_approval_end_date:
                            context['time_left'] = cycle.parameter_approval_end_date - date_today
                            context['time_left'] = context['time_left'].days
                            context['total_time'] = cycle.parameter_approval_end_date - cycle.parameter_approval_start_date
                            context['total_time'] = context['total_time'].days
                        elif cycle.appraisal_start_date <= date_today <= cycle.appraisal_end_date:
                            context['time_left'] = cycle.appraisal_end_date - date_today
                            context['time_left'] = context['time_left'].days
                            context['total_time'] = cycle.appraisal_end_date - cycle.appraisal_start_date
                            context['total_time'] = context['total_time'].days

                        elif cycle.r1_approval_start_date <= date_today <= cycle.r1_approval_end_date:
                            context['time_left'] = cycle.r1_approval_end_date - date_today
                            context['time_left'] = context['time_left'].days
                            context['total_time'] = cycle.r1_approval_end_date - cycle.r1_approval_start_date
                            context['total_time'] = context['total_time'].days

                        elif cycle.r2_approval_start_date <= date_today <= cycle.r2_approval_end_date:
                            context['time_left'] = cycle.r2_approval_end_date - date_today
                            context['time_left'] = context['time_left'].days
                            context['total_time'] = cycle.r2_approval_end_date - cycle.r2_approval_start_date
                            context['total_time'] = context['total_time'].days

                    context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
                    context['can_show_result'] = StaffHelperFunctions.can_show_result()
                except StaffAppraisalCycleConfiguration.DoesNotExist:
                    pass
                return render(request, 'html/staff/staff-dashboard.html', context)
            else:
                context = {}
                context['error_code'] = "Forbidden! Unauthorized Access"
                context['error_message'] = "You are a staff member. You are not allowed to access this page."
                return render(request, 'html/error_pages/pages-error.html', context)

    # @login_required(login_url='/login/')
    # def profile(request):
    #     if request.method == 'GET':
    #         # check if any parameter is not approved
    #         if request.user.roles == 'stf':
    #             try:
    #                 file = StaffAppraisalFile.objects.get(user=request.user)
    #             except StaffAppraisalFile.DoesNotExist:
    #                 year = datetime.now().year
    #                 file = StaffAppraisalFile.create(year, request.user)
    #                 file.save()
    #             context = {}
    #             context['file'] = file
    #             context['config'] = StaffConfiguration.objects.get(name='master')
    #             context['pagename'] = 'staff-profile'
    #             return render(request, 'html/staff/staff-profile.html', context)
    #         else:
    #             context = {}
    #             context['error_code'] = "Forbidden! Unauthorized Access"
    #             context['error_message'] = "You are a staff member. You are not allowed to access this page."
    #             return render(request, 'html/error_pages/pages-error.html', context)

    @staticmethod
    @login_required(login_url='/login/')
    def status(request):
        StaffHelperFunctions.check_authorized_user(request)
        if request.method == 'GET':
            # check if any parameter is not approved
            if request.user.roles == 'stf':
                try:
                    file = StaffAppraisalFile.objects.get(user=request.user)
                except StaffAppraisalFile.DoesNotExist:
                    year = datetime.now().year
                    file = StaffAppraisalFile.create(year, request.user)
                    file.save()
                context = {}
                context['file'] = file
                context['config'] = StaffConfiguration.objects.get(name='master')
                context['pagename'] = 'staff-appraisal-status'
                context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
                context['can_show_result'] = StaffHelperFunctions.can_show_result()
                return render(request, 'html/staff/staff-status.html', context)
            else:
                context = {}
                context['error_code'] = "Forbidden! Unauthorized Access"
                context['error_message'] = "You are a staff member. You are not allowed to access this page."
                return render(request, 'html/error_pages/pages-error.html', context)

    @staticmethod
    @login_required(login_url='/login/')
    def upload_mooc(request):
        StaffHelperFunctions.check_authorized_user(request)
        if request.method == 'POST' and not request.user.is_anonymous:
            file = request.FILES['file']
            staff_file = StaffAppraisalFile.objects.get(user=request.user)
            f = staff_file.mooc_file.file
            if f is not None:
                try:
                    path = f.path
                    if os.path.isfile(path):
                        os.remove(path)
                except ValueError as e:
                    pass

            staff_file.mooc_file.file = file
            staff_file.mooc_file.user = request.user
            staff_file.mooc_file.filename = file.name
            staff_file.mooc_file.save()
            staff_file.was_mooc_completed = True
            staff_file.save()

            response = {'status': 'success', 'filename': file.name, 'file_url': staff_file.mooc_file.file.url}
            return JsonResponse(json.dumps(response), safe=False)
        else:
            HttpResponse("error")

    @staticmethod
    @login_required(login_url='/login/')
    def delete_certification(request):
        StaffHelperFunctions.check_authorized_user(request)

        if request.method == 'POST':
            data = dict(request.POST)

            id = int(data['file_id'][0])
            file = StaffAppraisalFile.objects.get(user=request.user)
            cert = file.self_development_parameter.get(id=id)
            if cert.file is not None:
                f = cert.file
                if f.file:
                    path = f.file.path
                    if os.path.isfile(path):
                        os.remove(path)
                f.delete()
            cert.delete()
            file.self_development_parameter_count -= 1
            file.save()
            return HttpResponse("success")

    @staticmethod
    @login_required(login_url='/login/')
    def upload_certifications(request):
        StaffHelperFunctions.check_authorized_user(request)
        if request.method == 'POST' and not request.user.is_anonymous:
            files = dict(request.FILES)
            data = dict(request.POST)
            ret = []
            my_data = []
            file = StaffAppraisalFile.objects.get(user=request.user)
            file.training_taken = True
            for i in range(len(files['file'])):
                var = {}
                var['file'] = files['file'][i]
                var['name'] = data['name'][i]
                var['filename'] = files['file'][i].name
                my_data.append(var)

            for i in my_data:
                cert = Certificate()
                cert.name = i['name']
                f = File()
                f.file = i['file']
                f.filename = i['filename']
                f.user = request.user
                f.save()
                cert.file = f
                cert.is_file = True
                cert.is_mooc = False
                cert.save()
                file.self_development_parameter.add(cert)
                file.self_development_parameter_count += 1
                tmp = {}
                tmp['filename'] = i['filename']
                tmp['name'] = i['name']
                tmp['url'] = f.file.url
                tmp['id'] = cert.id
                ret.append(tmp)

            file.save()

            return JsonResponse(json.dumps(ret), safe=False)

    @staticmethod
    @login_required(login_url='/login/')
    def staff_show(request):
        StaffHelperFunctions.check_authorized_user(request)
        user = request.user
        if user.is_anonymous:
            return HttpResponseRedirect('/login/')

        if user.roles != 'stf':
            # throw forbidden error
            context = {'error_code': 'You are not authorized to view this page',
                       'error_message': 'You are not a staff, So you cant participate in this cycle'}
            return render(request, 'html/error_pages/pages-error.html', context)
        if request.method == 'GET':
            # check if any parameter is not approved
            context = {
                'key_param_validation': {'maxkey': 250, 'maxval': 1000},
                'maj_param_validation': {'maxkey': 250, 'maxval': 1000},
                'min_param_validation': {'maxkey': 250, 'maxval': 1000},
                'general_textbox_max': 1000,
                'can_show_result': StaffHelperFunctions.can_show_result(),
            }

            try:
                file = StaffAppraisalFile.objects.get(user=request.user)
                context['file'] = file
            except StaffAppraisalFile.DoesNotExist:
                year = datetime.now().year
                file = StaffAppraisalFile.create(year, request.user)

            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            if file.file_level == "APPRAISEE" and (context['stage'] == 'not_started' or context['stage'] == 'parameter_approval' or context['stage'] == 'appraisal'):
                if context['stage'] == 'not_started':
                    return render(request, 'html/staff/entry/no-input.html', context)
                if context['stage'] == 'parameter_approval':
                    if file.ro1_validation.is_parameters_approved:
                        return render(request, 'html/staff/entry/no-input.html', context)
                    context['all_parameters_approved'] = file.is_all_parameters_approved
                    context['key_parameter_count'] = file.key_parameter_count
                    context['major_parameter_count'] = file.major_parameter_count
                    context['minor_parameter_count'] = file.minor_parameter_count
                    context['key_parameters'] = []
                    for i in range(file.key_parameter_count):
                        context['key_parameters'].append(file.key_parameter.all()[i])
                    context['major_parameters'] = []
                    for i in range(file.major_parameter_count):
                        context['major_parameters'].append(file.major_parameter.all()[i])
                    context['minor_parameters'] = []
                    for i in range(file.minor_parameter_count):
                        context['minor_parameters'].append(file.minor_parameter.all()[i])

                    # Configuration
                    config = StaffConfiguration.objects.get(name="master")
                    context['max_key_allowed'] = config.max_key_parameter
                    context['max_major_allowed'] = config.max_major_parameter
                    context['max_minor_allowed'] = config.max_minor_parameter

                    context['config'] = StaffConfiguration.objects.get(name="master")
                    context['pagename'] = 'staff-appraisal-form'

                    return render(request, 'html/staff/entry/approval-entry.html', context)
                else:
                    # when all parameters are approved
                    context['all_parameters_approved'] = file.is_all_parameters_approved
                    context['key_parameter_count'] = file.key_parameter_count
                    context['major_parameter_count'] = file.major_parameter_count
                    context['minor_parameter_count'] = file.minor_parameter_count
                    context['key_parameters'] = []
                    for i in range(file.key_parameter_count):
                        context['key_parameters'].append(file.key_parameter.all()[i])
                    context['major_parameters'] = []
                    for i in range(file.major_parameter_count):
                        context['major_parameters'].append(file.major_parameter.all()[i])
                    context['minor_parameters'] = []
                    for i in range(file.minor_parameter_count):
                        context['minor_parameters'].append(file.minor_parameter.all()[i])

                    # Configuration
                    config = StaffConfiguration.objects.get(name="master")
                    context['max_key_allowed'] = config.max_key_parameter
                    context['max_major_allowed'] = config.max_major_parameter
                    context['max_minor_allowed'] = config.max_minor_parameter
                    context['config'] = StaffConfiguration.objects.get(name="master")
                    context['pagename'] = 'staff-appraisal-form'
                    return render(request, 'html/staff/entry/main-entry.html', context)
            if context['stage'] == 'r1_approval':
                context['config'] = StaffConfiguration.objects.get(name="master")
                context['pagename'] = 'staff-appraisal-form'
                return render(request, 'html/staff/entry/no-input.html', context)
            if context['stage'] == 'r2_approval':
                context['config'] = StaffConfiguration.objects.get(name="master")
                context['pagename'] = 'staff-appraisal-form'
                return render(request, 'html/staff/entry/no-input.html', context)
            if context['stage'] == 'completed':
                context['config'] = StaffConfiguration.objects.get(name="master")
                context['pagename'] = 'staff-appraisal-form'
                return render(request, 'html/staff/entry/no-input.html', context)
            else:
                return render(request, 'html/staff/entry/no-input.html', context)

    @staticmethod
    @login_required(login_url='/login/')
    def staff_show_old(request):
        StaffHelperFunctions.check_authorized_user(request)
        user = request.user
        if user.is_anonymous:
            return HttpResponseRedirect('/login/')

        if user.roles != 'stf':
            # throw forbidden error
            context = {'error_code': 'You are not authorized to view this page',
                       'error_message': 'You are not a staff, So you cant participate in this cycle'}
            return render(request, 'html/error_pages/pages-error.html', context)
        if request.method == 'GET':
            # check if any parameter is not approved
            context = {
                'key_param_validation': {'maxkey': 500, 'maxval': 2000},
                'maj_param_validation': {'maxkey': 350, 'maxval': 1500},
                'min_param_validation': {'maxkey': 300, 'maxval': 1000},
                'can_show_result': StaffHelperFunctions.can_show_result(),
            }

            try:
                file = StaffAppraisalFile.objects.get(user=request.user)
            except StaffAppraisalFile.DoesNotExist:
                year = datetime.now().year
                file = StaffAppraisalFile.create(year, request.user)

            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            if file.file_level == "APPRAISEE":
                if not file.is_all_parameters_approved:
                    context['all_parameters_approved'] = file.is_all_parameters_approved
                    context['key_parameter_count'] = file.key_parameter_count
                    context['major_parameter_count'] = file.major_parameter_count
                    context['minor_parameter_count'] = file.minor_parameter_count
                    context['key_parameters'] = []
                    for i in range(file.key_parameter_count):
                        context['key_parameters'].append(file.key_parameter.all()[i])
                    context['major_parameters'] = []
                    for i in range(file.major_parameter_count):
                        context['major_parameters'].append(file.major_parameter.all()[i])
                    context['minor_parameters'] = []
                    for i in range(file.minor_parameter_count):
                        context['minor_parameters'].append(file.minor_parameter.all()[i])

                    # Configuration
                    config = StaffConfiguration.objects.get(name="master")
                    context['max_key_allowed'] = config.max_key_parameter
                    context['max_major_allowed'] = config.max_major_parameter
                    context['max_minor_allowed'] = config.max_minor_parameter

                    context['file'] = file
                    context['config'] = StaffConfiguration.objects.get(name="master")
                    context['pagename'] = 'staff-appraisal-form'

                    return render(request, 'html/staff/staff-entry.html', context)
                else:
                    # when all parameters are approved
                    context['all_parameters_approved'] = file.is_all_parameters_approved
                    context['key_parameter_count'] = file.key_parameter_count
                    context['major_parameter_count'] = file.major_parameter_count
                    context['minor_parameter_count'] = file.minor_parameter_count
                    context['key_parameters'] = []
                    for i in range(file.key_parameter_count):
                        context['key_parameters'].append(file.key_parameter.all()[i])
                    context['major_parameters'] = []
                    for i in range(file.major_parameter_count):
                        context['major_parameters'].append(file.major_parameter.all()[i])
                    context['minor_parameters'] = []
                    for i in range(file.minor_parameter_count):
                        context['minor_parameters'].append(file.minor_parameter.all()[i])

                    # Configuration
                    config = StaffConfiguration.objects.get(name="master")
                    context['max_key_allowed'] = config.max_key_parameter
                    context['max_major_allowed'] = config.max_major_parameter
                    context['max_minor_allowed'] = config.max_minor_parameter
                    context['config'] = StaffConfiguration.objects.get(name="master")
                    context['file'] = file
                    context['pagename'] = 'staff-appraisal-form'
                    return render(request, 'html/staff/staff-entry.html', context)
            elif file.file_level == "RO1":
                context = {'config': StaffConfiguration.objects.get(name="master"), 'file': file, 'pagename': 'staff-appraisal-form'}
                return render(request, 'html/staff/staff-entry.html', context)
            elif file.file_level == "RO2":
                context = {'config': StaffConfiguration.objects.get(name="master"), 'file': file, 'pagename': 'staff-appraisal-form'}
                return render(request, 'html/staff/staff-entry.html', context)
            elif file.file_level == "HR":
                context = {'config': StaffConfiguration.objects.get(name="master"), 'file': file, 'pagename': 'staff-appraisal-form'}
                return render(request, 'html/staff/staff-entry.html', context)

    @staticmethod
    @login_required(login_url='/login/')
    def staff_entry(request):
        StaffHelperFunctions.check_authorized_user(request)
        if request.user.roles != 'stf':
            #
            # throw forbidden error
            return HttpResponseForbidden()
        if request.method == 'POST':

            if request.headers['phase'] == "Phase 1":

                # create a new staff appraisal file
                try:
                    file = StaffAppraisalFile.objects.get(user=request.user)
                except StaffAppraisalFile.DoesNotExist:
                    file = None
                if file is None:
                    # get current year as int
                    year = datetime.now().year
                    file = StaffAppraisalFile.create(year=year, user=request.user)
                    file.save()

                # check if all parameters are not approved
                if file.file_level == 'APPRAISEE':

                    # It will enter here only if
                    #   1. Parameters are not submitted
                    #   2. Parameters are submitted but not approved by ro and returned to appraisee, so need to edit
                    #   3. Parameters are submitted and approved by RO, now appraisee, fills rest details.

                    # check if parameters are approved by RO

                    if not file.is_all_parameters_approved:

                        # Only working with parameters CASE 1
                        data = json.loads(request.POST['json'])
                        file.key_parameter_count = data['key_parameter_count']
                        file.major_parameter_count = data['major_parameter_count']
                        file.minor_parameter_count = data['minor_parameter_count']
                        for i in file.key_parameter.all():
                            print(i.parameter_index)
                        cancelled = data['cancelled_parameters']
                        for i in cancelled['key']:
                            try:
                                deletable = file.key_parameter.all().get(id=int(i))
                                file.key_parameter.remove(deletable)
                                file.cancelled_parameters.add(deletable)
                                m = MarkField()
                                m.save()
                                p = Parameter(parameter_index=deletable.parameter_index)
                                p.save()
                                file.key_parameter.add(p)
                            except Exception:
                                return HttpResponse("Parameter does not exist")

                        for i in cancelled['major']:
                            try:
                                deletable = file.major_parameter.all().get(id=int(i))
                                file.major_parameter.remove(deletable)
                                file.cancelled_parameters.add(deletable)
                                m = MarkField()
                                m.save()
                                p = Parameter(parameter_index=deletable.parameter_index)
                                p.save()
                                file.major_parameter.add(p)
                            except Exception:
                                return HttpResponse("Parameter does not exist")
                        for i in cancelled['minor']:
                            try:
                                deletable = file.minor_parameter.all().get(id=int(i))
                                file.minor_parameter.remove(deletable)
                                file.cancelled_parameters.add(deletable)
                                m = MarkField()
                                m.save()
                                p = Parameter(parameter_index=deletable.parameter_index)
                                p.marks = m
                                p.save()
                                file.minor_parameter.add(p)
                            except Exception:
                                return HttpResponse("Parameter does not exist")
                        file.save()
                        for i in file.key_parameter.all():
                            print('-', i.parameter_index)
                        for i in file.key_parameter.all():
                            i.name = ""
                            i.save()
                        for i in file.major_parameter.all():
                            i.name = ""
                            i.save()
                        for i in file.minor_parameter.all():
                            i.name = ""
                            i.save()

                        for i in range(file.key_parameter_count):
                            # try:
                            parameter = list(file.key_parameter.all())[i]
                            # except Parameter.DoesNotExist:
                            #     parameter = Parameter()
                            #     parameter.parameter_index = i + 1

                            parameter.name = data['key_parameters'][i]
                            parameter.save()
                        for i in range(file.major_parameter_count):
                            # try:
                            parameter = list(file.major_parameter.all())[i]
                            # except Parameter.DoesNotExist:
                            #     parameter = Parameter()
                            #     parameter.parameter_index = i + 1
                            parameter.name = data['major_parameters'][i]
                            parameter.save()
                        for i in range(file.minor_parameter_count):
                            # try:
                            parameter = list(file.minor_parameter.all())[i]
                            # except Parameter.DoesNotExist:
                            #     parameter = Parameter()
                            #     parameter.parameter_index = i + 1
                            parameter.name = data['minor_parameters'][i]
                            parameter.save()
                        if data['is_submit']:
                            file.file_level = "RO1"
                            file.file_with = file.user.ro1_id
                        file.save()
                        return HttpResponse("Parameters Saved")
                # convert file object to json and display it in web response body
            else:  # Phase 2
                try:
                    file = StaffAppraisalFile.objects.get(user=request.user)
                except StaffAppraisalFile.DoesNotExist:
                    file = None
                if file is None:
                    return HttpResponseForbidden("File not found")
                    # check if all parameters are not approved
                if file.file_level == 'APPRAISEE':

                    #   3. Parameters are submitted and approved by RO, now appraisee, fills rest details.

                    data = json.loads(request.POST['json'])
                    if file.is_all_parameters_approved:

                        file.key_parameter_count = data['key_parameter_count']
                        file.major_parameter_count = data['major_parameter_count']
                        file.minor_parameter_count = data['minor_parameter_count']
                        key_params = data['key_parameters']
                        major_params = data['major_parameters']
                        minor_params = data['minor_parameters']
                        saved_key_params = file.key_parameter.all()
                        saved_major_params = file.major_parameter.all()
                        saved_minor_params = file.minor_parameter.all()
                        file.save()
                        for i in range(file.key_parameter_count):
                            param = list(saved_key_params)[i]

                            param.name = list(key_params[i].keys())[0]
                            param.value = list(key_params[i].values())[0]

                            param.save()
                        for i in range(file.major_parameter_count):
                            param = list(saved_major_params)[i]

                            param.name = list(major_params[i].keys())[0]
                            param.value = list(major_params[i].values())[0]

                            param.save()
                        for i in range(file.minor_parameter_count):
                            param = list(saved_minor_params)[i]

                            param.name = list(minor_params[i].keys())[0]
                            param.value = list(minor_params[i].values())[0]

                            param.save()
                        file.save()
                        # self development

                        # file.was_mooc_completed = data['mooc_completed']
                        if data['mooc_completed']:
                            file.mooc_description = data['mooc_description']
                        else:
                            file.was_mooc_completed = False
                            file.mooc_file.file = None
                            file.mooc_file.save()
                            file.mooc_description = ''
                            file.save()
                        file.other_activities_parameter_available = data['other_activities_completed']
                        if data['other_activities_completed']:
                            file.other_activities_parameter = data['other_activities_data']
                        file.save()
                        # self evaluation
                        self_eval = data['self_eval']

                        file.key_highlights = self_eval['key_highlights']
                        file.challenges = self_eval['challenges']
                        file.areas_of_improvement = self_eval['areas_of_improvement']
                        file.areas_of_strength = self_eval['areas_of_strength']
                        file.save()
                        if data['training_taken']:
                            if file.self_development_parameter_count > 0:
                                file.training_taken = data['training_taken']
                            else:
                                file.training_taken = 0
                        file.save()

                        if not file.training_taken:
                            file.self_development_parameter.all().delete()
                            file.self_development_parameter_count = 0
                        file.save()

                    if data["is_submit"]:
                        file.file_level = 'RO1'
                        file.file_with = file.user.ro1_id
                        file.save()
                        # REDIRECT TO HOME PAGE
                        return HttpResponse("Submitted")
                    return HttpResponse("Saved")
        else:
            return HttpResponse('failed')

    @staticmethod
    @login_required(login_url='/login/')
    def staff_result(request):
        if request.method == 'GET':
            StaffHelperFunctions.check_authorized_user(request)
            try:
                file = StaffAppraisalFile.objects.get(user=request.user)
            except StaffAppraisalFile.DoesNotExist:
                return HttpResponse('No file found')
            # if file.file_level == "RO2":
            context = {}
            context['file'] = file
            context['config'] = StaffConfiguration.objects.get(name='master')
            context['pagename'] = 'staff-result'
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
            context['section_1_total_r1'] = context['key_total_r1'] + context['major_total_r1'] + context[
                'minor_total_r1']
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
            context['can_show_result'] = StaffHelperFunctions.can_show_result()
            context['cycle'], context['stage'], context['today'] = HelperFunctions.get_cycles()
            context['grade'] = GradeConfiguration.objects.filter(is_active=True).first().get_grade(
                context['grand_total'])

            return render(request, 'html/staff/staff-result.html', context)


class StaffHelperFunctions:
    @staticmethod
    def check_authorized_user(request):
        print(request.user.roles)
        if request.user.is_authenticated and request.user.is_active and StaffAppraisalCycleInclusion.check_inclusion(request.user):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

    @staticmethod
    def can_show_result():
        obj = ShowResult.objects.first()
        return obj.show_result

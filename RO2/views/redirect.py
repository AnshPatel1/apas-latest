from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from MasterConfiguration.models import *
from Account.models import User
from Faculty.FacultyFOET.models import *
from MasterConfiguration.models import *


class RO2FacultyRedirectViewSet:
    @staticmethod
    @login_required(login_url='/login/')
    def redirect(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        category = FacultyHelperFunctions.get_inclusion(pk)
        if category is None:
            return HttpResponseRedirect("Please contact admin. This user is not included in any cycle inclusion.")
        elif category == "SOT":
            return HttpResponseRedirect(reverse('ro2-faculty-foet-faculty-home', kwargs={'pk': pk}))
        elif category == "SLS":
            return HttpResponseRedirect(reverse('ro2-faculty-fols-faculty-home', kwargs={'pk': pk}))
        elif category == "SPM":
            return HttpResponseRedirect(reverse('ro2-faculty-foem-faculty-home', kwargs={'pk': pk}))
        elif category == "MATH":
            return HttpResponseRedirect(reverse('ro2-faculty-maths-faculty-home', kwargs={'pk': pk}))
        elif category == "SCIENCE":
            return HttpResponseRedirect(reverse('ro2-faculty-science-faculty-home', kwargs={'pk': pk}))
        else:
            return HttpResponseRedirect("Please contact admin. This user is not included in any cycle inclusion.")


class FacultyHelperFunctions:
    @staticmethod
    def check_if_ro2_is_authorized(request, appraisee_id):
        try:
            user = User.objects.get(id=appraisee_id)
            ro_user = request.user
        except Model.DoesNotExist:
            return False

        if user.ro2_id.id == ro_user.id:
            return True
        else:
            return False

    @staticmethod
    def get_inclusion(user):
        user = User.objects.get(id=user)
        try:
            if SOTFacultyAppraisalCycleInclusion.check_inclusion(user):
                return "SOT"
            elif SLSFacultyAppraisalCycleInclusion.check_inclusion(user):
                return "SLS"
            elif SPMFacultyAppraisalCycleInclusion.check_inclusion(user):
                return "SPM"
            elif MathFacultyAppraisalCycleInclusion.check_inclusion(user):
                return "MATH"
            elif ScienceFacultyAppraisalCycleInclusion.check_inclusion(user):
                return "SCIENCE"
            else:
                return None
        except SOTFacultyAppraisalCycleInclusion.DoesNotExist:
            raise Http404("Cycles does not exist")
        except SLSFacultyAppraisalCycleInclusion.DoesNotExist:
            raise Http404("Cycles does not exist")
        except SPMFacultyAppraisalCycleInclusion.DoesNotExist:
            raise Http404("Cycles does not exist")
        except MathFacultyAppraisalCycleInclusion.DoesNotExist:
            raise Http404("Cycles does not exist")
        except ScienceFacultyAppraisalCycleInclusion.DoesNotExist:
            raise Http404("Cycles does not exist")

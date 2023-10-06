from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse

from Account.models import *
from MasterConfiguration.models import *
import csv


class FacultyRedirectViewSet:
    @staticmethod
    @login_required(login_url='/login/')
    def redirect(request):

        category = FacultyHelperFunctions.get_inclusion(request.user)
        if category is None:
            return HttpResponseRedirect("Please contact admin. This user is not included in any cycle inclusion.")
        elif category == "SOT":
            return HttpResponseRedirect("sot/")
        elif category == "SLS":
            return HttpResponseRedirect("sls/")
        elif category == "SPM":
            return HttpResponseRedirect("soem/")
        elif category == "MATH":
            return HttpResponseRedirect("maths/")
        elif category == "SCIENCE":
            return HttpResponseRedirect("science/")
        else:
            return HttpResponseRedirect("Please contact admin. This user is not included in any cycle inclusion.")


class FacultyHelperFunctions:
    @staticmethod
    def get_inclusion(user):
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
            elif StaffAppraisalCycleInclusion.check_inclusion(user):
                return "STAFF"
            else:
                return None
        except SOTFacultyAppraisalCycleInclusion.DoesNotExist or SLSFacultyAppraisalCycleInclusion.DoesNotExist or SPMFacultyAppraisalCycleInclusion.DoesNotExist or MathFacultyAppraisalCycleInclusion.DoesNotExist or ScienceFacultyAppraisalCycleInclusion.DoesNotExist or StaffAppraisalCycleInclusion.DoesNotExist:
            raise Http404("Cycles does not exist")


from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import Http404, HttpResponse
from django.shortcuts import render
from Faculty.FacultySoEM.models import *
from Account.models import User
from MasterConfiguration.models import *


class RO2FacultyFOEMViewSet:
    @staticmethod
    @login_required(login_url='/login/')
    def dashboard(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)
        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'faculty-home', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        return render(request, "html/r2/faculty/foem/dashboard.html", context)

    @login_required(login_url='/login/')
    def verify_data(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)
        context = {'user': request.user, 'page_name': 'verify-data', 'file': FacultyHelperFunctions.get_file(pk),
                   'cycle': FacultyHelperFunctions.get_cycle()}
        return render(request, "html/r2/faculty/foem/verify-data.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def teaching_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'teaching-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}
        if file.modern_teaching_methods.marks is None:
            file.modern_teaching_methods.marks = MarkField()
            file.modern_teaching_methods.marks.save()
            file.modern_teaching_methods.save()

        if file.exam_duty.marks is None:
            file.exam_duty.marks = MarkField()
            file.exam_duty.marks.save()
            file.exam_duty.save()

        if file.books_and_publications_marks is None:
            file.books_and_publications_marks = MarkField()
            file.books_and_publications_marks.save()
        file.save()

        context['books'] = file.research_books.all().union(file.textbooks.all()).union(file.literary_books.all())

        if request.method == 'POST':
            # entries_text = [value for key, value in dict(request.POST).items() if key.startswith('books-text')]
            # entries_research = [value for key, value in dict(request.POST).items() if key.startswith('books-research')]
            file.modern_teaching_methods.marks.ro2_remarks = request.POST.get('modern-methods-remarks')
            file.modern_teaching_methods.marks.ro2 = float(request.POST.get('modern-methods-marks'))
            if request.POST.get('teaching-methods-action') == 'accept':
                file.modern_teaching_methods.marks.ro2_agreed = True
            if request.POST.get('teaching-methods-action') == 'reject':
                file.modern_teaching_methods.marks.ro2_agreed = False
            file.modern_teaching_methods.marks.save()

            file.upkeep_of_course_files_marks.ro2_remarks = request.POST.get('upkeep-of-course-files-remarks')
            file.upkeep_of_course_files_marks.ro2 = float(request.POST.get('upkeep-of-course-files-marks'))
            if request.POST.get('upkeep-of-course-files-action') == 'accept':
                file.upkeep_of_course_files_marks.ro2_agreed = True
            if request.POST.get('upkeep-of-course-files-action') == 'reject':
                file.upkeep_of_course_files_marks.ro2_agreed = False
            file.upkeep_of_course_files_marks.save()

            file.inclusion_of_alumni_marks.ro2_remarks = request.POST.get('inclusion-of-alumni-remarks')
            file.inclusion_of_alumni_marks.ro2 = float(request.POST.get('inclusion-of-alumni-marks'))
            if request.POST.get('inclusion-of-alumni-action') == 'accept':
                file.inclusion_of_alumni_marks.ro2_agreed = True
            if request.POST.get('inclusion-of-alumni-action') == 'reject':
                file.inclusion_of_alumni_marks.ro2_agreed = False
            file.inclusion_of_alumni_marks.save()

            existing_books = list(file.textbooks.all())
            for i in range(len(existing_books)):
                db_book = existing_books[i]
                if db_book.marks is None:
                    db_book.marks = MarkField()
                # if entries_text[i][1] == 'accept':
                db_book.marks.ro2_agreed = True
                # if entries_text[i][1] == 'reject':
                #     db_book.marks.ro2_agreed = False
                # db_book.marks.ro2_remarks = entries_text[i][0]
                db_book.marks.save()
                db_book.save()

            existing_books = list(file.research_books.all())
            for i in range(len(existing_books)):
                db_book = existing_books[i]
                if db_book.marks is None:
                    db_book.marks = MarkField()
                # if entries_research[i][1] == 'accept':
                db_book.marks.ro2_agreed = True
                # if entries_research[i][1] == 'reject':
                #     db_book.marks.ro2_agreed = False
                # db_book.marks.ro2_remarks = entries_research[i][0]
                db_book.marks.save()
                db_book.save()
            file.save()

            existing_books = list(file.literary_books.all())
            for i in range(len(existing_books)):
                db_book = existing_books[i]
                if db_book.marks is None:
                    db_book.marks = MarkField()
                # if entries_research[i][1] == 'accept':
                db_book.marks.ro2_agreed = True
                # if entries_research[i][1] == 'reject':
                #     db_book.marks.ro2_agreed = False
                # db_book.marks.ro2_remarks = entries_research[i][0]
                db_book.marks.save()
                db_book.save()

            file.ro2_validator.teaching_validated = True
            file.ro2_validator.save()

        return render(request, "html/r2/faculty/foem/teaching.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def research_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'research-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST':
            # papers = [value for key, value in dict(request.POST).items() if key.startswith('papers')]
            db_papers = list(file.publications_in_scopus_wos.all())
            # conferences = [value for key, value in dict(request.POST).items() if key.startswith('conferences')]
            db_conferences = list(file.conference_proceedings_scopus_wos.all())
            # epubs = [value for key, value in dict(request.POST).items() if key.startswith('epubs')]
            db_epubs = list(file.e_publications_articles.all())

            for i in range(len(db_papers)):
                paper = db_papers[i]
                if paper.marks is None:
                    paper.marks = MarkField()

                paper.marks.ro2_agreed = True
                # if papers[i][1] == 'accept':
                # if papers[i][1] == 'reject':
                #     paper.marks.ro2_agreed = False
                # paper.marks.ro2_remarks = papers[i][0]
                paper.marks.save()
                paper.save()

            for i in range(len(db_conferences)):
                conference = db_conferences[i]
                if conference.marks is None:
                    conference.marks = MarkField()

                conference.marks.ro2_agreed = True
                # if conferences[i][1] == 'accept':
                # if conferences[i][1] == 'reject':
                #     conference.marks.ro2_agreed = False
                # conference.marks.ro2_remarks = conferences[i][0]
                conference.marks.save()
                conference.save()

            for i in range(len(db_epubs)):
                epub = db_epubs[i]
                if epub.marks is None:
                    epub.marks = MarkField()

                epub.marks.ro2_agreed = True
                # if epubs[i][1] == 'accept':
                #     pass
                # if epubs[i][1] == 'reject':
                #     epub.marks.ro2_agreed = False
                # epub.marks.ro2_remarks = epubs[i][0]
                epub.marks.save()
                epub.save()

            file.ro2_validator.research_validated = True
            file.ro2_validator.save()

        return render(request, "html/r2/faculty/foem/research-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def project_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'project-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST':
            # projects = [value for key, value in dict(request.POST).items() if key.startswith('projects')]
            db_projects = list(file.projects.all())

            for i in range(len(db_projects)):
                project = db_projects[i]
                if project.marks is None:
                    project.marks = MarkField()
                project.marks.ro2_agreed = True
                # if projects[i][1] == 'accept':
                #     project.marks.ro2_agreed = True
                # if projects[i][1] == 'reject':
                #     project.marks.ro2_agreed = False
                # project.marks.ro2_remarks = projects[i][0]
                project.marks.save()
                project.save()

            file.ro2_validator.project_validated = True
            file.ro2_validator.save()

        return render(request, "html/r2/faculty/foem/project-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def phd_guidance_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'phd-guidance-entry', 'file': file,
                   'external_guidance': file.phd_guidance.filter(category='external'),
                   'internal_guidance': file.phd_guidance.filter(category='internal'),
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST':
            # internal = [value for key, value in dict(request.POST).items() if key.startswith('internal')]
            db_internal = list(file.phd_guidance.filter(category='internal'))
            external = [value for key, value in dict(request.POST).items() if key.startswith('external')]
            db_external = list(file.phd_guidance.filter(category='external'))

            for i in range(len(db_internal)):
                guidance = db_internal[i]
                if guidance.marks is None:
                    guidance.marks = MarkField()
                guidance.marks.ro2_agreed = True

                # if internal[i][1] == 'accept':
                #     guidance.marks.ro2_agreed = True
                # if internal[i][1] == 'reject':
                #     guidance.marks.ro2_agreed = False
                # guidance.marks.ro2_remarks = internal[i][0]
                guidance.marks.save()
                guidance.save()

            for i in range(len(db_external)):
                guidance = db_external[i]
                if guidance.marks is None:
                    guidance.marks = MarkField()
                if external[i][1] == 'accept':
                    guidance.marks.ro2_agreed = True
                if external[i][1] == 'reject':
                    guidance.marks.ro2_agreed = False
                guidance.marks.ro2_remarks = external[i][0]
                guidance.marks.save()
                guidance.save()

            file.ro2_validator.phd_validated = True
            file.ro2_validator.save()

        context['external_guidance'] = file.phd_guidance.filter(category='external')
        context['internal_guidance'] = file.phd_guidance.filter(category='internal')

        return render(request, "html/r2/faculty/foem/phd-guidance-entry.html", context)

    @staticmethod
    def dissertation_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'dissertation-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST':
            print(request.POST)
            # bachelors = [value for key, value in dict(request.POST).items() if key.startswith('bachelors')]
            # db_bachelors = list(file.bachelors_dissertation.all())
            masters = [value for key, value in dict(request.POST).items() if key.startswith('masters')]
            db_masters = list(file.masters_thesis.all())

            # for i in range(len(db_bachelors)):
            #     dissertation = db_bachelors[i]
            #     if dissertation.marks is None:
            #         dissertation.marks = MarkField()
            #
            #     if bachelors[i][1] == 'accept':
            #         dissertation.marks.ro2_agreed = True
            #     if bachelors[i][1] == 'reject':
            #         dissertation.marks.ro2_agreed = False
            #     dissertation.marks.ro2_remarks = bachelors[i][0]
            #     dissertation.marks.save()
            #     dissertation.save()

            for i in range(len(db_masters)):
                dissertation = db_masters[i]
                if dissertation.marks is None:
                    dissertation.marks = MarkField()

                if masters[i][1] == 'accept':
                    dissertation.marks.ro2_agreed = True
                if masters[i][1] == 'reject':
                    dissertation.marks.ro2_agreed = False
                dissertation.marks.ro2_remarks = masters[i][0]
                dissertation.marks.save()
                dissertation.save()

            file.ro2_validator.dissertation_validated = True
            file.ro2_validator.save()
        return render(request, "html/r2/faculty/foem/dissertation-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def patent_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'patent-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}
        if len(file.patents.all()) == 0:
            context['faculty_advisor_show'] = True
        else:
            context['faculty_advisor_show'] = False

        if request.method == 'POST':
            # patents = [value for key, value in dict(request.POST).items() if key.startswith('patents')]
            db_patents = list(file.patents.all())

            for i in range(len(db_patents)):
                patent = db_patents[i]
                if patent.marks is None:
                    patent.marks = MarkField()
                patent.marks.ro2_agreed = True
                # if patents[i][1] == 'accept':
                #     patent.marks.ro2_agreed = True
                # if patents[i][1] == 'reject':
                #     patent.marks.ro2_agreed = False
                # patent.marks.ro2_remarks = patents[i][0]
                patent.marks.save()
                patent.save()

            if file.user.designation_abbreviation == 'assistant_prof_on_contract' and file.faculty_advisor_available and \
                    context['faculty_advisor_show']:
                advisors = [value for key, value in dict(request.POST).items() if key.startswith('advisor')]
                db_advisors = list(file.faculty_advisor.all())
                try:
                    if file.faculty_advisor_available:
                        # fac_advisor_marks = int(request.POST.get('faculty_advisor_marks'))
                        if file.faculty_advisor_total is None:
                            file.faculty_advisor_total = MarkField()
                        # file.faculty_advisor_total.ro2 = fac_advisor_marks
                        file.faculty_advisor_total.save()
                        file.save()
                except ValueError:
                    return HttpResponse("Marks should be an integer")

                total = 0
                for i in range(len(db_advisors)):
                    advisor = db_advisors[i]
                    if advisor.marks is None:
                        advisor.marks = MarkField()

                    if advisors[i][1] == 'accept':
                        advisor.marks.ro2_agreed = True
                    if advisors[i][1] == 'reject':
                        advisor.marks.ro2_agreed = False
                    advisor.marks.ro2_remarks = advisors[i][0]
                    advisor.marks.ro2 = float(advisors[i][2])
                    total += float(advisors[i][2])
                    advisor.marks.save()
                    advisor.save()
                file.faculty_advisor_total.ro2 = total
                file.faculty_advisor_total.save()

            file.ro2_validator.patents_validated = True
            file.ro2_validator.save()

        return render(request, "html/r2/faculty/foem/patent-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def award_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'award-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST':
            # awards = [value for key, value in dict(request.POST).items() if key.startswith('awards')]
            db_awards = list(file.recognition_awards.all())

            for i in range(len(db_awards)):
                award = db_awards[i]
                if award.marks is None:
                    award.marks = MarkField()
                award.marks.ro2_agreed = True
                # if awards[i][1] == 'accept':
                #     award.marks.ro2_agreed = True
                # if awards[i][1] == 'reject':
                #     award.marks.ro2_agreed = False
                # award.marks.ro2_remarks = awards[i][0]
                award.marks.save()
                award.save()

            file.ro2_validator.award_validated = True
            file.ro2_validator.save()

        return render(request, "html/r2/faculty/foem/award-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def consultancy_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'consultancy-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST':
            # consultancies = [value for key, value in dict(request.POST).items() if key.startswith('consultancy')]
            db_consultancies = list(file.providing_consultancy.all())

            for i in range(len(db_consultancies)):
                consultancy = db_consultancies[i]
                if consultancy.marks is None:
                    consultancy.marks = MarkField()
                consultancy.marks.ro2_agreed = True

                # if consultancies[i][1] == 'accept':
                #     consultancy.marks.ro2_agreed = True
                # if consultancies[i][1] == 'reject':
                #     consultancy.marks.ro2_agreed = False
                # consultancy.marks.ro2_remarks = consultancies[i][0]
                consultancy.marks.save()
                consultancy.save()
            if file.user.designation_abbreviation == 'assistant_prof_on_contract' and file.faculty_advisor_available:
                industry_collaboration = [value for key, value in dict(request.POST).items() if
                                          key.startswith('industry')]
                db_industry_collaboration = list(file.industry_collaboration.all())

                for i in range(len(db_industry_collaboration)):
                    industry = db_industry_collaboration[i]
                    if industry.marks is None:
                        industry.marks = MarkField()

                    if industry_collaboration[i][1] == 'accept':
                        industry.marks.ro2_agreed = True
                    if industry_collaboration[i][1] == 'reject':
                        industry.marks.ro2_agreed = False
                    industry.marks.ro2_remarks = industry_collaboration[i][0]
                    industry.marks.save()
                    industry.save()

            file.ro2_validator.consultancy_validated = True
            file.ro2_validator.save()
        return render(request, "html/r2/faculty/foem/consultancy-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def academia_collab_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'academia-collab-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}
        if request.method == 'POST':
            file.academia_collaboration.mou_marks.ro2 = file.academia_collaboration.mou_marks.ro1
            file.academia_collaboration.contribution_marks.ro2 = file.academia_collaboration.contribution_marks.ro1
            file.academia_collaboration.mou_marks.save()
            file.academia_collaboration.contribution_marks.save()
            # print(request.POST)
            # if request.POST.get('mou-action') == 'accept':
            #     file.academia_collaboration.mou_marks.ro2_agreed = True
            #     # file.academia_collaboration.mou_marks.ro2 = request.POST.get('mou_given')
            # else:
            #     file.academia_collaboration.mou_marks.ro2_agreed = False
            # file.academia_collaboration.mou_marks.ro2 = float(request.POST.get('mou_input'))
            #
            # file.academia_collaboration.mou_marks.ro2_remarks = request.POST.get('mou-remarks')
            # file.academia_collaboration.mou_marks.save()
            #
            # if request.POST.get('contribution-action') == 'accept':
            #     file.academia_collaboration.contribution_marks.ro2_agreed = True
            #     # file.academia_collaboration.contribution_marks.ro2 = request.POST.get('contribution_given')
            # else:
            #     file.academia_collaboration.contribution_marks.ro2_agreed = False
            # file.academia_collaboration.contribution_marks.ro2 = float(request.POST.get('contrib_input'))
            # file.academia_collaboration.contribution_marks.ro2_remarks = request.POST.get('contrib-remarks')
            # file.academia_collaboration.contribution_marks.save()
            # if file.academia_collaboration_total is None:
            #     file.academia_collaboration_total = MarkField()
            # file.academia_collaboration_total.ro2 = file.academia_collaboration.mou_marks.ro2 + file.academia_collaboration.contribution_marks.ro2
            # file.academia_collaboration_total.save()
            # file.save()

            file.ro2_validator.academia_collab_validated = True
            file.ro2_validator.save()
        return render(request, "html/r2/faculty/foem/academia-collab-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def international_admission_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'international-admission-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}
        if request.method == 'POST':
            file.ro2_validator.international_admission_validated = True
            file.ro2_validator.save()
        return render(request, "html/r1/faculty/foem/international-admission-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def arranging_conference_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'arranging-conference-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}
        if request.method == 'POST' and file.arranging_conferences_available:
            conferences = [value for key, value in dict(request.POST).items() if
                           key.startswith('conf') and key != 'arranging-conferences-marks']
            db_conferences = list(file.arranging_conferences.all())

            try:
                # marks = float(request.POST.get('arranging-conferences-marks'))
                if file.arranging_conferences_total is None:
                    file.arranging_conferences_total = MarkField()
                # file.arranging_conferences_total.ro2 = marks
                file.arranging_conferences_total.save()
                file.save()
            except ValueError:
                return HttpResponse("Marks should be a number")
            total = 0
            for i in range(len(db_conferences)):
                conference = db_conferences[i]
                print(conferences[i])
                if conference.marks is None:
                    conference.marks = MarkField()

                if conferences[i][1] == 'accept':
                    conference.marks.ro2_agreed = True
                if conferences[i][1] == 'reject':
                    conference.marks.ro2_agreed = False
                conference.marks.ro2_remarks = conferences[i][0]
                conference.marks.ro2 = float(conferences[i][2])
                total += float(conferences[i][2])
                conference.marks.save()
                conference.save()
            file.arranging_conferences_total.ro2 = total
            file.arranging_conferences_total.save()
        if request.method == 'POST':
            file.ro2_validator.arranging_conferences_validated = True
            file.ro2_validator.save()
        return render(request, "html/r2/faculty/foem/arranging-conference.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def mentorship_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'mentorship-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}
        if request.method == 'POST' and file.being_mentor_available:
            mentorships = [value for key, value in dict(request.POST).items() if
                           key.startswith('mentor') and key != 'mentorship-marks']
            db_mentorships = list(file.being_mentor.all())

            try:
                # marks = float(request.POST.get('mentorship-marks'))
                if file.being_mentor_total is None:
                    file.being_mentor_total = MarkField()
                # file.being_mentor_total.ro2 = marks
                file.being_mentor_total.save()
                file.save()
            except ValueError:
                return HttpResponse("Marks should be a number")
            total = 0
            for i in range(len(db_mentorships)):
                mentorship = db_mentorships[i]
                if mentorship.marks is None:
                    mentorship.marks = MarkField()

                if mentorships[i][1] == 'accept':
                    mentorship.marks.ro2_agreed = True
                if mentorships[i][1] == 'reject':
                    mentorship.marks.ro2_agreed = False
                mentorship.marks.ro2_remarks = mentorships[i][0]
                mentorship.marks.ro2 = mentorships[i][2]
                total += float(mentorships[i][2])
                mentorship.marks.save()
                mentorship.save()
            file.being_mentor_total.ro2 = total
            file.being_mentor_total.save()
        if request.method == 'POST':
            file.ro2_validator.mentorship_validated = True
            file.ro2_validator.save()
        return render(request, "html/r2/faculty/foem/mentorship-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def attending_conference_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'attending-conference-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST' and file.attending_conferences_available:
            conferences = [value for key, value in dict(request.POST).items() if
                           key.startswith('attending-conferences')]
            db_conferences = list(file.attending_conferences.all())

            try:
                for i in range(len(conferences)):
                    conf = db_conferences[i]
                    if conf.marks is None:
                        conf.marks = MarkField()
                    if conferences[i][1] == 'accept':
                        conf.marks.ro2_agreed = True
                    if conferences[i][1] == 'reject':
                        conf.marks.ro2_agreed = False
                    conf.marks.ro2_remarks = conferences[i][0]
                    conf.marks.save()
                    conf.save()

            except ValueError:
                return HttpResponse("Marks should be a number")
        if request.method == 'POST':
            file.ro2_validator.attending_conferences_validated = True
            file.ro2_validator.save()
        return render(request, "html/r2/faculty/foem/attending-conferences-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def community_development_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'community-development-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST' and file.community_development_available:
            initiatives = [value for key, value in dict(request.POST).items() if key.startswith('initiative')]
            db_initiatives = list(file.community_development.all())
            # marks = request.POST.get('community-development-marks')
            if file.community_development_available:
                if file.community_development_total is None:
                    file.community_development_total = MarkField()
                # file.community_development_total.ro2 = float(marks)
                file.community_development_total.save()
                file.save()
            total = 0
            for i in range(len(db_initiatives)):
                # accept or reject
                initiative = db_initiatives[i]
                if initiative.marks is None:
                    initiative.marks = MarkField()

                if initiatives[i][1] == 'accept':
                    initiative.marks.ro2_agreed = True
                if initiatives[i][1] == 'reject':
                    initiative.marks.ro2_agreed = False
                initiative.marks.ro2_remarks = initiatives[i][0]
                initiative.marks.ro2 = initiatives[i][2]
                total += float(initiatives[i][2])
                initiative.marks.save()
                initiative.save()
            file.community_development_total.ro2 = total
            file.community_development_total.save()
        if request.method == 'POST':
            file.ro2_validator.community_development_validated = True
            file.ro2_validator.save()
        return render(request, "html/r2/faculty/foem/community-development-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def extra_curricular_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'extra-curricular-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST':
            file.involvement_extra_curricular_marks.ro2 = file.involvement_extra_curricular_marks.ro1
            file.involvement_extra_curricular_marks.save()
            # remarks = request.POST.get('extra-curr-remarks')
            # try:
            #     marks = float(request.POST.get('extra-curr-marks'))
            # except ValueError:
            #     return HttpResponse("Marks should be a number")
            # if request.POST.get('extra-action') == 'accept':
            #     file.involvement_extra_curricular_marks.ro2_agreed = True
            # else:
            #     file.involvement_extra_curricular_marks.ro2_agreed = False
            # file.involvement_extra_curricular_marks.ro2 = marks
            # file.involvement_extra_curricular_marks.ro2_remarks = remarks
            # file.involvement_extra_curricular_marks.save()

            file.ro2_validator.extra_curricular_validated = True
            file.ro2_validator.save()

        return render(request, "html/r2/faculty/foem/extra-curricular-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def additional_entry(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'additional-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST':
            file.ro2_validator.additional_validated = True
            file.ro2_validator.save()

        if request.method == 'POST' and file.is_mooc_available:
            action = request.POST.get('mooc-action')
            if file.mooc_course.marks is None:
                file.mooc_course.marks = MarkField()
            file.mooc_course.marks.ro2_remarks = request.POST.get('mooc-remark')
            if action == 'accept':
                file.mooc_course.marks.ro2_agreed = True
                file.mooc_course.marks.ro2 = file.configuration.self_development_mooc_course_marks
            elif action == 'reject':
                file.mooc_course.marks.ro2_agreed = False
                file.mooc_course.marks.ro2 = 0

            file.mooc_course.marks.save()
            file.mooc_course.save()

            file.ro2_validator.additional_validated = True
            file.ro2_validator.save()

        return render(request, "html/r2/faculty/foem/additional-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def senior_feedback(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'senior-feedback-entry', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}

        if request.method == 'POST':
            senior_feedback_grade = request.POST.get('senior-feedback-grade')
            senior_feedback_remarks = request.POST.get('senior-feedback-remarks')
            file.senior_feedback_grade_r2 = senior_feedback_grade
            if file.senior_feedback_marks is None:
                file.senior_feedback_marks = MarkField()
            if senior_feedback_grade == 'O':
                file.senior_feedback_marks.ro2 = file.configuration.senior_feedback_outstanding_marks
            elif senior_feedback_grade == 'G':
                file.senior_feedback_marks.ro2 = file.configuration.senior_feedback_good_marks
            elif senior_feedback_grade == 'A':
                file.senior_feedback_marks.ro2 = file.configuration.senior_feedback_average_marks
            elif senior_feedback_grade == 'U':
                file.senior_feedback_marks.ro2 = file.configuration.senior_feedback_unsatisfactory_marks
            file.senior_feedback_marks.ro2_remarks = senior_feedback_remarks
            file.senior_feedback_marks.save()

            self_development_grade = request.POST.get('self-development-grade')
            self_development_remarks = request.POST.get('self-development-remarks')
            file.self_development_grade_r2 = self_development_grade
            if file.self_development_total is None:
                file.self_development_total = MarkField()
            if self_development_grade == 'O':
                file.self_development_total.ro2 = file.configuration.self_development_outstanding_marks
            elif self_development_grade == 'G':
                file.self_development_total.ro2 = file.configuration.self_development_good_marks
            elif self_development_grade == 'A':
                file.self_development_total.ro2 = file.configuration.self_development_average_marks
            elif self_development_grade == 'U':
                file.self_development_total.ro2 = file.configuration.self_development_unsatisfactory_marks
            file.self_development_total.ro2_remarks = self_development_remarks
            file.self_development_total.save()

            additional_responsibility_grade = request.POST.get('additional-responsibilities-grade')
            additional_responsibility_remarks = request.POST.get('additional-responsibilities-remarks')
            file.additional_responsibilities_grade_r2 = additional_responsibility_grade
            if file.additional_responsibilities_marks is None:
                file.additional_responsibilities_marks = MarkField()
            if additional_responsibility_grade == 'O':
                file.additional_responsibilities_marks.ro2 = file.configuration.additional_responsibilities_outstanding_marks
            elif additional_responsibility_grade == 'G':
                file.additional_responsibilities_marks.ro2 = file.configuration.additional_responsibilities_good_marks
            elif additional_responsibility_grade == 'A':
                file.additional_responsibilities_marks.ro2 = file.configuration.additional_responsibilities_average_marks
            elif additional_responsibility_grade == 'U':
                file.additional_responsibilities_marks.ro2 = file.configuration.additional_responsibilities_unsatisfactory_marks
            file.additional_responsibilities_marks.ro2_remarks = additional_responsibility_remarks
            file.additional_responsibilities_marks.save()

            file.save()

            file.ro2_validator.senior_feedback_validated = True
            file.ro2_validator.save()
        return render(request, "html/r2/faculty/foem/senior-feedback.html", context)

    @login_required(login_url='/login/')
    def review(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'faculty-review', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}
        engine = CalculationEngine(file)
        context['teaching'] = engine.calculateTeachingMaster()
        context['engine'] = engine
        context['engineR2'] = CalculationEngineR2(file)
        file = FacultyHelperFunctions.get_file(pk)
        context['file'] = file
        context['can_submit'] = file.ro2_validator.is_valid_for_ro(
            file.user.designation_abbreviation == 'assistant_prof_on_contract')

        return render(request, "html/r2/faculty/foem/review.html", context)

    @login_required(login_url='/login/')
    def print(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'faculty-review', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}
        engine = CalculationEngine(file)
        context['teaching'] = engine.calculateTeachingMaster()
        context['engine'] = engine
        context['engineR2'] = CalculationEngineR2(file)
        file = FacultyHelperFunctions.get_file(pk)
        context['file'] = file
        context['can_submit'] = file.ro2_validator.is_valid_for_ro(
            file.user.designation_abbreviation == 'assistant_prof_on_contract')

        return render(request, "html/r2/faculty/foem/print.html", context)

    @login_required(login_url='/login/')
    def submit(request, pk):
        if not FacultyHelperFunctions.check_if_ro2_is_authorized(request, pk):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        if request.method == 'POST':
            filex = FacultyHelperFunctions.get_file(pk)
            result = FacultyHelperFunctions.calculateResult(filex.user.username)

            if filex.grand_total is None:
                filex.grand_total = MarkField()
            filex.grand_total.ro2 = result['grand_total']
            filex.grand_total.save()

            if filex.part_a_total is None:
                filex.part_a_total = MarkField()
            filex.part_a_total.ro2 = result['part_a_total']
            filex.part_a_total.save()

            if filex.part_b_total is None:
                filex.part_b_total = MarkField()
            filex.part_b_total.ro2 = result['part_b_total']
            filex.part_b_total.save()

            if filex.part_a_section_1_total is None:
                filex.part_a_section_1_total = MarkField()
            filex.part_a_section_1_total.ro2 = result['part_a_section_1_total']
            filex.part_a_section_1_total.save()

            if filex.part_a_section_2_total is None:
                filex.part_a_section_2_total = MarkField()
            filex.part_a_section_2_total.ro2 = result['part_a_section_2_total']
            filex.part_a_section_2_total.save()

            if filex.part_a_section_3_total is None:
                filex.part_a_section_3_total = MarkField()
            filex.part_a_section_3_total.ro2 = result['part_a_section_3_total']
            filex.part_a_section_3_total.save()

            if filex.part_a_section_4_total is None:
                filex.part_a_section_4_total = MarkField()
            filex.part_a_section_4_total.ro2 = result['part_a_section_4_total']
            filex.part_a_section_4_total.save()

            filex.r2_percentage = result['percent']
            filex.r2_grade = result['grade']
            filex.file_level = 'HR'
            filex.save()
        file = FacultyHelperFunctions.get_file(pk)
        context = {'user': request.user, 'page_name': 'faculty-submit', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}
        engine = CalculationEngine(file)
        context['teaching'] = engine.calculateTeachingMaster()
        context['engine'] = engine
        context['engineR2'] = CalculationEngineR2(file)
        file = FacultyHelperFunctions.get_file(pk)
        context['file'] = file
        context['can_submit'] = file.ro2_validator.is_valid_for_ro(
            file.user.designation_abbreviation == 'assistant_prof_on_contract')
        return render(request, "html/r2/faculty/foem/submit.html", context)


class FacultyHelperFunctions:
    @staticmethod
    def calculateResult(username):
        appraisee = User.objects.get(username=username)
        file = None
        if appraisee.designation_abbreviation == "assistant_prof_on_contract":
            file = FOEMAssistantProfOnContractAppraisalFile.objects.filter(user=appraisee).first()
        elif appraisee.designation_abbreviation == "assistant_prof":
            file = FOEMAssistantProfAppraisalFile.objects.filter(user=appraisee).first()
        elif appraisee.designation_abbreviation == "associate_prof":
            file = FOEMAssociateProfAppraisalFile.objects.filter(user=appraisee).first()
        elif appraisee.designation_abbreviation == "prof":
            file = FOEMProfAppraisalFile.objects.filter(user=appraisee).first()

        denominator = file.configuration.grand_total
        engine = CalculationEngineR2(file)

        grand_total = engine.calculateGrandTotal()
        teaching_total = engine.calculateTeachingMaster()

        percent = (grand_total / denominator) * 100
        percent = round(percent + 0.01, 0)

        result = {
            'grand_total': grand_total,
            'part_a_total': engine.calculatePartA(),
            'part_b_total': engine.calculatePartB(),
            'part_a_section_1_total': engine.calculateTeachingMaster(),
            'part_a_section_2_total': engine.calculateSection2(),
            'part_a_section_3_total': engine.calculateSection3(),
            'part_a_section_4_total': engine.calculateSection4(),
            'grade': None,
            'percent': percent,
        }

        if percent >= 95 and teaching_total >= file.configuration.section_1_minimum_marks:
            result['grade'] = 'OUTSTANDING'
        elif percent >= 65:
            result['grade'] = 'GOOD'
        elif percent >= 35:
            result['grade'] = 'AVERAGE'
        else:
            result['grade'] = 'BELOW AVERAGE'

        return result

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
    def get_file(appraisee_id):
        try:
            appraisee = User.objects.get(id=appraisee_id)
            print(appraisee)
            if appraisee.designation_abbreviation == "assistant_prof_on_contract":
                file = FOEMAssistantProfOnContractAppraisalFile.objects.filter(user=appraisee).first()
            elif appraisee.designation_abbreviation == "assistant_prof":
                file = FOEMAssistantProfAppraisalFile.objects.filter(user=appraisee).first()
            elif appraisee.designation_abbreviation == "associate_prof":
                file = FOEMAssociateProfAppraisalFile.objects.filter(user=appraisee).first()
            elif appraisee.designation_abbreviation == "prof":
                file = FOEMProfAppraisalFile.objects.filter(user=appraisee).first()
            else:
                return None
        except FOEMAssistantProfOnContractAppraisalFile.DoesNotExist or FOEMAssistantProfAppraisalFile.DoesNotExist or FOEMAssociateProfAppraisalFile.DoesNotExist or FOEMProfAppraisalFile.DoesNotExist or User.DoesNotExist:
            raise Http404("File does not exist")
        FacultyHelperFunctions.createValidator(file)
        return file

    @staticmethod
    def createValidator(file):
        if file.ro2_validator is None:
            file.ro2_validator = FacultyValidator()
            file.ro2_validator.save()
            file.save()

    @staticmethod
    def get_cycle():
        try:
            config = SOEMFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first()
            print(config.get_cycle())
            return {'name': config.get_cycle(), 'config': config, 'current_date': CurrentDate.objects.first().date}
        except SOEMFacultyAppraisalCycleConfiguration.DoesNotExist:
            return HttpResponse("Problem while fetching cycles")

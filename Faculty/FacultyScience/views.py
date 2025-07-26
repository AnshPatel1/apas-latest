from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from BulkUpload.BulkUploadScience.models import *
from MasterConfiguration.models import ScienceFacultyAppraisalCycleConfiguration, ScienceFacultyAppraisalCycleInclusion, CurrentDate, ShowResult


class FacultyViewSet:
    @staticmethod
    @login_required(login_url='/login/')
    def dashboard(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)
        context = {'user': request.user, 'page_name': 'faculty-home'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file
        return render(request, "html/faculty/science/dashboard.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def verify_data(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)
        context = {'user': request.user, 'page_name': 'verify-data'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is None:
            return HttpResponse("No Appraisal File Found")
        context['file'] = file

        try:
            context['teaching_load'] = ViewTeachingLoad.objects.get(faculty=request.user)
            context['student_feedback'] = ViewStudentFeedback.objects.get(faculty=request.user)
            context['exam_duty'] = ViewExamDuty.objects.get(faculty=request.user)
            context['books'] = ViewBook.objects.filter(faculty=request.user)
            context['papers'] = ViewScopusWos.objects.filter(faculty=request.user, type='journal')
            context['conferences'] = ViewScopusWos.objects.filter(faculty=request.user, type='conf')
            context['articles'] = ViewScopusWos.objects.filter(faculty=request.user, type='article')
            context['epubs'] = ViewScopusWos.objects.filter(faculty=request.user, type='epub')
            context['epubs_articles'] = context['epubs'].union(context['articles'])
            context['projects'] = ViewProject.objects.filter(faculty=request.user)
            context['internal_phd_guidances'] = ViewPhDGuidance.objects.filter(faculty=request.user)
            context['patents'] = ViewPatent.objects.filter(faculty=request.user)
            context['awards'] = ViewAward.objects.filter(faculty=request.user)
            # context['consultancies'] = ViewConsultancy.objects.filter(faculty=request.user)
            context['academia_collab'] = ViewAcademiaCollaboration.objects.get(faculty=request.user)
            context['extra_curricular'] = ViewCoCurricular.objects.get(faculty=request.user)
            context['additional'] = ViewAdditionalMarks.objects.get(faculty=request.user)
        except ViewTeachingLoad.DoesNotExist:
            return HttpResponse("No Teaching Load Found")
        except ViewTeachingLoad.MultipleObjectsReturned:
            return HttpResponse("Multiple Teaching Loads Found. Please contact admin to get this fixed.")
        except ViewStudentFeedback.DoesNotExist:
            return HttpResponse("No Student Feedback Found")
        except ViewStudentFeedback.MultipleObjectsReturned:
            return HttpResponse("Multiple Student Feedbacks Found. Please contact admin to get this fixed.")
        except ViewExamDuty.DoesNotExist:
            return HttpResponse("No Exam Duty Found")
        except ViewExamDuty.MultipleObjectsReturned:
            return HttpResponse("Multiple Exam Duties Found. Please contact admin to get this fixed.")
        except ViewAcademiaCollaboration.DoesNotExist:
            ViewAcademiaCollaboration.objects.create(faculty=request.user,
                                                     designation=request.user.designation_abbreviation,
                                                     department=request.user.department, mou_available=False,
                                                     mou_marks=0, marks=0)
        except ViewAcademiaCollaboration.MultipleObjectsReturned:
            return HttpResponse("Multiple Academia Collaborations Marks Found. Please contact admin to get this fixed.")
        except ViewCoCurricular.DoesNotExist:
            return HttpResponse("No Extra Curricular Marks Found")
        except ViewCoCurricular.MultipleObjectsReturned:
            return HttpResponse("Multiple Extra Curricular Marks Found. Please contact admin to get this fixed.")
        except ViewAdditionalMarks.DoesNotExist:
            return HttpResponse("No Additional Marks Found")
        except ViewAdditionalMarks.MultipleObjectsReturned:
            return HttpResponse("Multiple Additional Marks Found. Please contact admin to get this fixed.")

        if request.method == 'POST' and not file.has_verified_data:
            file.has_verified_data = True
            file.save()
            # Copying all data from view objects to actual files.
            # 1. Teaching Load
            if file.teaching_load is None:
                file.teaching_load = TeachingLoad()
            file.teaching_load.semester_odd = context['teaching_load'].load_odd
            file.teaching_load.semester_even = context['teaching_load'].load_even
            file.teaching_load.save()

            # 2. Student Feedback
            file.student_feedback = context['student_feedback'].student_feedback
            file.save()

            # 3. Exam Duty
            if file.exam_duty is None:
                file.exam_duty = ExamDuty()
            file.exam_duty.timely_invigilation = context['exam_duty'].timely_invigilation
            file.exam_duty.paper_setting = context['exam_duty'].paper_setting
            file.exam_duty.evaluation = context['exam_duty'].evaluation
            file.exam_duty.result_submission = context['exam_duty'].result_submission
            file.exam_duty.save()

            # 4. Books
            pubs_text = []
            pubs_research = []
            for book in context['books']:
                publication = Publication()
                publication.title = book.title
                publication.month = book.month
                publication.year = book.year
                publication.is_main_author = book.is_main_author
                publication.co_author_count = book.co_author_count
                if book.category.lower() == 'research':
                    publication.category = 'research'
                elif book.category.lower() == 'text':
                    publication.category = 'textbook'
                if book.type.lower() == 'book':
                    publication.type = 'book'
                elif book.type.lower() == 'chapter':
                    if book.is_editor:
                        publication.type = 'edited_book_chapter'
                    else:
                        publication.type = 'book_chapter'
                publication.isbn = book.isbn
                publication.publication_level = book.level.lower()
                publication.author = book.faculty
                if book.category.lower() == 'research':
                    pubs_research.append(publication)
                elif book.category.lower() == 'text':
                    pubs_text.append(publication)
            Publication.objects.bulk_create(pubs_text)
            Publication.objects.bulk_create(pubs_research)
            file.textbooks.all().delete()
            file.textbooks.set(pubs_text)
            file.research_books.all().delete()
            file.research_books.set(pubs_research)
            file.save()

            # 5. Papers
            pubs_paper = []
            pubs_conference = []
            pubs_epub = []
            for paper in context['papers'].union(context['conferences'], context['epubs_articles']):
                pub = Paper()
                pub.title = paper.title
                pub.entity_name = paper.entity_name
                pub.month = paper.month
                pub.year = paper.year
                pub.isbn = paper.isbn
                pub.is_main_author = paper.is_main_author
                pub.co_author_count = paper.co_author_count
                if paper.is_scopus:
                    pub.category = 'scopus'
                elif paper.is_wos:
                    pub.category = 'wos'
                else:
                    pub.category = 'other'
                if paper.type.lower() == 'journal':
                    pub.type = 'journal'
                    pub.quality = paper.paper_quality
                    pubs_paper.append(pub)
                elif paper.type.lower() == 'conf':
                    pub.type = 'conference'
                    pub.quality = paper.paper_quality
                    pub.conference_organization = paper.conference_organization
                    pub.conference_level = paper.conference_level
                    pubs_conference.append(pub)
                elif paper.type.lower() == 'article':
                    pub.type = 'article'
                    pubs_epub.append(pub)
                elif paper.type.lower() == 'epub':
                    pub.type = 'epub'
                    pubs_epub.append(pub)
            file.publications_in_scopus_wos.all().delete()
            Paper.objects.bulk_create(pubs_paper)
            file.publications_in_scopus_wos.set(pubs_paper)
            file.conference_proceedings_scopus_wos.all().delete()
            Paper.objects.bulk_create(pubs_conference)
            file.conference_proceedings_scopus_wos.set(pubs_conference)
            file.e_publications_articles.all().delete()
            Paper.objects.bulk_create(pubs_epub)
            file.e_publications_articles.set(pubs_epub)

            # 6. Projects
            projects = []
            for project in context['projects']:
                proj = Project()
                proj.description = project.title
                proj.month = project.month
                proj.year = project.year
                proj.funding_agency = project.funding_agency
                proj.funds_received = project.amount
                if project.role == 'pi' or project.role == 'copi':
                    proj.project_participation = project.role
                # if project.status.lower() == 'completed' or project.status.lower() == 'ongoing':
                #     proj.status = project.status.lower()
                if project.is_institutional:
                    proj.project_category = 'INS'
                    mf = MarkField()
                    mf.ro1 = project.institutional_marks
                    mf.ro1_agreed = True
                    mf.save()
                    proj.marks = mf
                elif project.is_osrp:
                    proj.project_category = 'OSRP'
                else:
                    proj.project_category = project.get_category()
                proj.innovator = project.faculty
                projects.append(proj)
            file.projects.all().delete()
            Project.objects.bulk_create(projects)
            file.projects.set(projects)

            # 7. PhD Guidances
            phd_guidances = []
            for phd in context['internal_phd_guidances']:
                guidance = PhDGuidance()
                guidance.student_name = phd.student_name
                guidance.year = phd.year
                guidance.category = 'internal'
                guidance.faculty = phd.faculty
                if phd.status == 'awarded' or phd.status == 'synopsis':
                    guidance.status = phd.status
                elif phd.status == 'inprogress':
                    guidance.status = 'ongoing'
                else:
                    guidance.status = 'other'
                phd_guidances.append(guidance)
            file.phd_guidance.all().delete()
            PhDGuidance.objects.bulk_create(phd_guidances)
            file.phd_guidance.set(phd_guidances)

            # 8. Patents
            patents = []
            for patent in context['patents']:
                p = Patent()
                p.title = patent.description
                p.year = patent.year
                p.month = patent.month
                if patent.status == 'granted' or patent.status == 'licensed' or patent.status == 'filed' or patent.status == 'published':
                    p.status = patent.status
                else:
                    return HttpResponse("Invalid patent status")
                p.application_no = patent.application_no
                p.inventor = patent.faculty
                patents.append(p)
            file.patents.all().delete()
            Patent.objects.bulk_create(patents)
            file.patents.set(patents)

            # 9. Awards
            awards = []
            for award in context['awards']:
                a = Award()
                a.title = award.title
                a.description = award.description
                a.year = award.year
                a.month = award.month
                a.awardee = award.faculty
                if award.level == 'international' or award.level == 'national' or award.level == 'state' or award.level == 'regional' or award.level == 'university':
                    a.award_type = award.level
                else:
                    return HttpResponse("Invalid award level")
                awards.append(a)
            file.recognition_awards.all().delete()
            Award.objects.bulk_create(awards)
            file.recognition_awards.set(awards)

            # 10. Consultancy
            # consultancies = []
            # for consultancy in context['consultancies']:
            #     c = Consultancy()
            #     c.description = consultancy.description
            #     c.year = consultancy.year
            #     c.month = consultancy.month
            #     c.amount = consultancy.amount
            #     c.faculty = consultancy.faculty
            #     c.consultancy_type = consultancy.type
            #     consultancies.append(c)
            # file.providing_consultancy.all().delete()
            # Consultancy.objects.bulk_create(consultancies)
            # file.providing_consultancy.set(consultancies)

            # 11. Academia Collaboration
            aca = AcademiaCollaboration()
            aca.appraisee = request.user
            aca.mou_marks = MarkField(ro1=context['academia_collab'].mou_marks, ro1_agreed=True)
            aca.mou_marks.save()
            aca.contribution_marks = MarkField(ro1=context['academia_collab'].marks, ro1_agreed=True)
            aca.contribution_marks.save()
            aca.save()
            if file.academia_collaboration is not None:
                file.academia_collaboration.delete()
            file.academia_collaboration = aca
            if file.academia_collaboration_total is None:
                file.academia_collaboration_total = MarkField()
            file.academia_collaboration_total.ro1 = aca.mou_marks.ro1 + aca.contribution_marks.ro1
            file.academia_collaboration_total.ro1_remarks = 'From: Dean (R&D) Office/ Dean & Director'
            file.academia_collaboration_total.ro1_agreed = True
            file.academia_collaboration_total.save()

            # 12. Extra Curricular Activities
            if file.involvement_extra_curricular_marks is None:
                file.involvement_extra_curricular_marks = MarkField()
            file.involvement_extra_curricular_marks.ro1 = context['extra_curricular'].marks
            file.involvement_extra_curricular_marks.ro1_remarks = 'From: OSAIL'
            file.involvement_extra_curricular_marks.ro1_agreed = True
            file.involvement_extra_curricular_marks.save()

            # 13. Additional Marks
            if file.placement_duty_marks is None:
                file.placement_duty_marks = MarkField()
            file.placement_duty_marks.ro1 = context['additional'].placement_activity
            file.placement_duty_marks.ro1_remarks = 'From: Dean (Placement & Admission)'
            file.placement_duty_marks.ro1_agreed = True
            file.placement_duty_marks.save()

            if file.admission_duty_marks is None:
                file.admission_duty_marks = MarkField()
            file.admission_duty_marks.ro1 = context['additional'].admission_activity
            file.admission_duty_marks.ro1_remarks = 'From: Dean (Placement & Admission)'
            file.admission_duty_marks.ro1_agreed = True
            file.admission_duty_marks.save()

            file.save()
        else:
            if file.has_verified_data and request.method == 'POST':
                return render(request, "html/faculty/science/verify-data.html", context)

        if file.validator is None:
            file.validator = FacultyValidator()
            file.validator.save()

        file.save()

        return render(request, "html/faculty/science/verify-data.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def teaching_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'teaching-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        context['books'] = file.textbooks.all().union(file.research_books.all())
        if file is not None:
            context['file'] = file
        if request.method == 'POST':
            if file.modern_teaching_methods is None:
                file.modern_teaching_methods = ModernMethods()
                file.modern_teaching_methods.save()
                file.save()
            file.modern_teaching_methods.flip_classes = request.POST.get('teaching-flip-classes')
            file.upkeep_of_course_files = request.POST.get('upkeep-of-course-files')
            file.inclusion_of_alumni = request.POST.get('inclusion-of-alumni')
            file.modern_teaching_methods.save()
            file.save()

            file.validator.teaching_validated = True
            file.validator.save()

        return render(request, "html/faculty/science/teaching.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def research_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'research-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        context['books'] = file.textbooks.all().union(file.research_books.all())
        if file is not None:
            context['file'] = file
        return render(request, "html/faculty/science/research-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def project_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'project-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file

        return render(request, "html/faculty/science/project-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def phd_guidance_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'phd-guidance-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file
        if request.method == 'POST':
            data_available = 'No' not in dict(request.POST)['external-guidance-available']
            file.external_phd_guidance_available = data_available
            file.save()
            
            if data_available:
                entries = {key: value for key, value in dict(request.POST).items() if key.startswith('phdguidance')}
                entries = list(entries.values())
                ext_phd = []
                for entry in entries:
                    guidance = PhDGuidance()
                    guidance.faculty = request.user
                    guidance.description = entry[0]
                    guidance.student_name = entry[1]
                    guidance.scopus_publications = entry[2]
                    guidance.category = 'external'
                    ext_phd.append(guidance)
                file.phd_guidance.filter(category='external').delete()
                PhDGuidance.objects.bulk_create(ext_phd)
                file.phd_guidance.add(*ext_phd)
            else:
                file.phd_guidance.filter(category='external').delete()
            file.validator.phd_validated = True
            file.validator.save()
        context['external_guidance'] = file.phd_guidance.filter(category='external')
        context['internal_guidance'] = file.phd_guidance.filter(category='internal')
        return render(request, "html/faculty/science/phd-guidance-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def dissertation_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'dissertation-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file
        if request.method == 'POST':
            file.validator.dissertation_validated = True
            file.validator.save()
            bachelors_available = 'No' not in dict(request.POST)['bachelors-available']
            masters_available = 'No' not in dict(request.POST)['masters-available']
            file.bachelors_dissertation_available = bachelors_available
            file.masters_thesis_available = masters_available
            print('No' in dict(request.POST)['bachelors-available'], masters_available)
            file.save()
            if bachelors_available:
                entries = {key: value for key, value in dict(request.POST).items() if
                           key.startswith('bachelors-dissertation')}
                entries = list(entries.values())
                bachelors = []
                for entry in entries:
                    diss = BachelorsDissertation()
                    diss.faculty = request.user
                    diss.description = entry[0]
                    diss.student_name = entry[1]
                    if entry[2] == 'awarded':
                        diss.is_awarded = True
                    bachelors.append(diss)
                file.bachelors_dissertation.all().delete()
                BachelorsDissertation.objects.bulk_create(bachelors)
                file.bachelors_dissertation.set(bachelors)
            else:
                file.bachelors_dissertation.all().delete()
            if masters_available:
                entries = {key: value for key, value in dict(request.POST).items() if
                           key.startswith('masters-dissertation')}
                entries = list(entries.values())
                masters = []
                for entry in entries:
                    thesis = MastersDissertation()
                    thesis.faculty = request.user
                    thesis.description = entry[0]
                    thesis.student_name = entry[1]
                    if entry[2] == 'submitted' or entry[2] == 'submitted_patent_published' or entry[
                        2] == 'submitted_patent_papers_published':
                        thesis.status = entry[2]
                    masters.append(thesis)
                file.masters_thesis.all().delete()
                MastersDissertation.objects.bulk_create(masters)
                file.masters_thesis.set(masters)
            else:
                file.masters_thesis.all().delete()
        return render(request, "html/faculty/science/dissertation-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def patent_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'patent-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file
        if request.method == 'POST':
            file.validator.patents_validated = True
            file.validator.save()
        if request.user.designation_abbreviation == 'assistant_prof_on_contract' and len(file.patents.all()) == 0:
            # if True:
            if request.method == 'POST':
                available = 'No' not in dict(request.POST)['faculty-available']
                file.faculty_advisor_available = available

                file.save()
                if available:
                    entries = {key: value for key, value in dict(request.POST).items() if key.startswith('faculty-advisor')}
                    entries = list(entries.values())
                    print(entries)
                    advisories = []
                    for entry in entries:
                        adv = FacultyAdvisor()
                        adv.faculty = request.user
                        adv.title = entry[0]
                        adv.description = entry[1]
                        advisories.append(adv)

                    file.faculty_advisor.all().delete()
                    FacultyAdvisor.objects.bulk_create(advisories)
                    file.faculty_advisor.set(advisories)
                else:
                    file.faculty_advisor.all().delete()
                
        return render(request, "html/faculty/science/patent-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def award_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)


        context = {'user': request.user, 'page_name': 'award-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file
        return render(request, "html/faculty/science/award-entry.html", context)

    # @staticmethod
    # @login_required(login_url='/login/')
    # def consultancy_entry(request):
    #     if not FacultyHelperFunctions.check_authorized_user(request):
    #         context = {
    #             'error_code': "Unauthorized Error",
    #             "error_message": "You are not authorized to view this page."
    #         }
    #         return render(request, "html/error_pages/pages-error.html", context)
    #
    #     context = {'user': request.user, 'page_name': 'consultancy-entry'}
    #     file = FacultyHelperFunctions.get_appraisal_file(request)
    #     context['cycle'] = FacultyHelperFunctions.get_cycle()
    #     if file is not None:
    #         context['file'] = file
    #     if request.method == 'POST':
    #         file.validator.consultancy_validated = True
    #         file.validator.save()
    #     if request.user.designation_abbreviation == 'assistant_prof_on_contract':
    #         # if True:
    #         if request.method == 'POST':
    #             available = 'No' not in dict(request.POST)['industry-available']
    #             file.industry_collaboration_available = available
    #             file.save()
    #             if available:
    #                 entries = {key: value for key, value in dict(request.POST).items() if key.startswith('industry-collaboration')}
    #                 entries = list(entries.values())
    #                 print(entries)
    #                 collabs = []
    #                 for entry in entries:
    #                     collab = Collaboration()
    #                     collab.faculty = request.user
    #                     collab.title = entry[0]
    #                     collab.collaboration_type = 'industry'
    #                     collab.description = entry[1]
    #                     try:
    #                         collab.amount = float(entry[2])
    #                     except ValueError:
    #                         return HttpResponse("Invalid Amount")
    #                     collabs.append(collab)
    #                 file.industry_collaboration.all().delete()
    #                 Collaboration.objects.bulk_create(collabs)
    #                 file.industry_collaboration.set(collabs)
    #             else:
    #                 file.industry_collaboration.all().delete()
    #
    #     return render(request, "html/faculty/science/consultancy-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def academia_collab_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)
        context = {'user': request.user, 'page_name': 'academia-collab-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file
        return render(request, "html/faculty/science/academia-collab-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def arranging_conference_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'arranging-conference-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file

        if request.method == 'POST':
            file.validator.arranging_conferences_validated = True
            file.validator.save()
            available = 'No' not in dict(request.POST)['conferences-available']
            file.arranging_conferences_available = available
            file.save()
            print(available)
            if available:
                entries = {key: value for key, value in dict(request.POST).items() if key.startswith('arranging-conferences')}
                entries = list(entries.values())
                data = []
                for entry in entries:
                    point = GenericMarkedParameter()
                    point.faculty = request.user
                    point.title = entry[0]
                    point.description = entry[1]
                    data.append(point)
                file.arranging_conferences.all().delete()
                GenericMarkedParameter.objects.bulk_create(data)
                file.arranging_conferences.set(data)
            else:
                file.arranging_conferences.all().delete()

        return render(request, "html/faculty/science/arranging-conference.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def mentorship_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'mentorship-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file

        if request.method == 'POST':
            file.validator.mentorship_validated = True
            file.validator.save()
            available = 'No' not in dict(request.POST)['mentorship-available']
            file.being_mentor_available = available
            file.save()
            print(available)
            if available:
                entries = {key: value for key, value in dict(request.POST).items() if key.startswith('mentorship-data')}
                entries = list(entries.values())
                data = []
                for entry in entries:
                    point = GenericMarkedParameter()
                    point.faculty = request.user
                    point.title = entry[0]
                    point.description = entry[1]
                    data.append(point)
                file.being_mentor.all().delete()
                GenericMarkedParameter.objects.bulk_create(data)
                file.being_mentor.set(data)
            else:
                file.being_mentor.all().delete()
        return render(request, "html/faculty/science/mentorship-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def attending_conference_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'attending-conference-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file

        if request.method == 'POST':
            file.validator.attending_conferences_validated = True
            file.validator.save()
            available = 'No' not in dict(request.POST)['attending-available']
            file.attending_conferences_available = available
            file.save()
            print(available)
            if available:
                entries = {key: value for key, value in dict(request.POST).items() if key.startswith('attending-conferences')}
                entries = list(entries.values())
                data = []
                for entry in entries:
                    point = GenericMarkedParameter()
                    point.faculty = request.user
                    point.title = entry[0]
                    point.description = entry[1]
                    data.append(point)
                file.attending_conferences.all().delete()
                GenericMarkedParameter.objects.bulk_create(data)
                file.attending_conferences.set(data)
            else:
                file.attending_conferences.all().delete()
        return render(request, "html/faculty/science/attending-conferences-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def community_development_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'community-development-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file

        if request.method == 'POST':
            file.validator.community_development_validated = True
            file.validator.save()
            available = 'No' not in dict(request.POST)['community-available']
            file.community_development_available = available
            file.save()
            print(available)
            if available:
                entries = {key: value for key, value in dict(request.POST).items() if key.startswith('community-development')}
                entries = list(entries.values())
                data = []
                for entry in entries:
                    point = GenericMarkedParameter()
                    point.faculty = request.user
                    point.title = entry[0]
                    point.description = entry[1]
                    data.append(point)
                file.community_development.all().delete()
                GenericMarkedParameter.objects.bulk_create(data)
                file.community_development.set(data)
            else:
                file.community_development.all().delete()
        return render(request, "html/faculty/science/community-development-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def extra_curricular_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'extra-curricular-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file
        return render(request, "html/faculty/science/extra-curricular-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def additional_entry(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'additional-entry'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file

        if request.method == 'POST':
            if request.method == 'POST':
                file.validator.additional_validated = True
                file.validator.save()
                available = 'No' not in dict(request.POST)['mooc-available']
                file.is_mooc_available = available
                file.save()
                print(available)
                if available:
                    cert = Certification()
                    mooc_file = request.FILES.get('mooc-file')
                    print(mooc_file)
                    if mooc_file is not None:
                        cert.file = mooc_file
                        cert.is_mooc = True
                        cert.user = request.user
                        cert.title = request.POST.get('mooc-title')
                        cert.description = request.POST.get('mooc-description')
                        cert.save()
                    else:
                        return HttpResponse("No file uploaded")
                    # if file.mooc_course is not None:
                    #     file.mooc_course.delete()
                    file.mooc_course = cert
                    file.save()
                else:
                    # if file.mooc_course is not None:
                    #     file.mooc_course.delete()
                    file.mooc_course = None
                    file.save()

        return render(request, "html/faculty/science/additional-entry.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def review(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'faculty-review'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        if file is not None:
            context['file'] = file

        return render(request, "html/faculty/science/review.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def result(request):
        from Account.models import DualRole
        from MasterConfiguration.models import StaffMarkOverride
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        file = FacultyHelperFunctions.get_appraisal_file(request)
        context = {'user': request.user, 'page_name': 'faculty-result', 'file': file,
                   'cycle': FacultyHelperFunctions.get_cycle()}
        if not context['cycle'].get('show_result'):
            context['error_code'] = "Result Error"
            context['error_message'] = "Result not yet available."
            return render(request, "html/error_pages/pages-error.html", context)
        engine = CalculationEngine(file)
        context['teaching'] = engine.calculateTeachingMaster()
        context['engine'] = engine
        context['engineR2'] = CalculationEngineR2(file)
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['file'] = file
        context['can_submit'] = file.ro2_validator.is_valid_for_ro(
            file.user.designation_abbreviation == 'assistant_prof_on_contract') and file.file_level == 'HR'

        dr = DualRole.objects.filter(faculty_profile=request.user).first()
        if dr is not None:
            dr = dr.get_appraisal_files()
        overriden = StaffMarkOverride.objects.filter(user=request.user).first()
        if overriden is not None:
            overriden = overriden.get_appraisal_files()
        dual_role_data = overriden or dr
        if dual_role_data:
            staff_file = dual_role_data['staff_file']
            faculty_file = dual_role_data['faculty_file']
            final_percentage = round(staff_file.total_marks.ro2 * 0.4 + faculty_file.r2_percentage * 0.6 + 0.1, 0)
            if final_percentage >= 95:
                final_grade = 'OUTSTANDING'
            elif final_percentage >= 65:
                final_grade = 'GOOD'
            elif final_percentage >= 35:
                final_grade = 'AVERAGE'
            else:
                final_grade = 'BELOW AVERAGE'
            context['dual_role'] = {
                'full_name': faculty_file.user.full_name,
                'staff_username': staff_file.user.username,
                'faculty_username': faculty_file.user.username,
                'staff_ro1_marks': staff_file.total_marks.ro1,
                'staff_ro2_marks': staff_file.total_marks.ro2,
                'staff_ro1_grade': staff_file.grade_received_ro1,
                'staff_ro2_grade': staff_file.grade_received_ro2,
                'staff_r2_percentage_100': staff_file.total_marks.ro2,
                'faculty_ro1_marks': faculty_file.grand_total.ro1,
                'faculty_ro2_marks': faculty_file.grand_total.ro2,
                'faculty_ro1_grade': faculty_file.r1_grade,
                'faculty_ro2_grade': faculty_file.r2_grade,
                'faculty_r2_percentage_100': faculty_file.r2_percentage,
                'staff_percentage_40': round(staff_file.total_marks.ro2 * 0.4, 2),
                'faculty_percentage_60': round(faculty_file.r2_percentage * 0.6, 2),
                'final_percentage': final_percentage,
                'final_grade': final_grade
            }
        return render(request, "html/faculty/science/result.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def submit(request):
        if not FacultyHelperFunctions.check_authorized_user(request):
            context = {
                'error_code': "Unauthorized Error",
                "error_message": "You are not authorized to view this page."
            }
            return render(request, "html/error_pages/pages-error.html", context)

        context = {'user': request.user, 'page_name': 'faculty-submit'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['cycle'] = FacultyHelperFunctions.get_cycle()
        context['can_submit'] = file.validator.is_valid(request.user.designation_abbreviation == 'assistant_prof_on_contract')
        print(request.user.designation_abbreviation == 'assistant_prof_on_contract')
        if file is not None:
            context['file'] = file
        if request.method == 'POST':
            file.file_level = 'RO1'
            file.save()
        return render(request, "html/faculty/science/submit.html", context)

    @staticmethod
    @login_required(login_url='/login/')
    def summary(request):
        context = {'user': request.user, 'page_name': 'faculty-download'}
        file = FacultyHelperFunctions.get_appraisal_file(request)
        context['file'] = file
        context['books'] = file.textbooks.all().union(file.research_books.all())
        context['external_guidance'] = file.phd_guidance.filter(category='external')
        context['internal_guidance'] = file.phd_guidance.filter(category='internal')
        return render(request, "html/faculty/science/download.html", context)


class FacultyHelperFunctions:
    @staticmethod
    def check_authorized_user(request):
        print(request.user.roles)
        if request.user.is_authenticated and request.user.is_active and request.user.roles == 'fac' and ScienceFacultyAppraisalCycleInclusion.check_inclusion(request.user):
            return True
        else:
            return False

    @staticmethod
    def get_appraisal_file(request) -> ScienceAssistantProfOnContractAppraisalFile | ScienceAssistantProfAppraisalFile | ScienceAssociateProfAppraisalFile | ScienceProfAppraisalFile:
        try:
            file = None
            if request.user.designation_abbreviation == 'assistant_prof_on_contract':
                try:
                    file = ScienceAssistantProfOnContractAppraisalFile.objects.get(user=request.user)
                except ScienceAssistantProfOnContractAppraisalFile.DoesNotExist:
                    file = ScienceAssistantProfOnContractAppraisalFile()
                    file.user = request.user
                    file.configuration = ScienceGoalSheetAssistantProfOnContract.objects.filter(is_active=True).first()
                    file.save()
            elif request.user.designation_abbreviation == 'assistant_prof':
                try:
                    file = ScienceAssistantProfAppraisalFile.objects.get(user=request.user)
                except ScienceAssistantProfAppraisalFile.DoesNotExist:
                    file = ScienceAssistantProfAppraisalFile()
                    file.user = request.user
                    file.configuration = ScienceGoalSheetAssistantProf.objects.filter(is_active=True).first()
                    file.save()
            elif request.user.designation_abbreviation == 'associate_prof':
                try:
                    file = ScienceAssociateProfAppraisalFile.objects.get(user=request.user)
                except ScienceAssociateProfAppraisalFile.DoesNotExist:
                    print("hi")
                    file = ScienceAssociateProfAppraisalFile()
                    file.user = request.user
                    file.configuration = ScienceGoalSheetAssociateProf.objects.filter(is_active=True).first()
                    file.save()
            elif request.user.designation_abbreviation == 'prof':
                try:
                    file = ScienceProfAppraisalFile.objects.get(user=request.user)
                except ScienceProfAppraisalFile.DoesNotExist:
                    file = ScienceProfAppraisalFile()
                    file.user = request.user
                    file.configuration = ScienceGoalSheetProf.objects.filter(is_active=True).first()
                    file.save()
            return file
        except Exception as e:
            raise Exception("Error in getting appraisal file: " + str(e))

    @staticmethod
    def get_cycle():
        try:
            config = ScienceFacultyAppraisalCycleConfiguration.objects.filter(is_active=True).first()
            print(config.get_cycle())
            return {'name': config.get_cycle(), 'config': config, 'current_date': CurrentDate.objects.first().date,
                    'show_result': ShowResult.objects.first().show_result}
        except ScienceFacultyAppraisalCycleConfiguration.DoesNotExist:
            return HttpResponse("Problem while fetching cycles")

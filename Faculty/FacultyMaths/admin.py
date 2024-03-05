from django.contrib import admin

from Faculty.FacultyMaths.models import *


# Register your models herEM


class MathGoalSheetModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'is_active']
    list_filter = ['id', 'year', 'is_active']
    search_fields = ['id', 'year']
    list_per_page = 25
    fieldsets = (
        ('General Configuration', {
            'fields': ('year', 'is_active', 'grand_total'),
        }),
        ('PART A', {
            'fields': ('part_a_total', 'section_1_minimum_marks', 'section_1_maximum_marks', 'section_2_subtotal'),
        }),
        ('Part A > SECTION 1: Teaching', {
            'fields': (
                'teaching_load_upper_limit', 'teaching_load_lower_limit', 'teaching_load_t_coefficient',
                'teaching_load_minimum_marks', 'students_feedback_s_coefficient', 'students_feedback_lower_limit',
                'modern_methods_of_teaching_max_marks', 'upkeep_of_course_files_max_marks',
                'inclusion_of_alumni_max_marks', 'section_1d_max_marks',
                'timely_invigilation', 'paper_setting', 'evaluation', 'result_submission',
                'section_1e_i_per_book_per_author', 'section_1e_i_per_chapter',
                'section_1e_ii_per_international_book_per_author', 'section_1e_ii_per_national_book_per_author',
                'section_1e_ii_per_chapter')
        }),
        ('Part A > SECTION 2 A: Research And Publications/Patents', {
            'fields': (
                'section_2a_a_i_per_scopus_q1', 'section_2a_a_i_per_scopus_q2', 'section_2a_a_i_per_scopus_q3',
                'section_2a_a_i_per_scopus_q4', 'section_2a_a_i_per_wos',
                'section_2a_a_ii_per_scopus_q1', 'section_2a_a_ii_per_scopus_q2', 'section_2a_a_ii_per_scopus_q3',
                'section_2a_a_ii_per_scopus_q4',
                'section_2a_a_ii_per_wos', 'section_2a_b_per_e_publication', 'section_2a_b_max_marks',
                'section_2a_c_category_a_per_pi', 'section_2a_c_category_a_per_co_pi',
                'section_2a_c_category_b_per_pi', 'section_2a_c_category_b_per_co_pi', 'section_2a_c_category_c_per_pi',
                'section_2a_c_category_c_per_co_pi',
                'section_2a_c_category_d_per_pi', 'section_2a_c_category_d_per_co_pi', 'section_2a_c_category_e_per_pi',
                'section_2a_c_category_e_per_co_pi',
                'section_2a_c_category_f_per_pi', 'section_2a_c_category_f_per_co_pi', 'section_2a_c_category_g_per_pi',
                'section_2a_c_category_g_per_co_pi',
                'section_2a_c_category_h_per_pi', 'section_2a_c_category_h_per_co_pi',
                'section_2a_c_category_institutional_projects',
                'section_2a_c_category_osrp_student_research_project',)
        }),
        ('Part A > SECTION 2 B: PhD Guidance', {
            'fields': ('section_2b_phd_guidance_awarded', 'section_2b_phd_guidance_synopsis_submitted',
                       'section_2b_phd_guidance_under_progress'),
        }),
        ('Part A > SECTION 2 C: Dissertation/Thesis', {
            'fields': (
                'section_2c_i_marks_per_dissertation_awarded', 'section_2c_i_max_dissertation',
                'section_2c_ii_marks_per_thesis_submitted',
                'section_2c_ii_marks_per_thesis_submitted_and_patent_granted',
                'section_2c_ii_marks_per_thesis_submitted_and_papers_published'),
        }),
        ('Part A > SECTION 2 D: Patents/Inventions leading to patents', {
            'fields': (
            'section_2d_patent_granted_and_licensed', 'section_2d_patent_granted', 'section_2d_patent_published',
            'section_2d_patent_filed',
            'section_2d_faculty_advisor_to_student'),
        }),
        ('Part A > SECTION 2 E: Recognition/Awards received', {
            'fields': ('section_2e_recognition_awards_received_max_marks', 'section_2e_international_level',
                       'section_2e_national_level', 'section_2e_state_level',
                       'section_2e_regional_university_level'),
        }),
        ('Part A > SECTION 2 F: Providing Consultancy/ Organizing MDPs , EDPs ...', {
            'fields': ('section_2f_providing_consultancy', 'section_2f_industry_collaboration_project'),
        }),
        ('Part A > SECTION 2 G: Academia Collaboration (University/ Societies/ Research Organization)', {
            'fields': (
            'section_2g_academia_collaboration_max_marks', 'section_2g_mou_signed', 'section_2g_faculty_contribution'),
        }),
        ('Part A > SECTION 3: Administrative Activities', {
            'fields': ('section_3_subtotal',),
        }),
        ('Part A > SECTION 3 A: Arranging Conferences/ Seminars/Conclaves', {
            'fields': ('section_3a_arranging_conferences_max_marks',),
        }),
        ('Part A > SECTION 3 B: Being Mentor to students(providing Career/Academic counselling)', {
            'fields': ('section_3b_mentor_to_students_max_marks',),
        }),
        ('Part A > SECTION 4: Extended Activities', {
            'fields': (),
        }),
        ('Part A > SECTION 4 A: Arranging Conferences/Seminars', {
            'fields': (
            'section_4a_arranging_conferences_max_marks', 'section_4a_arranging_conferences_marks_per_conference'),
        }),
        ('Part A > SECTION 4 B: Community Development Initiatives', {
            'fields': ('section_4b_community_development_initiatives_max_marks',),
        }),
        ('Part A > SECTION 4 C: Involvement in Extra curricular/ Co- curricular activities', {
            'fields': ('section_4c_involvement_in_extra_curricular_activities_max_marks',),
        }),

        ('Part B', {
            'fields': ('part_b_total',),
        }),

        ('Part B > SECTION 1: SENIOR FEEDBACK', {
            'fields': (
            'senior_feedback_outstanding_marks', 'senior_feedback_good_marks', 'senior_feedback_average_marks',
            'senior_feedback_unsatisfactory_marks',),
        }),
        ('Part B > SECTION 2: Self Development', {
            'fields': (
            'self_development_outstanding_marks', 'self_development_good_marks', 'self_development_average_marks',
            'self_development_unsatisfactory_marks',
            'self_development_mooc_course_marks',),
        }),
        ('Part B > SECTION 3: Ability to take and successfully execute additional responsibilities', {
            'fields': ('additional_responsibilities_outstanding_marks', 'additional_responsibilities_good_marks',
                       'additional_responsibilities_average_marks',
                       'additional_responsibilities_unsatisfactory_marks',),
        }),
    )


class AwardModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['awardee']
    list_display = ('awardee', 'year', 'award_type', 'description')
    list_filter = ('year', 'awardee', 'award_type')


class CollabModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['faculty']


class PatentModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['innovator']


class PublicationModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['author']


class PaperModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['author']


class ProjectModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['innovator']
    list_display = ['innovator', 'description', 'status', 'funding_agency', 'funds_received', 'project_participation',
                    'project_category', 'month', 'year']
    list_filter = ['status', 'project_participation', 'project_category', 'month', 'year']
    search_fields = ['innovator__email', 'description', 'funding_agency']
    fieldsets = (
        ('General', {
            'fields': ('innovator', 'description', 'status', 'project_participation', 'project_category')
        }),
        ('Funding', {
            'fields': ('funding_agency', 'funds_received')
        }),
        ('Timeline', {
            'fields': ('month', 'year')
        }),
    )


class PhDGuidanceModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['faculty']


class BachelorsDissertationModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['faculty']


class MastersDissertationModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['faculty']


class FacultyAdvisorModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['faculty']


class GenericMarkedParameterModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['appraisee']


class AcademiaCollaborationModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['appraisee']


class CertificationModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


class AppraisalFileModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user', ]
    filter_horizontal = ['research_books', 'textbooks', 'publications_in_scopus_wos',
                         'conference_proceedings_scopus_wos', 'e_publications_articles', 'projects', 'phd_guidance',
                         'recognition_awards', 'providing_consultancy', 'industry_collaboration',
                         'arranging_conferences', 'being_mentor', 'attending_conferences', 'community_development',
                         'self_development_trainings']


admin.site.register(MathGoalSheetAssistantProfOnContract)  # , MathGoalSheetModelAdmin)
admin.site.register(MathGoalSheetAssistantProf)  # , MathGoalSheetModelAdmin)
admin.site.register(MathGoalSheetAssociateProf)  # , MathGoalSheetModelAdmin)
admin.site.register(MathGoalSheetProf)  # , MathGoalSheetModelAdmin)
admin.site.register(MarkField)
admin.site.register(Award, AwardModelAdmin)
admin.site.register(Collaboration, CollabModelAdmin)
# admin.site.register(Patent, PatentModelAdmin)
admin.site.register(Publication, PublicationModelAdmin)
admin.site.register(Paper, PaperModelAdmin)
admin.site.register(Project, ProjectModelAdmin)
admin.site.register(PhDGuidance, PhDGuidanceModelAdmin)
# admin.site.register(BachelorsDissertation, BachelorsDissertationModelAdmin)
# admin.site.register(MastersDissertation, MastersDissertationModelAdmin)
admin.site.register(FacultyAdvisor, FacultyAdvisorModelAdmin)
admin.site.register(GenericMarkedParameter, GenericMarkedParameterModelAdmin)
admin.site.register(AcademiaCollaboration, AcademiaCollaborationModelAdmin)
admin.site.register(Certification, CertificationModelAdmin)
admin.site.register(MathAssistantProfOnContractAppraisalFile)  # , AppraisalFileModelAdmin)
admin.site.register(MathAssistantProfAppraisalFile)  # , AppraisalFileModelAdmin)
admin.site.register(MathAssociateProfAppraisalFile)  # , AppraisalFileModelAdmin)
admin.site.register(MathProfAppraisalFile)  # , AppraisalFileModelAdmin)
admin.site.register(ExamDuty)
admin.site.register(ModernMethods)
admin.site.register(TeachingLoad)
admin.site.register(FacultyValidator)
admin.site.register(Consultancy)

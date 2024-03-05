from django.db import models
from Faculty.FacultySLS.models.goalsheets import FOLSGoalSheetProf
from datetime import datetime


class FOLSProfAppraisalFile(models.Model):
    file_levels = (
        ('APPRAISEE', "APPRAISEE"),
        ('RO1', "Reporting Officer (RO)"),
        ('RO2', "Reviewing Officer (RV)"),
    )
    file_level = models.CharField(max_length=10, default="APPRAISEE", choices=file_levels)
    configuration = models.ForeignKey(FOLSGoalSheetProf, on_delete=models.PROTECT)
    user = models.ForeignKey('Account.User', on_delete=models.PROTECT)
    validator = models.ForeignKey('FacultySLS.FacultyValidator', on_delete=models.CASCADE, null=True, blank=True, related_name='sls_prof_validator')

    ro1_validator = models.ForeignKey('FacultySLS.FacultyValidator', on_delete=models.CASCADE, null=True, blank=True, related_name='sls_prof_r1_validator')
    ro2_validator = models.ForeignKey('FacultySLS.FacultyValidator', on_delete=models.CASCADE, null=True, blank=True, related_name='sls_prof_r2_validator')

    is_assistant_prof_on_contract = models.BooleanField(default=True)

    # Main Fields
    year = models.IntegerField(default=datetime.now().year)
    grand_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_grand_total', null=True, blank=True)
    grade_options = (
        ('OUTSTANDING', "OUTSTANDING"),
        ('GOOD', "GOOD"),
        ('AVERAGE', "AVERAGE"),
        ('BELOW AVERAGE', "BELOW AVERAGE"),
    )
    r1_percentage = models.FloatField(null=True, blank=True)
    r2_percentage = models.FloatField(null=True, blank=True)
    r1_grade = models.CharField(max_length=20, null=True, blank=True, choices=grade_options)
    r2_grade = models.CharField(max_length=20, null=True, blank=True, choices=grade_options)

    has_verified_data = models.BooleanField(default=False)
    # PART A
    part_a_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_part_a_total', null=True, blank=True)

    # PART A > SECTION 1 (TEACHING)
    part_a_section_1_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_part_a_section_1_total', null=True, blank=True)

    # PART A > SECTION 1 > SUBSECTION A (TEACHING)
    teaching_load = models.ForeignKey('FacultySLS.TeachingLoad', on_delete=models.CASCADE, related_name='sls_prof_teaching_load', null=True, blank=True)

    # PART A > SECTION 1 > SUBSECTION B (Student Feedback)
    student_feedback = models.FloatField(null=True, blank=True)
    student_feedback_marks = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_student_feedback_marks', null=True, blank=True)

    # PART A > SECTION 1 > SUBSECTION C (Modern Teaching Methods)
    modern_teaching_methods = models.ForeignKey('FacultySLS.ModernMethods', on_delete=models.CASCADE, related_name='sls_prof_modern_teaching_methods', null=True,
                                                blank=True)
    upkeep_of_course_files = models.TextField(null=True, blank=True)
    upkeep_of_course_files_marks = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE,
                                                     related_name='prof_upkeep_of_course_files_marks', null=True,
                                                     blank=True)
    inclusion_of_alumni = models.TextField(null=True, blank=True)
    inclusion_of_alumni_marks = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE,
                                                  related_name='prof_inclusion_of_alumni_marks', null=True, blank=True)

    # PART A > SECTION 1 > SUBSECTION D (Exam Duty)
    exam_duty = models.ForeignKey('FacultySLS.ExamDuty', on_delete=models.CASCADE, related_name='sls_prof_exam_duty_total_marks', null=True, blank=True)

    # PART A > SECTION 1 > SUBSECTION E (Books and Publications)
    books_and_publications_marks = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_books_and_publications_marks', null=True,
                                                     blank=True)
    research_books = models.ManyToManyField('FacultySLS.Publication', related_name='sls_prof_research_books', blank=True)
    literary_books = models.ManyToManyField('FacultySLS.Publication', related_name='sls_prof_literary_books', blank=True)
    textbooks = models.ManyToManyField('FacultySLS.Publication', related_name='sls_prof_textbook', blank=True)

    # PART A > SECTION 2 (Research and Publication/Patents)
    part_a_section_2_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_part_a_section_2_total', null=True, blank=True)

    # PART A > SECTION 2 > SUBSECTION A (Research and Publication)
    part_a_section_2a_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_part_a_section_2a_total', null=True, blank=True)
    publications_in_scopus_wos = models.ManyToManyField('FacultySLS.Paper', related_name='sls_prof_publications_in_scopus_wos', blank=True)
    publications_in_sci_ugc = models.ManyToManyField('FacultySLS.Paper', related_name='sls_prof_publications_in_sci_ugc', blank=True)
    conference_proceedings_scopus_wos = models.ManyToManyField('FacultySLS.Paper', related_name='sls_prof_conference_proceedings_scopus_wos', blank=True)
    e_publications_articles = models.ManyToManyField('FacultySLS.Paper', related_name='sls_prof_e_publications_articles', blank=True)
    projects = models.ManyToManyField('FacultySLS.Project', related_name='sls_prof_projects', blank=True)
    projects_total_marks = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_projects_total_marks', null=True, blank=True)

    # PART A > SECTION 2 > SUBSECTION B (PhD Guidance)
    external_phd_guidance_available = models.BooleanField(default=True)
    phd_guidance_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_phd_guidance_total', null=True, blank=True)
    phd_guidance = models.ManyToManyField('FacultySLS.PhDGuidance', related_name='sls_prof_phd_guidance', blank=True)
    # TODO: Check foet goalsheet row 50

    # PART A > SECTION 2 > SUBSECTION C (Dissertation)
    dissertation_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_dissertation_total', null=True, blank=True)

    bachelors_dissertation_available = models.BooleanField(default=True)
    bachelors_dissertation_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_bachelors_dissertation_total', null=True,
                                                     blank=True)
    bachelors_dissertation = models.ManyToManyField('FacultySLS.BachelorsDissertation', related_name='sls_prof_bachelors_dissertation', blank=True)

    masters_thesis_available = models.BooleanField(default=True)
    masters_thesis_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_masters_thesis_total', null=True, blank=True)
    masters_thesis = models.ManyToManyField('FacultySLS.MastersDissertation', related_name='sls_prof_masters_thesis', blank=True)

    # # PART A > SECTION 2 > SUBSECTION D (Patents)
    # patents_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_patents_total', null=True, blank=True)
    # patents = models.ManyToManyField('FacultySLS.Patent', related_name='sls_prof_patents', blank=True)
    # # only for Assistant Professor on Contract
    # faculty_advisor_available = models.BooleanField(default=True)
    # faculty_advisor_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_faculty_advisor_total', null=True, blank=True)
    # faculty_advisor = models.ManyToManyField('FacultySLS.FacultyAdvisor', related_name='sls_prof_faculty_advisor', blank=True)

    # PART A > SECTION 2 > SUBSECTION E (Recognition/Awards received)
    recognition_awards_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_recognition_awards_total', null=True,
                                                 blank=True)
    recognition_awards = models.ManyToManyField('FacultySLS.Award', related_name='sls_prof_recognition_awards', blank=True)

    # PART A > SECTION 2 > SUBSECTION F (Providing Consultancy/ Organizing MDPs , EDPs as Chief Coordinator/ Program Head services on the behalf of University)
    providing_consultancy_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_providing_consultancy_total', null=True,
                                                    blank=True)
    providing_consultancy = models.ManyToManyField('FacultySLS.Consultancy', related_name='sls_prof_providing_consultancy', blank=True)
    # ------------------  OR (Only for Assistant Prof. On Contract)  ------------------
    # Industry Collaboration (Academia-Industry Connect)
    # • Project in collaboration with Industry
    # • Conducting a Workshop/Seminar in collaboration with Industry
    industry_collaboration_available = models.BooleanField(default=True)
    industry_collaboration_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_industry_collaboration_total', null=True,
                                                     blank=True)
    industry_collaboration = models.ManyToManyField('FacultySLS.Collaboration', related_name='sls_prof_industry_collaboration', blank=True)

    # PART A > SECTION 2 > SUBSECTION G (Academia Collaboration (University/ Societies/ Research Organization)
    academia_collaboration_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_academia_collaboration_total', null=True,
                                                     blank=True)
    academia_collaboration = models.ForeignKey('FacultySLS.AcademiaCollaboration', on_delete=models.CASCADE, related_name='sls_prof_academia_collaboration', null=True,
                                               blank=True)

    # PART A > SECTION 3 (Professional Development)
    part_a_section_3_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_part_a_section_3_total', null=True, blank=True)

    # PART A > SECTION 3 > SUBSECTION A (Arranging Conferences/ Seminars/Conclaves)
    international_admission = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_international_admission', null=True, blank=True)
    arranging_conferences_available = models.BooleanField(default=True)
    arranging_conferences_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_arranging_conferences_total', null=True,
                                                    blank=True)
    arranging_conferences = models.ManyToManyField('FacultySLS.GenericMarkedParameter', related_name='sls_prof_arranging_conferences', blank=True)

    # PART A > SECTION 3 > SUBSECTION B (Being Mentor to students(providing Career/Academic counselling)
    being_mentor_available = models.BooleanField(default=True)
    being_mentor_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_being_mentor_total', null=True, blank=True)
    being_mentor = models.ManyToManyField('FacultySLS.GenericMarkedParameter', related_name='sls_prof_being_mentor', blank=True)

    # PART A > SECTION 4
    part_a_section_4_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_part_a_section_4_total', null=True, blank=True)

    # PART A > SECTION 4 > SUBSECTION A (Attending Conference/ Seminar)
    attending_conferences_available = models.BooleanField(default=True)
    attending_conferences_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_attending_conferences_total', null=True,
                                                    blank=True)
    attending_conferences = models.ManyToManyField('FacultySLS.GenericMarkedParameter', related_name='sls_prof_attending_conferences', blank=True)

    # PART A > SECTION 4 > SUBSECTION B (Community Development Initiatives)
    community_development_available = models.BooleanField(default=True)
    community_development_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_community_development_total', null=True,
                                                    blank=True)
    community_development = models.ManyToManyField('FacultySLS.GenericMarkedParameter', related_name='sls_prof_community_development', blank=True)

    # PART A > SECTION 4 > SUBSECTION C (Involvement in Extra curricular/ Co- curricular activities)
    involvement_extra_curricular_marks = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_involvement_extra_curricular_total',
                                                           null=True,
                                                           blank=True)

    placement_duty_marks = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_placement_duty_total', null=True, blank=True)
    admission_duty_marks = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_admission_duty_total', null=True, blank=True)
    # ====================  PART B  ====================
    part_b_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_part_b_total', null=True, blank=True)

    # PART B > SECTION 1 (Senior Feedback)
    GRADE_CHOICES = (
        ('O', 'Outstanding'),
        ('G', 'Good'),
        ('A', 'Average'),
        ('U', 'Unsatisfactory'),
    )
    senior_feedback_grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    senior_feedback_grade_r2 = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    senior_feedback_marks = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_senior_feedback_marks', null=True, blank=True)

    # PART B > SECTION 2 (Self Development)
    self_development_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_self_development_total', null=True, blank=True)
    self_development_grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    self_development_grade_r2 = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    self_development_trainings = models.ManyToManyField('FacultySLS.Certification', related_name='sls_prof_self_development_trainings', blank=True)

    is_mooc_available = models.BooleanField(default=True)
    mooc_courses_total = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_mooc_courses_total', null=True, blank=True)
    mooc_course = models.ForeignKey('FacultySLS.Certification', on_delete=models.CASCADE, related_name='sls_prof_mooc_course', null=True, blank=True)

    # PART B > SECTION 3 (Ability to take and successfully execute additional responsibilities)
    GRADE_CHOICES = (
        ('O', 'Outstanding'),
        ('G', 'Good'),
        ('A', 'Average'),
        ('U', 'Unsatisfactory'),
    )
    additional_responsibilities_grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    additional_responsibilities_grade_r2 = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    additional_responsibilities_marks = models.ForeignKey('FacultySLS.MarkField', on_delete=models.CASCADE, related_name='sls_prof_additional_responsibilities_marks',
                                                          null=True,
                                                          blank=True)

    class Meta:
        verbose_name = 'FoLS Professor Appraisal File'
        verbose_name_plural = 'FoLS Professor Appraisal Files'

    def __str__(self):
        return f'{self.user} - {self.year}'

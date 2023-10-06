from Faculty.FacultyFOET.models.goalsheets import FOETGoalSheetAssistantProfOnContract
from django.db import models
from datetime import datetime


class FOETAssistantProfOnContractAppraisalFile(models.Model):
    file_levels = (
        ('APPRAISEE', "APPRAISEE"),
        ('RO1', "Reporting Officer (RO)"),
        ('RO2', "Reviewing Officer (RV)"),
        ('HR', "HR"),
    )
    file_level = models.CharField(max_length=10, default="APPRAISEE", choices=file_levels)
    configuration = models.ForeignKey(FOETGoalSheetAssistantProfOnContract, on_delete=models.PROTECT)
    user = models.ForeignKey('Account.User', on_delete=models.PROTECT)
    validator = models.ForeignKey('FacultyFOET.FacultyValidator', on_delete=models.CASCADE, null=True, blank=True, related_name='assistant_prof_on_contract_validator')

    ro1_validator = models.ForeignKey('FacultyFOET.FacultyValidator', on_delete=models.CASCADE, null=True, blank=True, related_name='assistant_prof_on_contract_r1_validator')
    ro2_validator = models.ForeignKey('FacultyFOET.FacultyValidator', on_delete=models.CASCADE, null=True, blank=True, related_name='assistant_prof_on_contract_r2_validator')

    is_assistant_prof_on_contract = models.BooleanField(default=True)

    # Main Fields
    year = models.IntegerField(default=datetime.now().year)
    grand_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='grand_total', null=True, blank=True)
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
    part_a_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='part_a_total', null=True, blank=True)

    # PART A > SECTION 1 (TEACHING)
    part_a_section_1_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='part_a_section_1_total', null=True, blank=True)

    # PART A > SECTION 1 > SUBSECTION A (TEACHING)
    teaching_load = models.ForeignKey('FacultyFOET.TeachingLoad', on_delete=models.CASCADE, related_name='teaching_load', null=True, blank=True)

    # PART A > SECTION 1 > SUBSECTION B (Student Feedback)
    student_feedback = models.FloatField(null=True, blank=True)
    student_feedback_marks = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='student_feedback_marks', null=True, blank=True)

    # PART A > SECTION 1 > SUBSECTION C (Modern Teaching Methods)
    modern_teaching_methods = models.ForeignKey('FacultyFOET.ModernMethods', on_delete=models.CASCADE, related_name='modern_teaching_methods', null=True, blank=True)

    # PART A > SECTION 1 > SUBSECTION D (Exam Duty)
    exam_duty = models.ForeignKey('FacultyFOET.ExamDuty', on_delete=models.CASCADE, related_name='exam_duty_total_marks', null=True, blank=True)

    # PART A > SECTION 1 > SUBSECTION E (Books and Publications)
    books_and_publications_marks = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='books_and_publications_marks', null=True, blank=True)
    research_books = models.ManyToManyField('FacultyFOET.Publication', related_name='research_books', blank=True)
    textbooks = models.ManyToManyField('FacultyFOET.Publication', related_name='textbook', blank=True)

    # PART A > SECTION 2 (Research and Publication/Patents)
    part_a_section_2_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='part_a_section_2_total', null=True, blank=True)

    # PART A > SECTION 2 > SUBSECTION A (Research and Publication)
    part_a_section_2a_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='part_a_section_2a_total', null=True, blank=True)
    publications_in_scopus_wos = models.ManyToManyField('FacultyFOET.Paper', related_name='publications_in_scopus_wos', blank=True)
    conference_proceedings_scopus_wos = models.ManyToManyField('FacultyFOET.Paper', related_name='conference_proceedings_scopus_wos', blank=True)
    e_publications_articles = models.ManyToManyField('FacultyFOET.Paper', related_name='e_publications_articles', blank=True)
    projects = models.ManyToManyField('FacultyFOET.Project', related_name='projects', blank=True)
    projects_total_marks = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='projects_total_marks', null=True, blank=True)

    # PART A > SECTION 2 > SUBSECTION B (PhD Guidance)
    external_phd_guidance_available = models.BooleanField(default=True)
    phd_guidance_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='phd_guidance_total', null=True, blank=True)
    phd_guidance = models.ManyToManyField('FacultyFOET.PhDGuidance', related_name='phd_guidance', blank=True)
    # TODO: Check foet goalsheet row 50

    # PART A > SECTION 2 > SUBSECTION C (Dissertation)
    dissertation_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='dissertation_total', null=True, blank=True)

    bachelors_dissertation_available = models.BooleanField(default=True)
    bachelors_dissertation_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='bachelors_dissertation_total', null=True, blank=True)
    bachelors_dissertation = models.ManyToManyField('FacultyFOET.BachelorsDissertation', related_name='bachelors_dissertation', blank=True)

    masters_thesis_available = models.BooleanField(default=True)
    masters_thesis_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='masters_thesis_total', null=True, blank=True)
    masters_thesis = models.ManyToManyField('FacultyFOET.MastersDissertation', related_name='masters_thesis', blank=True)

    # PART A > SECTION 2 > SUBSECTION D (Patents)
    patents_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='patents_total', null=True, blank=True)
    patents = models.ManyToManyField('FacultyFOET.Patent', related_name='patents', blank=True)
    # only for Assistant Professor on Contract
    faculty_advisor_available = models.BooleanField(default=True)
    faculty_advisor_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='faculty_advisor_total', null=True, blank=True)
    faculty_advisor = models.ManyToManyField('FacultyFOET.FacultyAdvisor', related_name='faculty_advisor', blank=True)

    # PART A > SECTION 2 > SUBSECTION E (Recognition/Awards received)
    recognition_awards_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='recognition_awards_total', null=True, blank=True)
    recognition_awards = models.ManyToManyField('FacultyFOET.Award', related_name='recognition_awards', blank=True)

    # PART A > SECTION 2 > SUBSECTION F (Providing Consultancy/ Organizing MDPs , EDPs as Chief Coordinator/ Program Head services on the behalf of University)
    providing_consultancy_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='providing_consultancy_total', null=True, blank=True)
    providing_consultancy = models.ManyToManyField('FacultyFOET.Consultancy', related_name='providing_consultancy', blank=True)
    # ------------------  OR (Only for Assistant Prof. On Contract)  ------------------
    # Industry Collaboration (Academia-Industry Connect)
    # • Project in collaboration with Industry
    # • Conducting a Workshop/Seminar in collaboration with Industry
    industry_collaboration_available = models.BooleanField(default=True)
    industry_collaboration_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='industry_collaboration_total', null=True, blank=True)
    industry_collaboration = models.ManyToManyField('FacultyFOET.Collaboration', related_name='industry_collaboration', blank=True)

    # PART A > SECTION 2 > SUBSECTION G (Academia Collaboration (University/ Societies/ Research Organization)
    academia_collaboration_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='academia_collaboration_total', null=True, blank=True)
    academia_collaboration = models.ForeignKey('FacultyFOET.AcademiaCollaboration', on_delete=models.CASCADE, related_name='academia_collaboration', null=True, blank=True)

    # PART A > SECTION 3 (Professional Development)
    part_a_section_3_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='part_a_section_3_total', null=True, blank=True)

    # PART A > SECTION 3 > SUBSECTION A (Arranging Conferences/ Seminars/Conclaves)
    arranging_conferences_available = models.BooleanField(default=True)
    arranging_conferences_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='arranging_conferences_total', null=True, blank=True)
    arranging_conferences = models.ManyToManyField('FacultyFOET.GenericMarkedParameter', related_name='arranging_conferences', blank=True)

    # PART A > SECTION 3 > SUBSECTION B (Being Mentor to students(providing Career/Academic counselling)
    being_mentor_available = models.BooleanField(default=True)
    being_mentor_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='being_mentor_total', null=True, blank=True)
    being_mentor = models.ManyToManyField('FacultyFOET.GenericMarkedParameter', related_name='being_mentor', blank=True)

    # PART A > SECTION 4
    part_a_section_4_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='part_a_section_4_total', null=True, blank=True)

    # PART A > SECTION 4 > SUBSECTION A (Attending Conference/ Seminar)
    attending_conferences_available = models.BooleanField(default=True)
    attending_conferences_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='attending_conferences_total', null=True, blank=True)
    attending_conferences = models.ManyToManyField('FacultyFOET.GenericMarkedParameter', related_name='attending_conferences', blank=True)

    # PART A > SECTION 4 > SUBSECTION B (Community Development Initiatives)
    community_development_available = models.BooleanField(default=True)
    community_development_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='community_development_total', null=True, blank=True)
    community_development = models.ManyToManyField('FacultyFOET.GenericMarkedParameter', related_name='community_development', blank=True)

    # PART A > SECTION 4 > SUBSECTION C (Involvement in Extra curricular/ Co- curricular activities)
    involvement_extra_curricular_marks = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='involvement_extra_curricular_total', null=True,
                                                           blank=True)

    placement_duty_marks = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='placement_duty_total', null=True, blank=True)
    admission_duty_marks = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='admission_duty_total', null=True, blank=True)
    # ====================  PART B  ====================
    part_b_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='part_b_total', null=True, blank=True)

    # PART B > SECTION 1 (Senior Feedback)
    GRADE_CHOICES = (
        ('O', 'Outstanding'),
        ('G', 'Good'),
        ('A', 'Average'),
        ('U', 'Unsatisfactory'),
    )
    senior_feedback_grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    senior_feedback_grade_r2 = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    senior_feedback_marks = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='senior_feedback_marks', null=True, blank=True)

    # PART B > SECTION 2 (Self Development)
    self_development_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='self_development_total', null=True, blank=True)
    self_development_grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    self_development_grade_r2 = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    self_development_trainings = models.ManyToManyField('FacultyFOET.Certification', related_name='self_development_trainings', blank=True)

    is_mooc_available = models.BooleanField(default=True)
    mooc_courses_total = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='mooc_courses_total', null=True, blank=True)
    mooc_course = models.ForeignKey('FacultyFOET.Certification', on_delete=models.CASCADE, related_name='mooc_course', null=True, blank=True)

    # PART B > SECTION 3 (Ability to take and successfully execute additional responsibilities)
    GRADE_CHOICES = (
        ('O', 'Outstanding'),
        ('G', 'Good'),
        ('A', 'Average'),
        ('U', 'Unsatisfactory'),
    )
    additional_responsibilities_grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    additional_responsibilities_grade_r2 = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    additional_responsibilities_marks = models.ForeignKey('FacultyFOET.MarkField', on_delete=models.CASCADE, related_name='additional_responsibilities_marks', null=True,
                                                          blank=True)

    class Meta:
        verbose_name = 'FoET Assistant Professor On Contract Appraisal File'
        verbose_name_plural = 'FoET Assistant Professor On Contract Appraisal Files'

    def __str__(self):
        return f'{self.user} - {self.year}'


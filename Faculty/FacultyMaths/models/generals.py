import os
from datetime import datetime

from django.db import models
from Staff.models import user_directory_path


class MarkField(models.Model):
    ro1 = models.FloatField(default=0)
    ro2 = models.FloatField(default=0)
    ro1_remarks = models.TextField(null=True, blank=True)
    ro2_remarks = models.TextField(null=True, blank=True)
    ro1_agreed = models.BooleanField(default=True)
    ro2_agreed = models.BooleanField(default=True)
    ro2_agrees_with_ro1 = models.BooleanField(default=True)

    def __str__(self):
        if self.ro1 == 0 and self.ro2 == 0:
            return "Not yet marked"
        else:
            if self.ro1 == 0:
                ro1 = "NA"
            if self.ro2 == 0:
                ro2 = "NA"
            return f'{self.id}:  RO1: {self.ro1} RO2: {self.ro2}'


class TeachingLoad(models.Model):
    year = models.IntegerField(default=datetime.now().year)
    semester_odd = models.FloatField(default=0)
    semester_even = models.FloatField(default=0)
    semester_third = models.FloatField(default=0)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_teaching_load')


class ModernMethods(models.Model):
    flip_classes = models.TextField(null=True, blank=True)
    case_study = models.TextField(null=True, blank=True)
    technology_integration = models.TextField(null=True, blank=True)
    design_thinking = models.TextField(null=True, blank=True)
    project_based_teaching = models.TextField(null=True, blank=True)
    other = models.TextField(null=True, blank=True)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_modern_methods')


class ExamDuty(models.Model):
    year = models.IntegerField(default=datetime.now().year)
    timely_invigilation = models.FloatField(null=True, blank=True)
    paper_setting = models.FloatField(null=True, blank=True)
    evaluation = models.FloatField(null=True, blank=True)
    result_submission = models.FloatField(null=True, blank=True)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_exam_duty')


class Publication(models.Model):
    choices_pub = (
        ('book', 'Book'),
        ('book_chapter', 'Book Chapter'),
        # ('edited_book', 'Edited Book'),
        ('edited_book_chapter', 'Edited Book Chapter'),
    )

    category_choices = (
        ('research', 'Research Book'),
        ('textbook', 'Text Book'),
    )

    level = (
        ('national', 'National'),
        ('international', 'International'),
    )

    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=0)
    type = models.CharField(max_length=100, blank=True, null=True, choices=choices_pub)
    category = models.CharField(max_length=50, blank=True, null=True, choices=category_choices)
    publication_level = models.CharField(max_length=50, blank=True, null=True, choices=level)
    title = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=100, blank=True, null=True)
    is_main_author = models.BooleanField(default=False)
    co_author_count = models.IntegerField(default=0)
    author = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_pub_author')
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_publication')

    def __str__(self):
        return f'{self.author} - {self.category} | {self.type} - {self.title}'

    def get_choices_pub_name(self):
        return dict(self.choices_pub)[self.type]

    def get_category_name(self):
        return dict(self.category_choices)[self.category]

    def get_level_name(self):
        return dict(self.level)[self.publication_level]


class Paper(models.Model):
    choices_publication = (
        ('journal', 'Journal'),
        ('conference', 'Conference'),
        ('epub', 'E-Publication'),
        ('article', 'Article'),
    )
    level = (
        ('national', 'National'),
        ('international', 'International'),
    )

    author_choices = (
        ('main', 'Main Author'),
        ('co', 'Co-Author'),
    )

    paper_quality = (
        ('q1', 'Q1'),
        ('q2', 'Q2'),
        ('q3', 'Q3'),
        ('q4', 'Q4'),
    )

    category_choices = (
        ('scopus', 'Scopus'),
        ('wos', 'Web of Science'),
        ('other', 'Other'),
    )

    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=0)
    paper_type = models.CharField(max_length=100, blank=True, null=True, choices=choices_publication)
    title = models.TextField(blank=True, null=True)
    entity_name = models.TextField(blank=True, null=True)
    quality = models.CharField(max_length=100, blank=True, null=True, choices=paper_quality)
    isbn = models.CharField(max_length=100, blank=True, null=True)
    conference_organization = models.TextField(blank=True, null=True)
    conference_level = models.CharField(max_length=100, blank=True, null=True, choices=level)
    is_main_author = models.BooleanField(default=False)
    co_author_count = models.IntegerField(default=0)
    category = models.CharField(max_length=100, blank=True, null=True, choices=category_choices)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_paper')
    author = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_paper_author')

    def __str__(self):
        return f'{self.id} - {self.quality} - {self.title}'

    def get_category_name(self):
        return dict(self.category_choices)[self.category]


class Project(models.Model):
    category_choices = (
        ('MAJOR', 'Above 10 Lakhs'),
        ('MEDIUM', 'Above 5 Lakhs'),
        ('MINOR', 'Above 50000'),
        ('INS', 'Institutional'),
        ('OSRP', 'OSRP Student Research Project'),
    )

    participation_choices = (
        ('pi', 'Principal Investigator'),
        ('copi', 'Co-Principal Investigator'),
    )

    status_choices = (
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )

    month = models.IntegerField(default=0)
    year = models.IntegerField(default=datetime.now().year)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=status_choices, blank=True, null=True)
    funding_agency = models.CharField(max_length=200, blank=True, null=True)
    funds_received = models.FloatField(default=0)
    project_participation = models.CharField(max_length=100, blank=True, null=True, choices=participation_choices)
    project_category = models.CharField(max_length=100, blank=True, null=True, choices=category_choices)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_project')
    innovator = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_project_innovator')

    def calculate_category(self, funds):
        if not self.project_category == 'INS' or not self.project_category == 'OSRP':
            if funds >= 500000:
                return 'MAJOR'
            elif funds >= 300000:
                return 'MEDIUM'
            elif funds >= 25000:
                return 'MINOR'
            else:
                raise Exception('Invalid Funds')

    def get_category_name(self):
        return dict(self.category_choices)[self.project_category]

    def get_participation_name(self):
        return dict(self.participation_choices)[self.project_participation]


class PhDGuidance(models.Model):
    choices_status = (
        ('awarded', 'Awarded'),
        ('synopsis', 'Synopsis Submitted'),
        ('ongoing', 'Under Progress'),
        ('other', 'Other'),
    )

    category_choices = (
        ('internal', 'Internal'),
        ('external', 'External'),
    )

    year = models.IntegerField(default=datetime.now().year)
    # month = models.IntegerField(default=0)
    student_name = models.TextField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=choices_status, blank=True, null=True)
    scopus_publications = models.IntegerField(null=True, blank=True, verbose_name='Scopus Publications (Only for External)')
    category = models.CharField(max_length=100, choices=category_choices, blank=True, null=True)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_phd')
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_phd_faculty')

    def get_status_name(self):
        return dict(self.choices_status)[self.status]


# class BachelorsDissertation(models.Model):
#     year = models.IntegerField(default=datetime.now().year)
#     month = models.IntegerField(default=0)
#     description = models.TextField(blank=True, null=True)
#     student_name = models.CharField(max_length=200, blank=True, null=True)
#     is_awarded = models.BooleanField(default=False)
#     marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_btech')
#     faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_btech_faculty')


class MastersDissertation(models.Model):
    status_choices = (
        ('submitted', 'Submitted'),
        ('submitted_patent_published', 'Submitted and Patent Published / Granted'),
        ('submitted_patent_papers_published', 'Submitted and Patent Granted/Published Papers Published'),
    )
    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    student_name = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=status_choices)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_mtech')
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_mtech_faculty')

    def get_status_name(self):
        return dict(self.status_choices)[self.status]


class Patent(models.Model):
    choices = (
        ('filed', 'Filed'),
        ('published', 'Published'),
        ('granted', 'Granted'),
        ('licensed', 'Granted & Licensed'),
    )

    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=0)
    status = models.CharField(max_length=100, blank=True, null=True, choices=choices)
    title = models.TextField(blank=True, null=True)
    application_no = models.CharField(max_length=100, blank=True, null=True)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_patent')
    innovator = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_patent_innovator')

    def __str__(self):
        return f'{self.status} - {self.title}'


class FacultyAdvisor(models.Model):
    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=0)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_faculty_advisor')
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_faculty_advisor_faculty')


class Award(models.Model):
    award_choices = (
        ('international', 'International'),
        ('national', 'National'),
        ('state', 'State'),
        ('regional', 'Regional'),
        ('university', 'University'),
    )

    year = models.IntegerField(default=datetime.now().year)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    award_type = models.CharField(max_length=100, blank=True, null=True, choices=award_choices)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_award')
    awardee = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_award_awardee')

    def __str__(self):
        return f'{self.award_type} - {self.description}'


class Consultancy(models.Model):
    consultancy_choices = (
        ('consultancy_edp_mdp', 'Consultancy, EDP, MDP'),
    )

    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField(default=0)
    consultancy_type = models.CharField(max_length=100, blank=True, null=True, choices=consultancy_choices)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_consultancy')
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_consultancy_faculty')

    def __str__(self):
        return f'{self.consultancy_type} - {self.description}'


class Collaboration(models.Model):
    collaboration_choices = (
        ('industry', 'Industry Collaboration'),
    )

    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=0)
    collaboration_type = models.CharField(max_length=100, blank=True, null=True, choices=collaboration_choices, auto_created=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField(default=0)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_collaboration')
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_collaboration_faculty')

    def __str__(self):
        return f'{self.collaboration_type} - {self.description}'


class AcademiaCollaboration(models.Model):
    year = models.IntegerField(default=datetime.now().year)
    description = models.TextField(blank=True, null=True)
    mou_marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_academia_collaboration_mou')
    contribution_marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name="sls_contrib_marks_academia_collaboration")
    appraisee = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_academia_collaboration_appraisee')


class GenericMarkedParameter(models.Model):
    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=0)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_generic_marked_parameter')
    appraisee = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_generic_marked_parameter_appraisee')


class Certification(models.Model):
    # GRADE_CHOICES = (
    #     ('O', 'Outstanding'),
    #     ('G', 'Good'),
    #     ('A', 'Average'),
    #     ('U', 'Unsatisfactory'),
    # )
    is_mooc = models.BooleanField(default=False)
    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=0)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    # grade = models.CharField(max_length=100, choices=GRADE_CHOICES, blank=True, null=True)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='math_certification')
    user = models.ForeignKey('Account.User', on_delete=models.CASCADE, null=True, blank=True, related_name='math_certification_user')

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete()

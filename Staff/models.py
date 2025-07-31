from django.db import models


# Create your models here.


# Types Below
class StaffValidation(models.Model):
    is_parameters_approved = models.BooleanField(default=False)
    is_parameters_valid = models.BooleanField(default=False)
    is_training_valid = models.BooleanField(default=False)
    is_other_activities_valid = models.BooleanField(default=False)
    is_mooc_valid = models.BooleanField(default=False)
    is_section_2_valid = models.BooleanField(default=False)


class GradeConfiguration(models.Model):
    outstanding_from = models.FloatField()
    outstanding_to = models.FloatField()
    good_from = models.FloatField()
    good_to = models.FloatField()
    average_from = models.FloatField()
    average_to = models.FloatField()
    below_from = models.FloatField()
    below_to = models.FloatField()

    is_active = models.BooleanField(default=False)

    def __str__(self):
        if self.is_active:
            return f"{self.id}. Grade Configuration (Active)"
        return f"{self.id}. Grade Configuration"

    def get_grade(self, marks: float):
        if self.outstanding_from <= marks <= self.outstanding_to:
            return "Outstanding"
        if self.good_from <= marks <= self.good_to:
            return "Good"
        if self.average_from <= marks <= self.average_to:
            return "Average"
        if self.below_from <= marks <= self.below_to:
            return "Below Average"
        return "Invalid"


class MarkField(models.Model):
    ro1 = models.FloatField(default=0)
    ro2 = models.FloatField(default=0)
    final = models.FloatField(default=0)
    ro1_remarks = models.TextField(null=True, blank=True)
    ro2_remarks = models.TextField(null=True, blank=True)
    final_remarks = models.TextField(null=True, blank=True)
    ro2_agrees_with_ro1 = models.BooleanField(default=True)

    def __str__(self):
        if self.ro1 == 0 and self.ro2 == 0 and self.final == 0:
            return "Not yet marked"
        else:
            if self.ro1 == 0:
                ro1 = "NA"
            if self.ro2 == 0:
                ro2 = "NA"
            if self.final == 0:
                final = "NA"
            return f'RO1: {self.ro1} RO2: {self.ro2} Final: {self.final}'


class StaffConfiguration(models.Model):
    name = models.CharField(max_length=100, default='master')
    max_key_parameter = models.IntegerField(default=5)
    max_major_parameter = models.IntegerField(default=3)
    max_minor_parameter = models.IntegerField(default=2)
    max_key_parameter_marks = models.IntegerField(default=30)
    max_major_parameter_marks = models.IntegerField(default=25)
    max_minor_parameter_marks = models.IntegerField(default=10)
    max_self_development_parameter_marks = models.IntegerField(default=5)
    max_other_activities_marks = models.IntegerField(default=5)
    self_development_min_marks = models.IntegerField(default=2)
    self_development_min_trainings = models.IntegerField(default=2)
    self_development_max_trainings = models.IntegerField(default=5)
    max_productivity_marks = models.IntegerField(default=5)
    max_quality_of_work_marks = models.IntegerField(default=5)
    max_domain_expertise_marks = models.IntegerField(default=5)
    max_teamwork_marks = models.IntegerField(default=5)
    max_key_skills_marks = models.IntegerField(default=5)
    max_mooc_marks = models.IntegerField(default=5)
    disciplinary_action_deductable = models.IntegerField(default=5)

    # max_productivity_marks

    def __str__(self):
        return self.name


class Parameter(models.Model):
    parameter_index = models.IntegerField(default=-1)
    name = models.TextField(null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True)
    # marks = models.FloatField(default=0)
    ro_remakrs = models.TextField(default='', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_finalized = models.BooleanField(default=False)

    def __str__(self):
        if self.name:
            return f'{self.id}:  {self.name} + {self.value}'
        else:
            return f"{self.id}:  Unset " + str(self.parameter_index)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print('user_{0}/{1}'.format(instance.user.id, filename))
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class File(models.Model):
    filename = models.CharField(max_length=1024)
    file = models.FileField(
        upload_to=user_directory_path, null=True, blank=True)
    user = models.ForeignKey(
        'Account.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.file:
            return f'{self.file.path}'
        else:
            return "Unset " + str(self.filename)


class Certificate(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True, default='')
    approved_by_ro = models.BooleanField(default=False)
    file = models.ForeignKey(
        File, on_delete=models.CASCADE, null=True, blank=True)
    marks = models.ForeignKey(
        MarkField, on_delete=models.CASCADE, null=True, blank=True)
    is_mooc = models.BooleanField(default=False)
    is_file = models.BooleanField(default=False)
    url = models.URLField(null=True, blank=True, default='')

    def __str__(self):
        return self.name


class StaffAppraisalFile(models.Model):
    # FILE LIFE CYCLE
    # 1. APPRAISEE ENTERS ONLY KEY, MAJOR AND MINOR PARAMETERS NOT VALUES FOR THEM.
    # 2. APPRAISEE SENDS THE FILE TO RO1 FOR APPROVAL OF ONLY PARAMETERS.
    # 3. RO1 APPROVES THE PARAMETERS AND SENDS IT BACK TO APPRAISEE.
    # 4. APPRAISEE ENTERS THE VALUES FOR PARAMETERS, PART B, PART C, PART D, AND MOOC COURSE AND SENDS IT TO RO1 FOR APPROVAL.
    #    IF RO1 REJECTS A CERTAIN PARAMETER, APPRAISEE CAN EDIT THAT PARAMETER AND SEND IT BACK TO RO1.
    #    CONTINUE THIS PROCESS UNTIL RO1 APPROVES ALL PARAMETERS.
    # 5. RO1 GIVES THE MARKS, CHECKS TOTAL MARKS AND SENDS IT TO RO2.
    # 6. RO2 GIVES THE FINAL MARKS AND SENDS IT TO HR.
    # 7. HR GIVES THE FINAL APPROVAL AND SENDS IT THE REPORT TO APPRAISEE.

    # STATUS
    file_level = models.CharField(max_length=10, choices=[
        ('APPRAISEE', 'APPRAISEE'),
        ('RO1', 'RO1'),
        ('RO2', 'RO2'),
        ('HR', 'HR'),
    ])

    grade_received_ro1 = models.CharField(max_length=100, null=True, blank=True)
    grade_received_ro2 = models.CharField(max_length=100, null=True, blank=True)

    is_all_parameters_approved = models.BooleanField(default=False)

    ro1_validation = models.ForeignKey(StaffValidation, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='ro1_validation')
    ro2_validation = models.ForeignKey(StaffValidation, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='ro2_validation')

    ro1_grading_done = models.BooleanField(default=False)
    total_marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, null=True, blank=True, related_name='total_marks')
    ro2_grading_done = models.BooleanField(default=False)

    file_with = models.ForeignKey(
        'Account.User', on_delete=models.CASCADE, related_name='file_with')

    year = models.IntegerField()

    is_finalized = models.BooleanField(default=False)

    RO1_marks = models.FloatField(default=-1)
    RO2_marks = models.FloatField(default=-1)
    final_marks = models.FloatField(default=-1)

    # import configs
    # config = StaffConfiguration.objects.get(name='master')

    # User
    user = models.ForeignKey('Account.User', on_delete=models.CASCADE)

    ##########################  PART A   #######################################################
    # Performance parameters
    key_parameter = models.ManyToManyField(
        'Parameter', related_name='key_parameter')
    major_parameter = models.ManyToManyField(
        'Parameter', related_name='major_parameter')
    minor_parameter = models.ManyToManyField(
        'Parameter', related_name='minor_parameter')
    key_parameter_marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='key_parameter_marks',
                                            null=True)
    major_parameter_marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='major_parameter_marks',
                                              null=True)
    minor_parameter_marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='minor_parameter_marks',
                                              null=True)

    # Parameter Counts
    key_parameter_count = models.IntegerField(null=True)
    major_parameter_count = models.IntegerField(null=True)
    minor_parameter_count = models.IntegerField(null=True)

    # cancelled parameters
    cancelled_parameters = models.ManyToManyField('Parameter', related_name="cancelled_parameters", blank=True)

    ##########################  PART B   #######################################################
    # Self development parameters
    training_taken = models.BooleanField(default=False)
    self_development_parameter = models.ManyToManyField('Certificate', related_name='self_development_parameter',
                                                        blank=True)
    self_development_parameter_marks = models.ForeignKey(MarkField, on_delete=models.CASCADE,
                                                         related_name='self_development_parameter_marks', null=True)
    self_development_parameter_count = models.IntegerField(
        null=True, blank=True, default=0)

    ##########################  PART C   #######################################################
    # Other Activities
    other_activities_parameter = models.TextField(null=True, blank=True)
    other_activities_parameter_available = models.BooleanField(default=False)
    other_activities_parameter_marks = models.ForeignKey(MarkField, on_delete=models.CASCADE,
                                                         related_name='other_activities_parameter_marks', null=True)

    ##########################  PART D   #######################################################
    # SELF EVALUATION
    # 1. KEY HIGHLIGHTS OF THE YEAR
    key_highlights = models.TextField(null=True, blank=True)

    # 2. CHALLENGES OF THE YEAR
    challenges = models.TextField(null=True, blank=True)

    # 3. AREAS OF STRENGTH
    areas_of_strength = models.TextField(null=True, blank=True)

    # 4. AREAS OF IMPROVEMENT
    areas_of_improvement = models.TextField(null=True, blank=True)

    ##########################  MOOC   #########################################################
    was_mooc_completed = models.BooleanField(default=False)
    mooc_description = models.CharField(max_length=200, null=True, blank=True)
    mooc_file = models.ForeignKey(
        'File', on_delete=models.CASCADE, null=True, blank=True)
    mooc_marks_awarded = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='mooc_marks_awarded',
                                           null=True)
    mooc_accepted = models.BooleanField(default=False)

    ##########################  SECTION 2 (RO1 ONLY)   ##########################################

    # 1. PRODUCTIVITY IN WORK  (MAX POINTS: 5)
    productivity_marks_total = models.ForeignKey(MarkField, on_delete=models.CASCADE,
                                                 related_name='productivity_marks_total', null=True)
    # |-> 1.1. Consistency in work
    # |-> 1.2. Planning and Organization Skills
    consistency_in_work = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='consistency_in_work',
                                            null=True)
    planning_and_organization_skills = models.ForeignKey(MarkField, on_delete=models.CASCADE,
                                                         related_name='planning_and_organization_skills', null=True)
    # Total of both must be 5

    # 2. QUALITY OF WORK - ACCURACY AND THROUGHNESS OF WORK (MAX POINTS: 5)
    quality_of_work_marks_total = models.ForeignKey(MarkField, on_delete=models.CASCADE,
                                                    related_name='quality_of_work_marks_total', null=True)
    # |-> 2.1. FLEXIBILITY AND ADAPTABILITY
    # |-> 2.2. ACCURACY AND THROUGHNESS OF WORK
    flexibility_and_adaptability = models.ForeignKey(MarkField, on_delete=models.CASCADE,
                                                     related_name='flexibility_and_adaptability', null=True)
    accuracy_and_thoroughness_of_work = models.ForeignKey(MarkField, on_delete=models.CASCADE,
                                                          related_name='accuracy_and_thoroughness_of_work', null=True)

    # 3. DOMAIN OF EXPERTISE (MAX POINTS: 5)
    domain_expertise_marks_total = models.ForeignKey(
        MarkField, on_delete=models.CASCADE, null=True)
    # |-> 3.1. Awareness on process and procedure related to his/her Job Profile
    # |-> 3.2. Handling unexpected problems or Assignments
    awareness = models.ForeignKey(
        MarkField, on_delete=models.CASCADE, related_name='awareness', null=True)
    handling_unexpected_problems = models.ForeignKey(MarkField, on_delete=models.CASCADE,
                                                     related_name='handling_unexpected_problems', null=True)

    # 4. TEAMWORK (MAX POINTS: 5)
    teamwork_marks_total = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='teamwork_marks_total',
                                             null=True)
    # |-> 4.1. Positive Approach of employee towards diasagreement of senior authorities/colleagues
    # |-> 4.2. Team Spirit & Team Building Skills
    positive_approach = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='positive_approach',
                                          null=True)
    team_building_skills = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='team_building_skills',
                                             null=True)

    # 5. KEY SKILLS (MAX POINTS: 5)
    key_skills_marks_total = models.ForeignKey(MarkField, on_delete=models.CASCADE,
                                               related_name='key_skills_marks_total', null=True)
    # |-> 5.1. INTEGRITY
    # |-> 5.2. SINCERITY
    # |-> 5.3. INITIATIVE TAKING SKILLS
    # |-> 5.4. LEADERSHIP SKILLS
    # |-> 5.5. COMMUNICATION SKILLS
    integrity = models.ForeignKey(
        MarkField, on_delete=models.CASCADE, related_name='integrity', null=True)
    sincerity = models.ForeignKey(
        MarkField, on_delete=models.CASCADE, related_name='sincerity', null=True)
    initiative_taking_skills = models.ForeignKey(MarkField, on_delete=models.CASCADE,
                                                 related_name='initiative_taking_skills', null=True)
    leadership_skills = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='leadership_skills',
                                          null=True)
    communication_skills = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='communication_skills',
                                             null=True)

    # 6. DISCIPLINARY ACTION TAKE AGAINST THE EMPLOYEE (DEDUCTABLE POINTS: 5)
    disciplinary_action_marks = models.ForeignKey(MarkField, on_delete=models.CASCADE, related_name='disciplinary_action', null=True, blank=True)
    disciplinary_action = models.BooleanField(default=False)
    disciplinary_action_ro2 = models.BooleanField(default=False)
    disciplinary_action_ro2_agrees_with_ro1 = models.BooleanField(default=True)

    # Visual Customiztion
    class Meta:
        verbose_name_plural = 'Staff Appraisal Files'

    def __str__(self):
        return self.user.full_name

    def create(year: int, user):
        file = StaffAppraisalFile()
        file.year = year
        file.user = user
        file.file_with = user
        file.file_level = 'APPRAISEE'
        file.key_parameter_count = 0
        file.major_parameter_count = 0
        file.minor_parameter_count = 0
        file.save()
        for i in range(StaffConfiguration.objects.get(name='master').max_key_parameter):
            param = Parameter()
            param.parameter_index = i + 1
            param.marks = MarkField()
            param.marks.save()
            param.save()
            file.key_parameter.add(param)
        for i in range(StaffConfiguration.objects.get(name='master').max_major_parameter):
            param = Parameter()
            param.parameter_index = i + 1
            param.marks = MarkField()
            param.marks.save()
            param.save()
            file.major_parameter.add(param)
        for i in range(StaffConfiguration.objects.get(name='master').max_minor_parameter):
            param = Parameter()
            param.parameter_index = i + 1
            param.marks = MarkField()
            param.marks.save()
            param.save()
            file.minor_parameter.add(param)

        # Create a MarkField Object for every field that has a mark
        file.key_parameter_marks = MarkField()
        file.key_parameter_marks.save()

        major_parameter_marks = MarkField()
        major_parameter_marks.save()
        file.major_parameter_marks = major_parameter_marks

        minor_parameter_marks = MarkField()
        minor_parameter_marks.save()
        file.minor_parameter_marks = minor_parameter_marks

        self_development_parameter_marks = MarkField()
        self_development_parameter_marks.save()
        file.self_development_parameter_marks = self_development_parameter_marks

        other_activities_parameter_marks = MarkField()
        other_activities_parameter_marks.save()
        file.other_activities_parameter_marks = other_activities_parameter_marks

        mooc_marks_awarded = MarkField()
        mooc_marks_awarded.save()
        file.mooc_marks_awarded = mooc_marks_awarded

        pmt = MarkField()
        pmt.save()
        file.productivity_marks_total = pmt

        consistency_in_work = MarkField()
        consistency_in_work.save()
        file.consistency_in_work = consistency_in_work

        planning_and_organization_skills = MarkField()
        planning_and_organization_skills.save()
        file.planning_and_organization_skills = planning_and_organization_skills

        quality_of_work = MarkField()
        quality_of_work.save()
        file.quality_of_work_marks_total = quality_of_work

        flexibility_and_adaptability = MarkField()
        flexibility_and_adaptability.save()
        file.flexibility_and_adaptability = flexibility_and_adaptability

        accuracy_and_thoroughness_of_work = MarkField()
        accuracy_and_thoroughness_of_work.save()
        file.accuracy_and_thoroughness_of_work = accuracy_and_thoroughness_of_work

        domain_expertise_marks_total = MarkField()
        domain_expertise_marks_total.save()
        file.domain_expertise_marks_total = domain_expertise_marks_total

        awareness = MarkField()
        awareness.save()
        file.awareness = awareness

        handling_unexpected_problems = MarkField()
        handling_unexpected_problems.save()
        file.handling_unexpected_problems = handling_unexpected_problems

        teamwork_marks_total = MarkField()
        teamwork_marks_total.save()
        file.teamwork_marks_total = teamwork_marks_total

        positive_approach = MarkField()
        positive_approach.save()
        file.positive_approach = positive_approach

        team_building_skills = MarkField()
        team_building_skills.save()
        file.team_building_skills = team_building_skills

        key_skills_marks_total = MarkField()
        key_skills_marks_total.save()
        file.key_skills_marks_total = key_skills_marks_total

        integrity = MarkField()
        integrity.save()
        file.integrity = integrity

        sincerity = MarkField()
        sincerity.save()
        file.sincerity = sincerity

        initiative_taking_skills = MarkField()
        initiative_taking_skills.save()
        file.initiative_taking_skills = initiative_taking_skills

        leadership_skills = MarkField()
        leadership_skills.save()
        file.leadership_skills = leadership_skills

        communication_skills = MarkField()
        communication_skills.save()
        file.communication_skills = communication_skills

        file.ro1_validation = StaffValidation()
        file.ro1_validation.save()

        file.ro2_validation = StaffValidation()
        file.ro2_validation.save()

        f = File()
        file.mooc_file = f
        file.mooc_file.save()

        file.save()
        return file


class RollbackStaffProfile(models.Model):
    """
    This model is used to rollback the staff profile to a previous state.
    It is used when the staff profile is updated and the user wants to rollback to the previous state.
    """
    user = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='rollback_staff_profile')
    stage = models.CharField(max_length=10, choices=[
        ('RO1', 'RO1'),
        ('RO2', 'RO2'),
    ])
    reason = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.stage} - {self.timestamp}"

    def save(
        self,
        force_insert = False,
        force_update = False,
        using = None,
        update_fields = None,
    ):
        file = StaffAppraisalFile.objects.get(user=self.user)
        if self.stage == 'RO2' or self.stage == 'RO1':
            file.file_level = 'RO2'
            file.grade_received_ro2 = None
            file.ro2_grading_done = False
            file.file_with = self.user.ro2_id
        if self.stage == 'RO1':
            file.file_level = 'RO1'
            file.grade_received_ro1 = None
            file.ro1_grading_done = False
            file.file_with = self.user.ro1_id
        file.save()
        super().save(force_insert, force_update, using, update_fields)
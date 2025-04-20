import datetime

from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.


class StaffAppraisalCycleInclusion(models.Model):
    appraisee = models.ManyToManyField('Account.User', related_name='appraisee', blank=True)
    year = models.IntegerField()
    is_active = models.BooleanField(default=False)

    # def clean(self):
    #     if self.instance.pk is not None:
    #         users = self.appraisee.all()
    #         sls_users = SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         spt_users = SPTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         spm_users = SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         sot_users = SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         for user in users:
    #             if user in sls_users or user in spt_users or user in spm_users or user in sot_users:
    #                 raise ValidationError(f'User {user} already exists in another inclusion list. Please remove him/her from that list first.')

    @staticmethod
    def check_inclusion(user):
        if user in StaffAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all():
            return True
        else:
            return False

    class Meta:
        verbose_name = 'Staff Appraisal Cycle Inclusion'
        verbose_name_plural = 'Staff Appraisal Cycle Inclusion'

    def __str__(self):
        return 'Staff Cycle Inclusion | ' + str(self.year)


class SOTFacultyAppraisalCycleInclusion(models.Model):
    appraisee = models.ManyToManyField('Account.User', related_name='sot_appraisee', blank=True)
    year = models.IntegerField()
    is_active = models.BooleanField(default=False)

    # def clean(self):
    #     if self.instance.pk is not None:
    #         users = self.appraisee.all()
    #         sls_users = SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         spt_users = SPTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         spm_users = SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         staff_users = StaffAppraisalCycleInclusion.objects.filter(year=self.year).first().appraisee.all()
    #         for user in users:
    #             if user in sls_users or user in spt_users or user in spm_users or user in staff_users:
    #                 raise ValidationError(f'User {user} already exists in another inclusion list. Please remove him/her from that list first.')

    @staticmethod
    def check_inclusion(user):
        if user in SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all():
            return True
        else:
            return False

    class Meta:
        verbose_name = 'SOT Faculty Appraisal Cycle Inclusion'
        verbose_name_plural = 'SOT Faculty Appraisal Cycle Inclusion'

    def __str__(self):
        return 'SOT Faculty Cycle Inclusion | ' + str(self.year)


class SPMFacultyAppraisalCycleInclusion(models.Model):
    appraisee = models.ManyToManyField('Account.User', related_name='spm_appraisee', blank=True)
    year = models.IntegerField()
    is_active = models.BooleanField(default=False)

    # def clean(self):
    #     if self.instance.pk is not None:
    #         users = self.appraisee.all()
    #         sls_users = SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         spt_users = SPTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         sot_users = SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         staff_users = StaffAppraisalCycleInclusion.objects.filter(year=self.year).first().appraisee.all()
    #         for user in users:
    #             if user in sls_users or user in spt_users or user in sot_users or user in staff_users:
    #                 raise ValidationError(f'User {user} already exists in another inclusion list. Please remove him/her from that list first.')
    #         if self.is_active:
    #             SPMFacultyAppraisalCycleInclusion.objects.update(is_active=False)
    #             self.is_active = True

    @staticmethod
    def check_inclusion(user):
        if user in SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all():
            return True
        else:
            return False

    class Meta:
        verbose_name = 'SOEM Faculty Appraisal Cycle Inclusion'
        verbose_name_plural = 'SOEM Faculty Appraisal Cycle Inclusion'

    def __str__(self):
        return 'SPM Faculty Cycle Inclusion | ' + str(self.year)


class SLSFacultyAppraisalCycleInclusion(models.Model):
    appraisee = models.ManyToManyField('Account.User', related_name='sls_appraisee', blank=True)
    year = models.IntegerField()
    is_active = models.BooleanField(default=False)

    # def clean(self):
    #     if self.instance.pk is not None:
    #         users = self.appraisee.all()
    #         spm_users = SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         spt_users = SPTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         sot_users = SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         staff_users = StaffAppraisalCycleInclusion.objects.filter(year=self.year).first().appraisee.all()
    #         for user in users:
    #             if user in spm_users or user in spt_users or user in sot_users or user in staff_users:
    #                 raise ValidationError(f'User {user} already exists in another inclusion list. Please remove him/her from that list first.')
    #         if self.is_active:
    #             SLSFacultyAppraisalCycleInclusion.objects.update(is_active=False)
    #             self.is_active = True

    @staticmethod
    def check_inclusion(user):
        if user in SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all():
            return True
        else:
            return False

    class Meta:
        verbose_name = 'SLS Faculty Appraisal Cycle Inclusion'
        verbose_name_plural = 'SLS Faculty Appraisal Cycle Inclusion'

    def __str__(self):
        return 'SLS Faculty Cycle Inclusion | ' + str(self.year)


class MathFacultyAppraisalCycleInclusion(models.Model):
    appraisee = models.ManyToManyField('Account.User', related_name='math_appraisee', blank=True)
    year = models.IntegerField()
    is_active = models.BooleanField(default=False)

    # def clean(self):
    #     if self.instance.pk is not None:
    #         users = self.appraisee.all()
    #         spm_users = SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         sls_users = SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         sot_users = SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         for user in users:
    #             if user in spm_users or user in sls_users or user in sot_users:
    #                 raise ValidationError(f'User {user} already exists in another inclusion list. Please remove him/her from that list first.')
    #         if self.is_active:
    #             SPTFacultyAppraisalCycleInclusion.objects.update(is_active=False)
    #             self.is_active = True

    @staticmethod
    def check_inclusion(user):
        if user in MathFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all():
            return True
        else:
            return False

    class Meta:
        verbose_name = 'Maths Faculty Appraisal Cycle Inclusion'
        verbose_name_plural = 'Maths Faculty Appraisal Cycle Inclusion'

    def __str__(self):
        return 'Maths Faculty Cycle Inclusion | ' + str(self.year)


class ScienceFacultyAppraisalCycleInclusion(models.Model):
    appraisee = models.ManyToManyField('Account.User', related_name='science_appraisee', blank=True)
    year = models.IntegerField()
    is_active = models.BooleanField(default=False)

    # def clean(self):
    #     if self.instance.pk is not None:
    #         users = self.appraisee.all()
    #         spm_users = SPMFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         sls_users = SLSFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         sot_users = SOTFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all()
    #         for user in users:
    #             if user in spm_users or user in sls_users or user in sot_users:
    #                 raise ValidationError(f'User {user} already exists in another inclusion list. Please remove him/her from that list first.')
    #         if self.is_active:
    #             SPTFacultyAppraisalCycleInclusion.objects.update(is_active=False)
    #             self.is_active = True

    @staticmethod
    def check_inclusion(user):
        if user in ScienceFacultyAppraisalCycleInclusion.objects.filter(is_active=True).first().appraisee.all():
            return True
        else:
            return False

    class Meta:
        verbose_name = 'Science Faculty Appraisal Cycle Inclusion'
        verbose_name_plural = 'Science Faculty Appraisal Cycle Inclusion'

    def __str__(self):
        return 'Science Faculty Cycle Inclusion | ' + str(self.year)


class RO1List(models.Model):
    ro1_users = models.ManyToManyField('Account.User', related_name='ro1_users')

    class Meta:
        verbose_name = 'RO1 List'
        verbose_name_plural = 'RO1 List'

    def __str__(self):
        return 'RO1 List'


class RO2List(models.Model):
    ro2_users = models.ManyToManyField('Account.User', related_name='ro2_users')

    class Meta:
        verbose_name = 'RO2 List'
        verbose_name_plural = 'RO2 List'

    def __str__(self):
        return 'RO2 List'


class HRList(models.Model):
    hr_users = models.ManyToManyField('Account.User', related_name='hr_users')

    class Meta:
        verbose_name = 'HR List'
        verbose_name_plural = 'HR List'

    def __str__(self):
        return 'HR List'


class StaffAppraisalCycleConfiguration(models.Model):
    year = models.IntegerField()
    parameter_approval_start_date = models.DateField()
    parameter_approval_end_date = models.DateField()
    appraisal_start_date = models.DateField()
    appraisal_end_date = models.DateField()
    r1_approval_start_date = models.DateField()
    r1_approval_end_date = models.DateField()
    r2_approval_start_date = models.DateField()
    r2_approval_end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def clean(self, *args, **kwargs):
        # run the base validation
        super(StaffAppraisalCycleConfiguration, self).clean(*args, **kwargs)

        # Don't allow dates older than now.
        if self.parameter_approval_end_date <= self.parameter_approval_start_date:
            raise ValidationError('Start time for parameter approval must be before end time.')
        if self.appraisal_start_date <= self.parameter_approval_end_date:
            raise ValidationError('Start time for appraisal must be after end time of parameter approval.')
        if self.appraisal_end_date <= self.appraisal_start_date:
            raise ValidationError('End time for appraisal must be after start time.')
        if self.appraisal_end_date >= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be after end time of appraisal.')
        if self.r1_approval_end_date <= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be before end time.')
        if self.r1_approval_end_date >= self.r2_approval_start_date:
            raise ValidationError('Start time for R2 approval must be after end time of R1 approval.')
        if self.r2_approval_end_date <= self.r2_approval_start_date:
            raise ValidationError("End time for R2 approval must be after start time.")

    class Meta:
        verbose_name = 'Staff Appraisal Cycle Configuration'
        verbose_name_plural = 'Staff Appraisal Cycle Configuration'

    def __str__(self):
        st = 'Staff Cycle Configuration for year ' + str(self.year)
        if self.is_active:
            st += ' (Active)'
        return st


class FOETFacultyAppraisalCycleConfiguration(models.Model):
    year = models.IntegerField(default=datetime.datetime.now().year)
    data_year = models.IntegerField(default=datetime.datetime.now().year - 1)
    is_active = models.BooleanField(default=True)
    verification_start_date = models.DateField()
    verification_end_date = models.DateField()
    appraisal_start_date = models.DateField()
    appraisal_end_date = models.DateField()
    r1_approval_start_date = models.DateField()
    r1_approval_end_date = models.DateField()
    r2_approval_start_date = models.DateField()
    r2_approval_end_date = models.DateField()

    def clean(self):
        # run the base validation
        super(FOETFacultyAppraisalCycleConfiguration, self).clean()

        # Don't allow dates older than now.
        if self.verification_end_date <= self.verification_start_date:
            raise ValidationError('Start time for verification must be before end time.')
        if self.appraisal_start_date <= self.verification_end_date:
            raise ValidationError('Start time for appraisal must be after end time of verification.')
        if self.appraisal_end_date <= self.appraisal_start_date:
            raise ValidationError('End time for appraisal must be after start time.')
        if self.appraisal_end_date >= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be after end time of appraisal.')
        if self.r1_approval_end_date <= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be before end time.')
        if self.r1_approval_end_date >= self.r2_approval_start_date:
            raise ValidationError('Start time for R2 approval must be after end time of R1 approval.')
        if self.r2_approval_end_date <= self.r2_approval_start_date:
            raise ValidationError("End time for R2 approval must be after start time.")

    def get_cycle(self):
        date = CurrentDate.objects.all().first()
        if date.use_system:
            date = datetime.date.today()
        else:
            date = date.date

        if date < self.verification_start_date:
            return 'not_started'
        elif self.verification_start_date <= date <= self.verification_end_date:
            return 'verification'
        elif self.appraisal_start_date <= date <= self.appraisal_end_date:
            return 'appraisal'
        elif self.r1_approval_start_date <= date <= self.r1_approval_end_date:
            return 'r1_approval'
        elif self.r2_approval_start_date <= date <= self.r2_approval_end_date:
            return 'r2_approval'
        elif date > self.r2_approval_end_date:
            return 'completed'
        else:
            return 'unknown'

    class Meta:
        verbose_name = 'SOT Appraisal Cycle Configuration'
        verbose_name_plural = 'SOT Appraisal Cycle Configuration'

    def __str__(self):
        st = 'SOT Cycle Configuration for year ' + str(self.year)
        if self.is_active:
            st += ' (Active)'
        return st


class SLSFacultyAppraisalCycleConfiguration(models.Model):
    year = models.IntegerField(default=datetime.datetime.now().year)
    data_year = models.IntegerField(default=datetime.datetime.now().year - 1)
    is_active = models.BooleanField(default=True)
    verification_start_date = models.DateField()
    verification_end_date = models.DateField()
    appraisal_start_date = models.DateField()
    appraisal_end_date = models.DateField()
    r1_approval_start_date = models.DateField()
    r1_approval_end_date = models.DateField()
    r2_approval_start_date = models.DateField()
    r2_approval_end_date = models.DateField()

    def clean(self):
        # run the base validation
        super(SLSFacultyAppraisalCycleConfiguration, self).clean()

        # Don't allow dates older than now.
        if self.verification_end_date <= self.verification_start_date:
            raise ValidationError('Start time for verification must be before end time.')
        if self.appraisal_start_date <= self.verification_end_date:
            raise ValidationError('Start time for appraisal must be after end time of verification.')
        if self.appraisal_end_date <= self.appraisal_start_date:
            raise ValidationError('End time for appraisal must be after start time.')
        if self.appraisal_end_date >= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be after end time of appraisal.')
        if self.r1_approval_end_date <= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be before end time.')
        if self.r1_approval_end_date >= self.r2_approval_start_date:
            raise ValidationError('Start time for R2 approval must be after end time of R1 approval.')
        if self.r2_approval_end_date <= self.r2_approval_start_date:
            raise ValidationError("End time for R2 approval must be after start time.")

    def get_cycle(self):
        date = CurrentDate.objects.all().first()
        if date.use_system:
            date = datetime.date.today()
        else:
            date = date.date

        if date < self.verification_start_date:
            return 'not_started'
        elif self.verification_start_date <= date <= self.verification_end_date:
            return 'verification'
        elif self.appraisal_start_date <= date <= self.appraisal_end_date:
            return 'appraisal'
        elif self.r1_approval_start_date <= date <= self.r1_approval_end_date:
            return 'r1_approval'
        elif self.r2_approval_start_date <= date <= self.r2_approval_end_date:
            return 'r2_approval'
        elif date > self.r2_approval_end_date:
            return 'completed'
        else:
            return 'unknown'

    class Meta:
        verbose_name = 'SLS Appraisal Cycle Configuration'
        verbose_name_plural = 'SLS Appraisal Cycle Configuration'

    def __str__(self):
        st = 'SLS Cycle Configuration for year ' + str(self.year)
        if self.is_active:
            st += ' (Active)'
        return st


class SOEMFacultyAppraisalCycleConfiguration(models.Model):
    year = models.IntegerField(default=datetime.datetime.now().year)
    data_year = models.IntegerField(default=datetime.datetime.now().year - 1)
    is_active = models.BooleanField(default=True)
    verification_start_date = models.DateField()
    verification_end_date = models.DateField()
    appraisal_start_date = models.DateField()
    appraisal_end_date = models.DateField()
    r1_approval_start_date = models.DateField()
    r1_approval_end_date = models.DateField()
    r2_approval_start_date = models.DateField()
    r2_approval_end_date = models.DateField()

    def clean(self):
        # run the base validation
        super(SOEMFacultyAppraisalCycleConfiguration, self).clean()

        # Don't allow dates older than now.
        if self.verification_end_date <= self.verification_start_date:
            raise ValidationError('Start time for verification must be before end time.')
        if self.appraisal_start_date <= self.verification_end_date:
            raise ValidationError('Start time for appraisal must be after end time of verification.')
        if self.appraisal_end_date <= self.appraisal_start_date:
            raise ValidationError('End time for appraisal must be after start time.')
        if self.appraisal_end_date >= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be after end time of appraisal.')
        if self.r1_approval_end_date <= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be before end time.')
        if self.r1_approval_end_date >= self.r2_approval_start_date:
            raise ValidationError('Start time for R2 approval must be after end time of R1 approval.')
        if self.r2_approval_end_date <= self.r2_approval_start_date:
            raise ValidationError("End time for R2 approval must be after start time.")

    def get_cycle(self):
        date = CurrentDate.objects.all().first()
        if date.use_system:
            date = datetime.date.today()
        else:
            date = date.date

        if date < self.verification_start_date:
            return 'not_started'
        elif self.verification_start_date <= date <= self.verification_end_date:
            return 'verification'
        elif self.appraisal_start_date <= date <= self.appraisal_end_date:
            return 'appraisal'
        elif self.r1_approval_start_date <= date <= self.r1_approval_end_date:
            return 'r1_approval'
        elif self.r2_approval_start_date <= date <= self.r2_approval_end_date:
            return 'r2_approval'
        elif date > self.r2_approval_end_date:
            return 'completed'
        else:
            return 'unknown'

    class Meta:
        verbose_name = 'SOEM Appraisal Cycle Configuration'
        verbose_name_plural = 'SOEM Appraisal Cycle Configuration'

    def __str__(self):
        st = 'SOEM Cycle Configuration for year ' + str(self.year)
        if self.is_active:
            st += ' (Active)'
        return st


class MathFacultyAppraisalCycleConfiguration(models.Model):
    year = models.IntegerField(default=datetime.datetime.now().year)
    data_year = models.IntegerField(default=datetime.datetime.now().year - 1)
    is_active = models.BooleanField(default=True)
    verification_start_date = models.DateField()
    verification_end_date = models.DateField()
    appraisal_start_date = models.DateField()
    appraisal_end_date = models.DateField()
    r1_approval_start_date = models.DateField()
    r1_approval_end_date = models.DateField()
    r2_approval_start_date = models.DateField()
    r2_approval_end_date = models.DateField()

    def clean(self):
        # run the base validation
        super(MathFacultyAppraisalCycleConfiguration, self).clean()

        # Don't allow dates older than now.
        if self.verification_end_date <= self.verification_start_date:
            raise ValidationError('Start time for verification must be before end time.')
        if self.appraisal_start_date <= self.verification_end_date:
            raise ValidationError('Start time for appraisal must be after end time of verification.')
        if self.appraisal_end_date <= self.appraisal_start_date:
            raise ValidationError('End time for appraisal must be after start time.')
        if self.appraisal_end_date >= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be after end time of appraisal.')
        if self.r1_approval_end_date <= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be before end time.')
        if self.r1_approval_end_date >= self.r2_approval_start_date:
            raise ValidationError('Start time for R2 approval must be after end time of R1 approval.')
        if self.r2_approval_end_date <= self.r2_approval_start_date:
            raise ValidationError("End time for R2 approval must be after start time.")

    def get_cycle(self):
        date = CurrentDate.objects.all().first()
        if date.use_system:
            date = datetime.date.today()
        else:
            date = date.date

        if date < self.verification_start_date:
            return 'not_started'
        elif self.verification_start_date <= date <= self.verification_end_date:
            return 'verification'
        elif self.appraisal_start_date <= date <= self.appraisal_end_date:
            return 'appraisal'
        elif self.r1_approval_start_date <= date <= self.r1_approval_end_date:
            return 'r1_approval'
        elif self.r2_approval_start_date <= date <= self.r2_approval_end_date:
            return 'r2_approval'
        elif date > self.r2_approval_end_date:
            return 'completed'
        else:
            return 'unknown'

    class Meta:
        verbose_name = 'Maths Appraisal Cycle Configuration'
        verbose_name_plural = 'Maths Appraisal Cycle Configuration'

    def __str__(self):
        st = 'Maths Cycle Configuration for year ' + str(self.year)
        if self.is_active:
            st += ' (Active)'
        return st


class ScienceFacultyAppraisalCycleConfiguration(models.Model):
    year = models.IntegerField(default=datetime.datetime.now().year)
    data_year = models.IntegerField(default=datetime.datetime.now().year - 1)
    is_active = models.BooleanField(default=True)
    verification_start_date = models.DateField()
    verification_end_date = models.DateField()
    appraisal_start_date = models.DateField()
    appraisal_end_date = models.DateField()
    r1_approval_start_date = models.DateField()
    r1_approval_end_date = models.DateField()
    r2_approval_start_date = models.DateField()
    r2_approval_end_date = models.DateField()

    def clean(self):
        # run the base validation
        super(ScienceFacultyAppraisalCycleConfiguration, self).clean()

        # Don't allow dates older than now.
        if self.verification_end_date <= self.verification_start_date:
            raise ValidationError('Start time for verification must be before end time.')
        if self.appraisal_start_date <= self.verification_end_date:
            raise ValidationError('Start time for appraisal must be after end time of verification.')
        if self.appraisal_end_date <= self.appraisal_start_date:
            raise ValidationError('End time for appraisal must be after start time.')
        if self.appraisal_end_date >= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be after end time of appraisal.')
        if self.r1_approval_end_date <= self.r1_approval_start_date:
            raise ValidationError('Start time for R1 approval must be before end time.')
        if self.r1_approval_end_date >= self.r2_approval_start_date:
            raise ValidationError('Start time for R2 approval must be after end time of R1 approval.')
        if self.r2_approval_end_date <= self.r2_approval_start_date:
            raise ValidationError("End time for R2 approval must be after start time.")

    def get_cycle(self):
        date = CurrentDate.objects.all().first()
        if date.use_system:
            date = datetime.date.today()
        else:
            date = date.date

        if date < self.verification_start_date:
            return 'not_started'
        elif self.verification_start_date <= date <= self.verification_end_date:
            return 'verification'
        elif self.appraisal_start_date <= date <= self.appraisal_end_date:
            return 'appraisal'
        elif self.r1_approval_start_date <= date <= self.r1_approval_end_date:
            return 'r1_approval'
        elif self.r2_approval_start_date <= date <= self.r2_approval_end_date:
            return 'r2_approval'
        elif date > self.r2_approval_end_date:
            return 'completed'
        else:
            return 'unknown'

    class Meta:
        verbose_name = 'Science Appraisal Cycle Configuration'
        verbose_name_plural = 'Science Appraisal Cycle Configuration'

    def __str__(self):
        st = 'Science Cycle Configuration for year ' + str(self.year)
        if self.is_active:
            st += ' (Active)'
        return st


class CurrentDate(models.Model):
    date = models.DateField()
    use_system = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Current Date'
        verbose_name_plural = 'Current Date'

    def __str__(self):
        return 'Current Date'

    def get_date(self):
        if self.use_system:
            return datetime.date.today()
        else:
            return self.date


class ShowResult(models.Model):
    show_result = models.BooleanField(default=False, verbose_name='Show Result ?')
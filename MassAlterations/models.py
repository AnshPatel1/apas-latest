import csv
import os

from django.db import models, transaction

import Account
from Account.models import User, designations, schools
from BulkUpload.BulkUploadFoET.models import UploadError
from MasterConfiguration.models import *


# Create your models here.

class ChangeR1R2(models.Model):
    """Model for storing the file uploaded by the user"""
    file = models.FileField(upload_to='alterations_csv_uploads')

    def clean(self):
        if not str(self.file.name).endswith('.csv'):
            raise UploadError(
                "Not correct file format. Please make sure the file is a csv file with extension .csv",
                self.file.url, 'Change R1 R2')
        self.save()

        with open(self.file.path, 'r') as f:
            csvreader = list(csv.reader(f))
            if len(csvreader[0]) != 3:
                raise UploadError("Not a valid csv file. Make sure the file has 2 columns", self.file.url,
                                  'Change R1 R2')
            objects = []
            for row in csvreader[1:]:
                try:
                    faculty = User.objects.get(username=row[0])
                    r1 = User.objects.get(username=row[1])
                    r2 = User.objects.get(username=row[2])
                    faculty.ro1_id = r1
                    faculty.ro2_id = r2
                    faculty.save()
                except User.DoesNotExist:
                    raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url,
                                      'Change R1 R2')
                except User.MultipleObjectsReturned:
                    raise UploadError(
                        f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue",
                        self.file.url, 'Change R1 R2')

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Change R1 R2'
        verbose_name_plural = 'Change R1 R2'
        ordering = ['id']


class ChangeDesignation(models.Model):
    """Model for storing the file uploaded by the user"""
    file = models.FileField(upload_to='alterations_csv_uploads')

    def clean(self):
        if not str(self.file.name).endswith('.csv'):
            raise UploadError(
                "Not correct file format. Please make sure the file is a csv file with extension .csv",
                self.file.url, 'Change Designation')
        self.save()

        with open(self.file.path, 'r') as f:
            csvreader = list(csv.reader(f))
            if len(csvreader[0]) != 2:
                raise UploadError("Not a valid csv file. Make sure the file has 2 columns", self.file.url,
                                  'Change Designation')
            objects = []
            for row in csvreader[1:]:
                try:
                    faculty = User.objects.get(username=row[0])
                    if row[1] in ['assistant_prof_on_contract', 'prof', 'associate_prof', 'assistant_prof']:
                        faculty.designation = designations[row[1]]
                        faculty.designation_abbreviation = row[1]
                        faculty.save()
                    else:
                        raise UploadError(
                            f"Invalid designation {row[1]}. Please enter one of prof, assoc_prof, asst_prof, lecturer",
                            self.file.url, 'Change Designation')

                except User.DoesNotExist:
                    raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url,
                                      'Change Designation')
                except User.MultipleObjectsReturned:
                    raise UploadError(
                        f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue",
                        self.file.url, 'Change Designation')

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Change Designation'
        verbose_name_plural = 'Change Designation'
        ordering = ['id']


class SetAppraise(models.Model):
    """Model for storing the file uploaded by the user"""
    target = models.CharField(max_length=100, choices=(
        ('STAFF', 'Staff'),
        ("FOET", "FOET"),
        ("FOLS", "FOLS"),
        ("FOM", "FOM"),
        ("MATHS", "MATHS"),
        ("SCIENCE", "SCIENCE")
    ))
    file = models.FileField(upload_to='alterations_csv_uploads')

    def clean(self):
        if not str(self.file.name).endswith('.csv'):
            raise UploadError(
                "Not correct file format. Please make sure the file is a csv file with extension .csv",
                self.file.url, 'Change Designation')
        self.save()

        with open(self.file.path, 'r') as f:
            csvreader = list(csv.reader(f))
            if len(csvreader[0]) != 1:
                raise UploadError("Not a valid csv file. Make sure the file has 2 columns", self.file.url,
                                  'Change Designation')
            objects = []
            for row in csvreader[1:]:
                try:
                    objects.append(User.objects.get(username=row[0]))
                except User.DoesNotExist:
                    raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url,
                                      'Change Designation')
                except User.MultipleObjectsReturned:
                    raise UploadError(
                        f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue",
                        self.file.url, 'Change Designation')
            if self.target == 'STAFF':
                inc = StaffAppraisalCycleInclusion.objects.get(is_active=True)
                inc.appraisee.clear()
                inc.appraisee.add(*objects)
                inc.save()
            elif self.target == 'FOET':
                inc = SOTFacultyAppraisalCycleInclusion.objects.get(is_active=True)
                inc.appraisee.clear()
                inc.appraisee.add(*objects)
                inc.save()
            elif self.target == 'FOLS':
                inc = SLSFacultyAppraisalCycleInclusion.objects.get(is_active=True)
                inc.appraisee.clear()
                inc.appraisee.add(*objects)
                inc.save()
            elif self.target == 'FOM':
                inc = SPMFacultyAppraisalCycleInclusion.objects.get(is_active=True)
                inc.appraisee.clear()
                inc.appraisee.add(*objects)
                inc.save()
            elif self.target == 'MATHS':
                inc = MathFacultyAppraisalCycleInclusion.objects.get(is_active=True)
                inc.appraisee.clear()
                inc.appraisee.add(*objects)
                inc.save()
            elif self.target == 'SCIENCE':
                inc = ScienceFacultyAppraisalCycleInclusion.objects.get(is_active=True)
                inc.appraisee.clear()
                inc.appraisee.add(*objects)
                inc.save()

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Set Appraise'
        verbose_name_plural = 'Set Appraise'
        ordering = ['id']


class SetHOD(models.Model):
    """Model for storing the file uploaded by the user"""
    file = models.FileField(upload_to='alterations_csv_uploads')

    def clean(self):
        if not str(self.file.name).endswith('.csv'):
            raise UploadError(
                "Not correct file format. Please make sure the file is a csv file with extension .csv",
                self.file.url, 'Change Designation')
        self.save()

        with open(self.file.path, 'r') as f:
            csvreader = list(csv.reader(f))
            if len(csvreader[0]) != 1:
                raise UploadError("Not a valid csv file. Make sure the file has 2 columns", self.file.url,
                                  'Change Designation')
            faculties = []
            for row in csvreader[1:]:
                try:
                    faculties.append(User.objects.get(username__iexact=row[0]).username)
                except User.DoesNotExist:
                    raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url,
                                      'Change Designation')
                except User.MultipleObjectsReturned:
                    raise UploadError(
                        f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue",
                        self.file.url, 'Change Designation')
            User.objects.update(is_hod=False)
            User.objects.filter(username__in=[faculty.id for faculty in faculties]).update(is_hod=True)


    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Set HOD'
        verbose_name_plural = 'Set HODs'
        ordering = ['id']


class BulkUserUpload(models.Model):
    """Model for storing the file uploaded by the user"""
    # full_name,username,email,designation,department,school
    file = models.FileField(upload_to='alterations_csv_uploads')

    def clean(self):
        if not str(self.file.name).endswith('.csv'):
            raise UploadError(
                "Not correct file format. Please make sure the file is a csv file with extension .csv",
                self.file.url, 'Bulk Upload User')
        self.save()

        with open(self.file.path, 'r') as f:
            csvreader = list(csv.reader(f))
            if len(csvreader[0]) != 8:
                raise UploadError("Not a valid csv file. Make sure the file has 8 columns", self.file.url,
                                  'Bulk Upload User')
            objects = []
            for row in csvreader[1:]:
                try:
                    user = User()
                    user.username = row[1]
                    user.full_name = row[0]
                    user.email = row[2]
                    if row[3] in ['assistant_prof_on_contract', 'prof', 'associate_prof', 'assistant_prof', 'stf']:
                        user.designation = designations[row[3]]
                        user.designation_abbreviation = row[3]
                    if row[3] == 'stf':
                        user.roles = 'stf'
                        user.type = "Staff"
                    else:
                        user.roles = 'fac'
                        user.type = "Faculty"
                    user.department = row[4]
                    if row[5] not in schools:
                        raise UploadError(f"Invalid school {row[5]}. Please enter one of {', '.join(schools.keys())}",
                                          self.file.url, 'Bulk Upload User')
                    user.school = schools[row[5]]
                    user.school_abbreviation = row[5]
                    user.ro1_id = User.objects.get(username=row[6])
                    user.ro2_id = User.objects.get(username=row[7])
                    objects.append(user)
                except User.DoesNotExist:
                    raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url,
                                      'Change R1 R2')
                except User.MultipleObjectsReturned:
                    raise UploadError(
                        f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue",
                        self.file.url, 'Change R1 R2')
            try:
                with transaction.atomic():
                    User.objects.bulk_create(objects)
            except Exception as e:
                raise UploadError(f"Error while saving the data. {e}", self.file.url, 'Bulk Upload User')

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'New User'
        verbose_name_plural = 'New Users'
        ordering = ['id']

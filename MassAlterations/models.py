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
                    faculty = User.objects.get(username__iexact=row[0])
                    r1 = User.objects.get(username__iexact=row[1])
                    r2 = User.objects.get(username__iexact=row[2])
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
                    faculty = User.objects.get(username__iexact=row[0])
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
                    objects.append(User.objects.get(username__iexact=row[0]))
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
            User.objects.filter(username__in=faculties).update(is_hod=True)

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
        with transaction.atomic():
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
                        user.ro1_id = User.objects.get(username__iexact=row[6])
                        user.ro2_id = User.objects.get(username__iexact=row[7])
                        objects.append(user)
                        user.save()
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url,
                                          'Change R1 R2')
                    except User.MultipleObjectsReturned:
                        raise UploadError(
                            f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue",
                            self.file.url, 'Change R1 R2')
                try:
                    pass
                    # with transaction.atomic():
                    #     User.objects.bulk_create(objects)
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


class SetNewCycle(models.Model):
    """Model for storing the file uploaded by the user"""
    clean_sot = models.BooleanField(default=False)
    clean_sls = models.BooleanField(default=False)
    clean_spm = models.BooleanField(default=False)
    clean_math = models.BooleanField(default=False)
    clean_science = models.BooleanField(default=False)
    goalsheet_year = models.IntegerField(default=2025)

    def clean(self):
        from BulkUpload.BulkUploadFoET import models as bulk_upload_foet
        from BulkUpload.BulkUploadFoLS import models as bulk_upload_fols
        from BulkUpload.BulkUploadFoEM import models as bulk_upload_foem
        from BulkUpload.BulkUploadMaths import models as bulk_upload_maths
        from BulkUpload.BulkUploadScience import models as bulk_upload_science
        from Faculty.FacultyFOET.models import FOETGoalSheetAssistantProf, FOETGoalSheetAssistantProfOnContract, FOETGoalSheetAssociateProf, FOETGoalSheetProf
        from Faculty.FacultySLS.models import FOLSGoalSheetAssistantProf, FOLSGoalSheetAssistantProfOnContract, FOLSGoalSheetAssociateProf, FOLSGoalSheetProf
        from Faculty.FacultySoEM.models import FOEMGoalSheetAssistantProf, FOEMGoalSheetAssistantProfOnContract, FOEMGoalSheetAssociateProf, FOEMGoalSheetProf
        from Faculty.FacultyMaths.models import MathGoalSheetAssistantProf, MathGoalSheetAssistantProfOnContract, MathGoalSheetAssociateProf, MathGoalSheetProf
        from Faculty.FacultyScience.models import ScienceGoalSheetAssistantProf, ScienceGoalSheetAssistantProfOnContract, ScienceGoalSheetAssociateProf, ScienceGoalSheetProf
        from django.apps import apps
        cleanable_models = {
            'FacultyFOET': {
                "enabled": self.clean_sot,
                "delete": [bulk_upload_foet.UploadCSV],
                "goalsheets": [FOETGoalSheetAssistantProf, FOETGoalSheetAssistantProfOnContract, FOETGoalSheetAssociateProf, FOETGoalSheetProf]
            },
            'FacultySLS': {
                "enabled": self.clean_sls,
                "delete": [bulk_upload_fols.UploadCSV],
                "goalsheets": [FOLSGoalSheetAssistantProf, FOLSGoalSheetAssistantProfOnContract, FOLSGoalSheetAssociateProf, FOLSGoalSheetProf]
            },
            'FacultySoEM': {
                "enabled": self.clean_spm,
                "delete": [bulk_upload_foem.UploadCSV],
                "goalsheets": [FOEMGoalSheetAssistantProf, FOEMGoalSheetAssistantProfOnContract, FOEMGoalSheetAssociateProf, FOEMGoalSheetProf]
            },
            'FacultyMaths': {
                "enabled": self.clean_math,
                "delete": [bulk_upload_maths.UploadCSV],
                "goalsheets": [MathGoalSheetAssistantProf, MathGoalSheetAssistantProfOnContract, MathGoalSheetAssociateProf, MathGoalSheetProf]
            },
            'FacultyScience': {
                "enabled": self.clean_science,
                "delete": [bulk_upload_science.UploadCSV],
                "goalsheets": [ScienceGoalSheetAssistantProf, ScienceGoalSheetAssistantProfOnContract, ScienceGoalSheetAssociateProf, ScienceGoalSheetProf]
            }
        }
        for app_label, models in cleanable_models.items():
            if models["enabled"]:
                # Get the models from the app
                app_config = apps.get_app_config(app_label)
                models["delete"] += [app_config.get_model(model.__name__) for model in app_config.get_models()]
                # Delete all the data from the models
                for i in range(2):
                    for model in models["delete"]:
                        try:
                            model.objects.all().delete()
                        except Exception as e:
                            print(f"Error deleting data from {model.__name__}: {e}")
                # Delete all the data from the goalsheets
                for goal_sheet in models["goalsheets"]:
                    gs = goal_sheet(year=self.goalsheet_year, is_active=True)
                    gs.save()
        self.save()


class ValidateUID(models.Model):
    """Model for storing the file uploaded by the user"""
    file = models.FileField(upload_to='validate_uids')

    def clean(self):
        if not str(self.file.name).endswith('.csv'):
            raise UploadError(
                "Not correct file format. Please make sure the file is a csv file with extension .csv",
                self.file.url, 'Change Designation')
        self.save()

        with open(self.file.path, 'r') as f:
            csvreader = list(csv.reader(f))
            system_users = set([u.username.lower() for u in User.objects.all()])
            file_users = set()
            for row in csvreader[1:]:
                file_users.add(row[0].lower())
            difference_users = file_users - system_users
            print(difference_users)
            if [i for i in difference_users if i]:
                raise UploadError(f"Users {', '.join(list(difference_users))} are not present in the system",
                                  self.file.url, 'Validate UID')

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Validate UID'
        verbose_name_plural = 'Validate UIDs'
        ordering = ['id']
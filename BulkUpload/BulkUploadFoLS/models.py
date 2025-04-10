import csv
import os
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ProtectedError
from Account.models import User
from APAS.middleware.ModelInstance import local


# Create your models here.


class UploadCSV(models.Model):
    """Model for storing the file uploaded by the user"""
    upload_choices = (
        ('additional', 'Additional Marks (Placement & Admission'),
        ('co_curricular', 'Co-Curricular Activities'),
        ('international_admission', 'Successful conversion of International Admission (SLS)/ Local Placements'),
        ('academia_collab', 'Academia Collaboration'),
        ('consultancy', 'Providing Consultancy'),
        ('award', 'Awards'),
        # ('patent', 'Patent'),
        ('phd_guidance', "PhD Guidance"),
        ('project', 'Project'),
        ('scopus_wos_ugc', 'Paper Publications in Scopus, Web of Science & UGC Care'),
        ('books', 'Books and Publications'),
        ('exam_duty', 'Exam Duty'),
        ('student_feedback', 'Student Feedback'),
        ('teaching_load', 'Teaching Load'),
    )
    upload_type = models.CharField(max_length=100, choices=upload_choices)
    file = models.FileField(upload_to='csv_files')

    def clean(self):
        if not str(self.file.name).endswith('.csv'):
            raise UploadError("Not correct file format. Please make sure the file is a csv file with extension .csv", self.file.url, self.upload_type)
        vf = VerifyUploaded()
        self.save()
        vf.csv_origin = self
        vf.save()

        if self.upload_type == 'academia_collab':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 3:
                    raise UploadError("Not a valid csv file. Make sure the file has 2 columns", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    aca = ViewAcademiaCollaboration()
                    aca.faculty = faculty
                    aca.csv_origin = self
                    aca.designation = faculty.designation
                    aca.department = faculty.department
                    try:
                        mou = float(row[1])
                        if mou > 0:
                            aca.mou_available = True
                            aca.mou_marks = mou
                        else:
                            aca.mou_available = False
                        aca.marks = float(row[2])
                    except ValueError:
                        raise UploadError("Marks should be a number at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(aca)
                ViewAcademiaCollaboration.objects.bulk_create(objects)
        elif self.upload_type == 'co_curricular':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 2:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    aw = ViewCoCurricular()
                    aw.faculty = faculty
                    aw.csv_origin = self
                    aw.designation = faculty.designation
                    aw.department = faculty.department
                    try:
                        aw.marks = float(row[1])
                    except ValueError:
                        raise UploadError("Marks should be a number at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(aw)
                ViewCoCurricular.objects.bulk_create(objects)
        elif self.upload_type == 'international_admission':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 2:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    aw = ViewInternationalAdmission()
                    aw.faculty = faculty
                    aw.csv_origin = self
                    aw.designation = faculty.designation
                    aw.department = faculty.department
                    try:
                        aw.marks = float(row[1])
                    except ValueError:
                        raise UploadError("Marks should be a number at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(aw)
                ViewInternationalAdmission.objects.bulk_create(objects)
        elif self.upload_type == 'award':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 6:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    aw = ViewAward()
                    aw.faculty = faculty
                    aw.csv_origin = self
                    aw.designation = faculty.designation
                    aw.department = faculty.department
                    try:
                        aw.title = row[1]
                        aw.description = row[2]
                        aw.level = row[3]
                        aw.month = int(row[4])
                        aw.year = int(row[5])
                    except ValueError:
                        raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(aw)
                ViewAward.objects.bulk_create(objects)
        elif self.upload_type == 'consultancy':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 6:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    aw = ViewConsultancy()
                    aw.faculty = faculty
                    aw.csv_origin = self
                    aw.designation = faculty.designation
                    aw.department = faculty.department
                    try:
                        aw.type = row[1]
                        aw.description = row[2]
                        aw.amount = int(row[3])
                        aw.month = int(row[4])
                        aw.year = int(row[5])
                    except ValueError:
                        raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(aw)
                ViewConsultancy.objects.bulk_create(objects)
        # elif self.upload_type == 'patent':
        #     with open(self.file.path, 'r') as f:
        #         csvreader = list(csv.reader(f))
        #         if len(csvreader[0]) != 6:
        #             raise UploadError("Not correct file format", self.file.url, self.upload_type)
        #         objects = []
        #         for row in csvreader[1:]:
        #             try:
        #                 faculty = User.objects.get(username__iexact=row[0])
        #             except User.DoesNotExist:
        #                 raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
        #             except User.MultipleObjectsReturned:
        #                 raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
        #             pa = ViewPatent()
        #             pa.faculty = faculty
        #             pa.csv_origin = self
        #             pa.designation = faculty.designation
        #             pa.department = faculty.department
        #             try:
        #                 pa.status = row[1]
        #                 pa.description = row[2]
        #                 pa.month = int(row[3])
        #                 pa.year = int(row[4])
        #                 pa.application_no = row[5]
        #             except ValueError:
        #                 raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
        #             objects.append(pa)
        #         ViewPatent.objects.bulk_create(objects)
        elif self.upload_type == 'phd_guidance':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 4:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    ad = ViewPhDGuidance()
                    ad.faculty = faculty
                    ad.csv_origin = self
                    ad.designation = faculty.designation
                    ad.department = faculty.department
                    try:
                        ad.status = row[1]
                        ad.student_name = row[2]
                        ad.year = int(row[3])
                    except ValueError:
                        raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(ad)
                ViewPhDGuidance.objects.bulk_create(objects)
        elif self.upload_type == 'project':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 10:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    pr = ViewProject()
                    pr.faculty = faculty
                    pr.csv_origin = self
                    pr.designation = faculty.designation
                    pr.department = faculty.department
                    try:
                        pr.title = row[1]
                        pr.status = row[2]
                        pr.funding_agency = row[2]
                        pr.amount = int(row[3])
                        role = row[4]
                        if role == 'pi':
                            pr.role = 'pi'
                        elif role == 'copi':
                            pr.role = 'copi'
                        else:
                            raise UploadError("Role should be either pi or co_pi at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        pr.year = int(row[5])
                        pr.month = int(row[6])
                        if row[7] == '1':
                            pr.is_institutional = True
                            pr.institutional_marks = float(row[9])
                        elif row[7] == '0':
                            pr.is_institutional = False
                        else:
                            raise UploadError("institutional field must br 0 or 1 at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        if row[8] == '1':
                            pr.is_osrp = True
                        elif row[8] == '0':
                            pr.is_osrp = False
                        else:
                            raise UploadError("OSRP field must br 0 or 1 at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)

                    except ValueError:
                        raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(pr)
                ViewProject.objects.bulk_create(objects)
        elif self.upload_type == 'scopus_wos_ugc':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 16:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    sw = ViewScopusWos()
                    sw.faculty = faculty
                    sw.csv_origin = self
                    sw.designation = faculty.designation
                    sw.department = faculty.department
                    try:
                        sw.month = int(row[1])
                        sw.year = int(row[2])
                        sw.type = row[3]
                        sw.title = row[4]
                        sw.entity_name = row[5]
                        sw.isbn = row[7]
                        if sw.type == 'journal':
                            sw.paper_quality = row[6]
                        elif sw.type == 'conf':
                            sw.paper_quality = row[6]
                            sw.conference_organization = row[8]
                            sw.conference_level = row[9]
                        elif sw.type == 'epub' or sw.type == 'article':
                            pass
                        else:
                            raise UploadError("Type should be either journal or conf at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        if row[10] == '1':
                            sw.is_main_author = True
                        elif row[10] == '0':
                            sw.is_main_author = False
                        else:
                            raise UploadError("main author field must br 0 or 1 at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        sw.co_author_count = int(row[11])
                        if row[12] == '1':
                            sw.is_scopus = True
                        elif row[12] == '0':
                            sw.is_scopus = False
                        else:
                            raise UploadError("Scopus field must br 0 or 1 at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        if row[13] == '1':
                            sw.is_wos = True
                        elif row[13] == '0':
                            sw.is_wos = False
                        else:
                            raise UploadError("Scopus field must br 0 or 1 at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        if row[14] == '1':
                            sw.is_ugc = True
                        elif row[14] == '0':
                            sw.is_ugc = False
                        else:
                            raise UploadError("WOS field must br 0 or 1 at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)

                    except ValueError:
                        raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(sw)
                ViewScopusWos.objects.bulk_create(objects)
        elif self.upload_type == 'books':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 11:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    bk = ViewBook()
                    bk.faculty = faculty
                    bk.csv_origin = self
                    bk.designation = faculty.designation
                    bk.department = faculty.department
                    try:
                        bk.month = int(row[1])
                        bk.year = int(row[2])
                        if row[3] == 'INTERNATIONAL' or row[3] == 'NATIONAL':
                            bk.level = row[3]
                        else:
                            raise UploadError("Type should be either 'INTERNATIONAL' or 'NATIONAL' at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        bk.title = row[4]
                        if row[5] == 'research' or row[5] == 'text' or row[5] == 'literary':
                            bk.category = row[5]
                        else:
                            raise UploadError("Category should be either 'research' or 'text' at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        if row[6] == 'chapter' or row[6] == 'book':
                            bk.type = row[6]
                        else:
                            raise UploadError("Book type should be either 'chapter' or 'book' at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        if row[7] == '0':
                            bk.is_main_author = False
                        elif row[7] == '1':
                            bk.is_main_author = True
                        else:
                            raise UploadError("Main author field must br 0 or 1 at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        bk.co_author_count = int(row[8])
                        if row[9] == '1':
                            bk.is_editor = True
                        elif row[9] == '0':
                            bk.is_editor = False
                        else:
                            raise UploadError("Editor field must br 0 or 1 at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                        bk.isbn = row[10]

                    except ValueError:
                        raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(bk)
                ViewBook.objects.bulk_create(objects)
        elif self.upload_type == 'exam_duty':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 5:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    ed = ViewExamDuty()
                    ed.faculty = faculty
                    ed.csv_origin = self
                    ed.designation = faculty.designation
                    ed.department = faculty.department
                    try:
                        ed.timely_invigilation = float(row[1])
                        ed.paper_setting = float(row[2])
                        ed.evaluation = float(row[3])
                        ed.result_submission = float(row[4])
                    except ValueError:
                        raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(ed)
                ViewExamDuty.objects.bulk_create(objects)
        elif self.upload_type == 'student_feedback':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 2:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    sf = ViewStudentFeedback()
                    sf.faculty = faculty
                    sf.csv_origin = self
                    sf.designation = faculty.designation
                    sf.department = faculty.department
                    try:
                        sf.student_feedback = float(row[1])
                    except ValueError:
                        raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(sf)
                ViewStudentFeedback.objects.bulk_create(objects)
        elif self.upload_type == 'teaching_load':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 5:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    tl = ViewTeachingLoad()
                    tl.faculty = faculty
                    tl.csv_origin = self
                    tl.designation = faculty.designation
                    tl.department = faculty.department
                    try:
                        if row[4] == '2':
                            tl.load_odd = float(row[1])
                            tl.load_even = float(row[2])
                        elif row[4] == '3':
                            tl.load_odd = float(row[1])
                            tl.load_even = float(row[2])
                            tl.load_tri = float(row[3])
                        else:
                            raise UploadError("Semester should be either 2 or 3 at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    except ValueError:
                        raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(tl)
                ViewTeachingLoad.objects.bulk_create(objects)
        elif self.upload_type == 'additional':
            with open(self.file.path, 'r') as f:
                csvreader = list(csv.reader(f))
                if len(csvreader[0]) != 3:
                    raise UploadError("Not correct file format", self.file.url, self.upload_type)
                objects = []
                for row in csvreader[1:]:
                    try:
                        faculty = User.objects.get(username__iexact=row[0])
                    except User.DoesNotExist:
                        raise UploadError(f"Faculty with username {row[0]} does not exist", self.file.url, self.upload_type)
                    except User.MultipleObjectsReturned:
                        raise UploadError(f"Multiple faculty with username {row[0]} exist. Please contact admin to resolve this issue", self.file.url, self.upload_type)
                    ad = ViewAdditionalMarks()
                    ad.faculty = faculty
                    ad.csv_origin = self
                    ad.designation = faculty.designation
                    ad.department = faculty.department
                    try:
                        ad.placement_activity = float(row[1])
                        ad.admission_activity = float(row[2])
                    except ValueError:
                        raise UploadError("Make sure the data is correct at row " + str(csvreader.index(row) + 1), self.file.url, self.upload_type)
                    objects.append(ad)
                ViewAdditionalMarks.objects.bulk_create(objects)

    def delete(self, using=None, keep_parents=False):
        Delete.verify_uploaded(Delete(), self)
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete()

    def __str__(self):
        return f'{self.id}.  {self.upload_type}'

    class Meta:
        verbose_name = 'Upload CSV'
        verbose_name_plural = 'Upload CSV'
        ordering = ['id']


class Template(models.Model):
    """Model for storing the template for the uploaded file"""
    name = models.CharField(max_length=100)
    template = models.FileField(upload_to='bulkupload/templates')

    def clean(self):
        Delete.template(Delete())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Download Template'
        verbose_name_plural = 'Download Template'


class VerifyUploaded(models.Model):
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def clean(self):
        pass

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'Verify Uploaded'
        verbose_name_plural = 'Verify Uploaded'


class ViewAcademiaCollaboration(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_academia_collab_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_academia_collab_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    mou_available = models.BooleanField(default=False)
    mou_marks = models.FloatField(default=0)
    marks = models.FloatField()

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    def __str__(self):
        return f'{self.faculty.full_name} - {self.designation} - {self.department} - {self.marks}'

    class Meta:
        verbose_name = 'View Academia Collaboration'
        verbose_name_plural = 'View Academia Collaboration'


class ViewCoCurricular(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_co_curricular_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_co_curricular_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    marks = models.FloatField()

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    def __str__(self):
        return f'{self.faculty.full_name} - {self.designation} - {self.department} - {self.marks}'

    class Meta:
        verbose_name = 'View Co-Curricular & Extra-Curricular Activities'
        verbose_name_plural = 'View Co-Curricular & Extra-Curricular Activities'


class ViewInternationalAdmission(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_int_admissions_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_int_admissions_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    marks = models.FloatField()

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    def __str__(self):
        return f'{self.faculty.full_name} - {self.designation} - {self.department} - {self.marks}'

    class Meta:
        verbose_name = 'View Successful Conversion of International Admission'
        verbose_name_plural = 'View Successful Conversion of International Admissions'


class ViewConsultancy(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_consultancy_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_consultancy_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'View Consultancy Provided'
        verbose_name_plural = 'View Consultancies Provided'


class ViewPatent(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_patent_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_patent_bulk_csv', null=True, blank=True)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    description = models.TextField()
    application_no = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    month = models.IntegerField()
    year = models.IntegerField()

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'View Patent'
        verbose_name_plural = 'View Patents'


class ViewPhDGuidance(models.Model):
    choices_status = (
        ('awarded', 'Awarded'),
        ('synopsis', 'Synopsis Submitted'),
        ('inprogress', 'Under Progress'),
        ('other', 'Other'),
    )
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_phd_guidance_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_phd_guidance_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    student_name = models.CharField(max_length=200)
    year = models.IntegerField()

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    def get_status_name(self):
        return dict(self.choices_status)[self.status]

    class Meta:
        verbose_name = 'View PhD Guidance'
        verbose_name_plural = 'View PhD Guidance'


class ViewProject(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_project_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_project_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    title = models.CharField(max_length=200)
    status = models.CharField(max_length=100)
    funding_agency = models.CharField(max_length=200)
    amount = models.IntegerField()
    role = models.CharField(max_length=4, choices=(('pi', 'PI'), ('copi', 'CO-PI')))
    year = models.IntegerField()
    month = models.IntegerField()
    is_institutional = models.BooleanField(default=False)
    institutional_marks = models.FloatField(default=0)
    is_osrp = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'View Project'
        verbose_name_plural = 'View Projects'

    def get_category(self):
        funds = self.amount
        if not self.is_institutional or not self.is_osrp:
            if funds >= 1000000:
                return 'MAJOR'
            elif funds >= 500000:
                return 'MEDIUM'
            elif funds >= 50000:
                return 'MINOR'
            else:
                raise Exception('Invalid Funds')


class ViewScopusWos(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_scopus_wos_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_scopus_wos_bulk_csv', null=True, blank=True)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    month = models.IntegerField()
    year = models.IntegerField()
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    entity_name = models.TextField()
    paper_quality = models.CharField(max_length=5)
    isbn = models.CharField(max_length=100)
    conference_organization = models.CharField(max_length=100)
    conference_level = models.CharField(max_length=100)
    is_main_author = models.BooleanField(default=False)
    co_author_count = models.IntegerField()
    is_scopus = models.BooleanField(default=False)
    is_wos = models.BooleanField(default=False)
    is_ugc = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'View Publication in Scopus/WOS'
        verbose_name_plural = 'View Publications in Scopus/WOS'


class ViewBook(models.Model):
    category_choices = (
        ('text', 'Textbook'),
        ('research', 'Research Book'),
        ('literary', 'Literary Book'),
    )

    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_book_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_book_bulk_csv', null=True, blank=True)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    month = models.IntegerField()
    year = models.IntegerField()
    level = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=category_choices)
    type = models.CharField(max_length=10)
    is_main_author = models.BooleanField(default=False)
    co_author_count = models.IntegerField()
    is_editor = models.BooleanField(default=False)
    isbn = models.CharField(max_length=100)

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'View Book'
        verbose_name_plural = 'View Books'


class ViewExamDuty(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_exam_duty_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_exam_duty_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    timely_invigilation = models.FloatField()
    paper_setting = models.FloatField()
    evaluation = models.FloatField()
    result_submission = models.FloatField()

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'View Exam Duty'
        verbose_name_plural = 'View Exam Duties'


class ViewStudentFeedback(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_student_feedback_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_student_feedback_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    student_feedback = models.FloatField()

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'View Student Feedback'
        verbose_name_plural = 'View Student Feedbacks'


class ViewTeachingLoad(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_teaching_load_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_teaching_load_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    load_odd = models.FloatField()
    load_even = models.FloatField()
    load_tri = models.FloatField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'View Teaching Load'
        verbose_name_plural = 'View Teaching Loads'


class ViewAward(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_award_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_award_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    month = models.IntegerField(default=0)
    year = models.IntegerField(default=datetime.now().year)
    title = models.CharField(max_length=300)
    description = models.TextField()
    level = models.CharField(max_length=20, null=True)

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'View Award'
        verbose_name_plural = 'View Awards'


class ViewAdditionalMarks(models.Model):
    faculty = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_additional_marks_bulk_faculty')
    csv_origin = models.ForeignKey(UploadCSV, on_delete=models.CASCADE, related_name='fols_additional_marks_bulk_csv')
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    placement_activity = models.FloatField()
    admission_activity = models.FloatField()

    def delete(self, using=None, keep_parents=False, internal=True):
        if not internal:
            raise DeleteError("Cannot delete this object directly. Delete the corresponding UploadCSV object instead", self._meta.verbose_name)
        else:
            super().delete()

    class Meta:
        verbose_name = 'View Additional Marks'
        verbose_name_plural = 'View Additional Marks'


def get_current_user(instance):
    return User.objects.get(id=instance.user.id)


class ErrorLog(models.Model):
    types = (
        ('validation', 'Validation'),
        ('deletion', 'Deletion'),
    )
    VALIDATION_ERROR = 'validation'
    DELETION_ERROR = 'deletion'
    csv_origin = models.FileField(upload_to='error_logs', null=True, blank=True)
    upload_type = models.CharField(max_length=100, null=True, blank=True)
    error = models.TextField()
    type = models.CharField(max_length=20, choices=types)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='fols_error_log_user', editable=False)

    def save(self, *args, **kwargs):
        if self.pk is None and hasattr(local, 'user'):
            self.created_by = local.user
        return super(ErrorLog, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.csv_origin} - {self.error}'

    class Meta:
        verbose_name = 'Error Log'
        verbose_name_plural = 'Error Logs'


class Delete:
    def verify_uploaded(self, csv_origin):
        VerifyUploaded.objects.get(csv_origin=csv_origin).delete(internal=True)

    def template(self):
        """Remove all the templates from the database"""
        templates = Template.objects.all()
        for template in templates:
            if os.path.isfile(template.template.path):
                os.remove(template.template.path)
            template.delete()


class UploadError(ValidationError):
    def __init__(self, msg, csv_path, _type):
        super().__init__(msg)
        errorlog = ErrorLog()
        errorlog.error = msg
        errorlog.csv_origin = csv_path
        errorlog.upload_type = _type
        errorlog.type = ErrorLog.VALIDATION_ERROR
        errorlog.save()


class DeleteError(ValidationError):
    def __init__(self, msg, class_name):
        super().__init__(msg)
        errlog = ErrorLog()
        errlog.error = msg
        errlog.type = ErrorLog.DELETION_ERROR
        errlog.upload_type = class_name
        errlog.save()

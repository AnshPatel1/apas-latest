from django.db import models

from APAS.settings import DEBUG
from Account.models import User


# Create your models here.

class PatentRecords(models.Model):
    internal_id = models.CharField(max_length=16, unique=True)
    faculty = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='patent_faculty')
    uid = models.CharField(max_length=16, default='NA')
    Email = models.CharField(max_length=100)
    department = models.CharField(max_length=500)
    school = models.CharField(max_length=100)
    brief_school = models.CharField(max_length=10)
    ptn_type = models.CharField(max_length=50)
    ptn_desc = models.TextField()
    month = models.CharField(max_length=10)
    yr = models.CharField(max_length=10)
    application_no = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)
    is_rejected = models.BooleanField(null=True)
    is_verified = models.BooleanField(null=True)
    remarks = models.TextField()
    rejected_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='patent_rejected_by', null=True)
    verified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='patent_verified_by', null=True)

    def __str__(self):
        return ' '.join([self.faculty.email, self.brief_school, self.yr, self.month, self.internal_id])

    def to_dict(self):
        return {
            'internal_ID': self.internal_id,
            'uid': self.faculty.username,
            'Email': self.Email,
            'department': self.department,
            'school': self.school,
            'brief_school': self.brief_school,
            'ptn_type': self.ptn_type,
            'ptn_desc': self.ptn_desc,
            'month': self.month,
            'yr': self.yr,
            'application_no': self.application_no,
            'hash': self.hash,
            'is_rejected': self.is_rejected,
            'is_verified': self.is_verified,
            'remarks': self.remarks,
        }

    class Meta:
        ordering = ['-yr', '-month']
        verbose_name = 'Patent Record'
        verbose_name_plural = 'Patents Records'


class PaperRecords(models.Model):
    internal_id = models.CharField(max_length=16, unique=True)
    faculty = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='paper_faculty')
    uid = models.CharField(max_length=16)
    Email = models.CharField(max_length=100)
    department = models.CharField(max_length=500)
    school = models.CharField(max_length=100)
    brief_school = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    yr = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    title = models.TextField()
    entity = models.CharField(max_length=200)
    conference_organization = models.TextField()
    conference_level = models.CharField(max_length=200)
    quality = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    is_main_author = models.BooleanField()
    co_author_count = models.IntegerField()
    is_scopus = models.BooleanField()
    is_wos = models.BooleanField()
    is_ugc = models.BooleanField()
    is_abdc = models.BooleanField()
    hash = models.CharField(max_length=100)
    is_rejected = models.BooleanField(null=True)
    is_verified = models.BooleanField(null=True)
    remarks = models.TextField()
    rejected_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='paper_rejected_by', null=True)
    verified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='paper_verified_by', null=True)

    def __str__(self):
        return ' '.join([self.faculty.email, self.internal_id, self.title])

    def save(self, *args, **kwargs):
        if DEBUG:
            additional_cats = ['e-journal']
        validations = {
            'type': self.type in ['journal', 'conf', 'epub', 'article', *additional_cats],
            'quality': self.quality in ['q1', 'q2', 'q3', 'q4', 'na'],
            'is_main_or_author': self.is_main_author or self.co_author_count > 0,
            'platform': self.type in ['epub', 'article', *additional_cats] or (self.type in ['journal', 'conf'] and (
                    self.is_scopus or self.is_wos or self.is_ugc or self.is_abdc)),
        }
        error_messages = {
            'type': 'Invalid type. Must be one of: journal, conf, epub, article.',
            'quality': 'Invalid quality. Must be one of: q1, q2, q3, q4.',
            'is_main_or_author': 'Either is_main_author must be true/1 or co_author_count must be greater than 0.',
            'platform': 'Invalid platform. Must be one of: scopus, wos, ugc, abdc for journal/conf types.',
        }
        if not all(validations.values()):
            messages = '\n'.join([error_messages[key] for key, valid in validations.items() if not valid])
            raise Exception(f"Validation Error ({self.internal_id}): \n{messages}")

        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            'internal_ID': self.internal_id,
            'uid': self.uid,
            'Email': self.Email,
            'department': self.department,
            'school': self.school,
            'brief_school': self.brief_school,
            'type': self.type,
            'title': self.title,
            'entity': self.entity,
            'conference_organization': self.conference_organization,
            'conference_level': self.conference_level,
            'quality': self.quality,
            'isbn': self.isbn,
            'mainauthor': '1' if self.is_main_author else '0',
            'coauthor_count': str(self.co_author_count),
            'Is_scopus': '1' if self.is_scopus else '0',
            'is_web_of_science': '1' if self.is_wos else '0',
            'ugc': '1' if self.is_ugc else '0',
            'abdc': '1' if self.is_abdc else '0',
            'month': self.month,
            'yr': self.yr,
            'hash': self.hash,
            'is_rejected': self.is_rejected,
            'is_verified': self.is_verified,
            'remarks': self.remarks
        }

    @staticmethod
    def calculate_hash(data):
        pragma = [
            'internal_ID',
            'uid',
            'Email',
            'department',
            'school',
            'brief_school',
            "month",
            "yr",
            "type",
            "title",
            "entity",
            "quality",
            "isbn",
            "conference_organization",
            "conference_level",
            "mainauthor",
            "coauthor_count",
            "Is_scopus",
            "is_web_of_science",
            "ugc",
            "abdc"
        ]
        import hashlib
        return hashlib.md5('|'.join([data[j] for j in pragma]).encode()).hexdigest()

    def populate(self, data):
        required_fields = [
            'internal_ID',
            'uid',
            'Email',
            'department',
            'school',
            'brief_school',
            "month",
            "yr",
            "type",
            "title",
            "entity",
            "quality",
            "isbn",
            "conference_organization",
            "conference_level",
            "mainauthor",
            "coauthor_count",
            "Is_scopus",
            "is_web_of_science",
            "ugc",
            "abdc"
        ]
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required fields in data")

        self.internal_id = data['internal_ID']
        self.uid = data['uid']
        self.Email = data['Email']
        self.department = data['department']
        self.school = data['school']
        self.brief_school = data['brief_school']
        self.month = data['month']
        self.yr = data['yr']
        self.type = data['type'].lower()
        self.title = data['title']
        self.entity = data['entity']
        self.conference_organization = data['conference_organization']
        self.conference_level = data['conference_level']
        self.quality = data['quality'].lower()
        self.isbn = data['isbn']
        self.is_main_author = data['mainauthor'] == '1'
        self.co_author_count = int(data['coauthor_count'])
        self.is_scopus = data['Is_scopus'] == '1'
        self.is_wos = data['is_web_of_science'] == '1'
        self.is_ugc = data['ugc'] == '1'
        self.is_abdc = data['abdc'] == '1'

    class Meta:
        ordering = ['-yr', '-month']
        verbose_name = 'Paper Record'
        verbose_name_plural = 'Papers Records'


class BookRecords(models.Model):
    internal_id = models.CharField(max_length=16, unique=True)
    faculty = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='book_faculty')
    uid = models.CharField(max_length=16)
    Email = models.CharField(max_length=100)
    department = models.CharField(max_length=500)
    school = models.CharField(max_length=100)
    brief_school = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    yr = models.CharField(max_length=10)
    level = models.CharField(max_length=50)
    title = models.TextField()
    category = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    is_main_author = models.BooleanField()
    co_author_count = models.IntegerField()
    is_editor = models.BooleanField()
    hash = models.CharField(max_length=100)
    is_rejected = models.BooleanField(null=True)
    is_verified = models.BooleanField(null=True)
    remarks = models.TextField()
    rejected_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='book_rejected_by', null=True)
    verified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='book_verified_by', null=True)

    def __str__(self):
        return ' '.join([self.faculty.email, self.internal_id, self.title])

    def save(self, *args, **kwargs):
        error_messages = {
            'level': 'Invalid level. Must be one of: INTERNATIONAL / NATIONAL',
            'category': 'Invalid category. Must be one of research, text, literary',
            'is_main_or_editor': 'Either is_main_author must be true/1 or co_author_count must be greater than 0.',
            'type': 'Invalid type. Must be one of: chapter / book',
        }
        validations = {
            'level': self.level in ['INTERNATIONAL', 'NATIONAL'],
            'category': self.category in ['research', 'text', 'literary'],
            'type': self.type in ['chapter', 'book'],
        }
        if not all(validations.values()):
            import json
            messages = '\n'.join([error_messages[key] for key, valid in validations.items() if not valid]) + f'\n {json.dumps(self.to_dict())}'
            raise Exception(f"Validation Error ({self.internal_id}): \n{messages}")

        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            'internal_ID': self.internal_id,
            'uid': self.uid,
            'Email': self.Email,
            'department': self.department,
            'school': self.school,
            'brief_school': self.brief_school,
            'month': self.month,
            'yr': self.yr,
            'level': self.level,
            'title': self.title,
            'category': self.category,
            'type': self.type,
            'isbn': self.isbn,
            'mainauthor': '1' if self.is_main_author else '0',
            'coauthor_count': str(self.co_author_count),
            'editor': '1' if self.is_editor else '0',
            'hash': self.hash,
            'is_rejected': self.is_rejected,
            'is_verified': self.is_verified,
            'remarks': self.remarks
        }

    @staticmethod
    def calculate_hash(data):
        pragma = [
            'internal_ID',
            'uid',
            'Email',
            'department',
            'school',
            'brief_school',
            'month',
            'yr',
            'level',
            'title',
            'category',
            'type',
            'isbn',
            'mainauthor',
            'coauthor_count',
            'editor',
        ]
        import hashlib
        return hashlib.md5('|'.join([data[j] for j in pragma]).encode()).hexdigest()

    def populate(self, data):
        required_fields = [
            'internal_ID',
            'uid',
            'Email',
            'department',
            'school',
            'brief_school',
            'month',
            'yr',
            'level',
            'title',
            'category',
            'type',
            'isbn',
            'mainauthor',
            'coauthor_count',
            'editor',
        ]
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required fields in data")

        self.internal_id = data['internal_ID']
        self.uid = data['uid']
        self.Email = data['Email']
        self.department = data['department']
        self.school = data['school']
        self.brief_school = data['brief_school']
        self.month = data['month']
        self.yr = data['yr']
        self.level = data['level'].upper()
        self.title = data['title']
        self.category = data['category'].lower()
        self.type = data['type'].lower()
        self.isbn = data['isbn']
        self.is_main_author = data['mainauthor'] == '1'
        self.co_author_count = int(data['coauthor_count'])
        self.is_editor = data['editor'] == '1'

    class Meta:
        ordering = ['-yr', '-month']
        verbose_name = 'Book Record'
        verbose_name_plural = 'Book Records'

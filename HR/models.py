from django.db import models

from APAS.settings import DEBUG
from Account.models import User
from BulkUpload.BulkUploadFoEM.models import ViewScopusWos


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
    is_finalized = models.BooleanField(default=False)
    remarks = models.TextField()
    rejected_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='patent_rejected_by', null=True)
    verified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='patent_verified_by', null=True)

    def __str__(self):
        return ' '.join([self.faculty.email, self.brief_school, self.yr, self.month, self.internal_id])

    def save(self, *args, **kwargs):
        error_messages = {
            'ptn_type': 'ptn_type level. Must be one of: filed, published, granted, licensed.'
        }
        validations = {
            'ptn_type': self.ptn_type in ['filed', 'published', 'granted', 'licensed'],
        }
        if not all(validations.values()):
            import json
            messages = '\n'.join([error_messages[key] for key, valid in validations.items() if not valid]) + f'\n {json.dumps(self.to_dict())}'
            raise Exception(f"Validation Error ({self.internal_id}): \n{messages}")

        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            'internal_ID': self.internal_id,
            'apas_id': self.faculty.username,
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

    @staticmethod
    def bulk_create_prepopulated_data(finalized, model_map, inclusion_map):
        patents = {}
        for i in model_map.keys():
            patents[i] = []
        for i in finalized:
            ptn_model = model_map[inclusion_map[i.faculty]]()
            ptn_model.faculty = i.faculty
            ptn_model.designation = i.faculty.designation_abbreviation
            ptn_model.department = i.department
            ptn_model.description = i.ptn_desc
            ptn_model.application_no = i.application_no
            ptn_model.status = i.ptn_type
            ptn_model.month = i.month
            ptn_model.year = i.yr
            patents[inclusion_map[i.faculty]].append(ptn_model)
        for model, ptns in patents.items():
            if not model_map[model]:
                continue
            model_map[model].objects.bulk_create(ptns)

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
    is_finalized = models.BooleanField(default=False)
    remarks = models.TextField()
    rejected_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='paper_rejected_by', null=True)
    verified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='paper_verified_by', null=True)

    def __str__(self):
        return ' '.join([self.faculty.email, self.internal_id, self.title])

    def save(self, *args, **kwargs):
        if DEBUG:
            additional_cats = []
        validations = {
            'type': self.type.lower() in ['journal', 'conf', 'epub', 'article', *additional_cats],
            'quality': self.type.lower() in ['journal', 'conf', 'epub', 'article'] and self.quality.lower() in ['q1', 'q2', 'q3', 'q4', 'na'],
            'is_main_or_author': self.is_main_author or self.co_author_count > 0,
        }
        error_messages = {
            'type': 'Invalid type. Must be one of: journal, conf, epub, article.',
            'quality': 'Invalid quality. Must be one of: q1, q2, q3, q4.',
            'is_main_or_author': 'Either is_main_author must be true/1 or co_author_count must be greater than 0.',
            'platform': 'Invalid platform. Must be one of: scopus, wos, ugc for journal/conf types.',
        }
        if not all(validations.values()):
            import json
            messages = '\n'.join([error_messages[key] for key, valid in validations.items() if not valid]) + f'\n {json.dumps(self.to_dict())}'
            raise Exception(f"Validation Error ({self.internal_id}): \n{messages}")

        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            'internal_ID': self.internal_id,
            'apas_id': self.faculty.username,
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
        self.type = data['type']
        self.title = data['title']
        self.entity = data['entity']
        self.conference_organization = data['conference_organization']
        self.conference_level = data['conference_level']
        self.quality = data['quality']
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

    @staticmethod
    def bulk_create_prepopulated_data(finalized, model_map, inclusion_map):
        papers = {}
        for i in model_map.keys():
            papers[i] = []
        for i in finalized:
            paper_model = model_map[inclusion_map[i.faculty]]()
            paper_model.faculty = i.faculty
            paper_model.designation = i.faculty.designation_abbreviation
            paper_model.department = i.department
            paper_model.month = i.month
            paper_model.year = i.yr
            paper_model.type = i.type.lower()
            paper_model.title = i.title
            paper_model.entity_name = i.entity
            paper_model.isbn = i.isbn
            paper_model.paper_quality = i.quality.lower()
            if i.type == 'conf':
                paper_model.conference_organization = i.conference_organization
                paper_model.conference_level = i.conference_level
            paper_model.is_main_author = i.is_main_author
            paper_model.co_author_count = i.co_author_count
            paper_model.is_wos = i.is_wos
            paper_model.is_scopus = i.is_scopus
            paper_model.is_ugc = i.is_ugc
            papers[inclusion_map[i.faculty]].append(paper_model)
        for model, ppers in papers.items():
            if not model_map[model]:
                continue
            model_map[model].objects.bulk_create(ppers)


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
    is_finalized = models.BooleanField(default=False)
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
            'level': self.level.upper() in ['INTERNATIONAL', 'NATIONAL'],
            'category': self.category.lower() in ['research', 'text', 'literary'],
            'type': self.type.lower() in ['chapter', 'book'],
        }
        if not all(validations.values()):
            import json
            messages = '\n'.join([error_messages[key] for key, valid in validations.items() if not valid]) + f'\n {json.dumps(self.to_dict())}'
            raise Exception(f"Validation Error ({self.internal_id}): \n{messages}")

        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            'internal_ID': self.internal_id,
            'apas_id': self.faculty.username,
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
        self.level = data['level']
        self.title = data['title']
        self.category = data['category']
        self.type = data['type']
        self.isbn = data['isbn']
        self.is_main_author = data['mainauthor'] == '1'
        self.co_author_count = int(data['coauthor_count'])
        self.is_editor = data['editor'] == '1'

    class Meta:
        ordering = ['-yr', '-month']
        verbose_name = 'Book Record'
        verbose_name_plural = 'Book Records'

    @staticmethod
    def bulk_create_prepopulated_data(finalized, model_map, inclusion_map):
        books = {}
        for i in model_map.keys():
            books[i] = []
        for i in finalized:
            book_model = model_map[inclusion_map[i.faculty]]()
            book_model.faculty = i.faculty
            book_model.designation = i.faculty.designation_abbreviation
            book_model.department = i.department
            book_model.month = i.month
            book_model.year = i.yr
            book_model.level = i.level.upper()
            book_model.title = i.title
            book_model.category = i.category.lower()
            book_model.type = i.type.lower()
            book_model.is_main_author = i.is_main_author
            book_model.co_author_count = i.co_author_count
            book_model.is_editor = i.is_editor
            books[inclusion_map[i.faculty]].append(book_model)
        for model, book in books.items():
            if not model_map[model]:
                continue
            model_map[model].objects.bulk_create(book)
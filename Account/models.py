from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

# Create your models here.
# create custome user model
schools = {
    'SOT': 'School of Technology',
    'SPM': 'School of Petroleum Management',
    'SPT': 'School of Petroleum Technology',
    'SLS': 'School of Liberal Studies',
    'PDPU': 'PDPU',
    'PDEU': 'PDEU'
}
designations = {'assistant_prof_on_contract': 'Assistant Professor (On Contract)',
                'prof': 'Professor',
                'associate_prof': 'Associate Professor',
                'assistant_prof': 'Assistant Professor',
                'DIRECTOR': 'DIRECTOR',
                'ADJUNCT PROFESSOR': 'Adjunct Professor',
                'Librarian': 'Librarian',
                'Senior Manager': 'Senior Manager',
                'Assistant Librarian': 'Assistant Librarian',
                'Manager (Student Affairs)': 'Manager',
                'Manager': 'Manager',
                'Technician': 'Technician',
                'Library Assistant': 'Library Assistant',
                'Assistant Manager': 'Assistant Manager',
                'Lab Assistant': 'Lab Assistant',
                'Senior Executive': 'Senior Executive',
                'PA to DG': 'PA to DG',
                'Executive': 'Executive',
                'PA to Director': 'PA to Director',
                'Senior Manager(Legal & Co-Ordination)': 'Senior Manager(Legal & Co-Ordination)',
                'Security Officer': 'Security Officer',
                'Engineer Electrical': 'Engineer Electrical',
                'Hostel Warden': 'Hostel Warden',
                'Junior Engineer': 'Junior Engineer',
                'Assistant': 'Assistant',
                'Project Coordinator': 'Project Coordinator',
                'Administrative Assistant': 'Administrative Assistant',
                'Assistant Registrar ( Academics)': 'Assistant Registrar ( Academics)',
                'Senior Assistant': 'Senior Assistant',
                'CCM': 'CCM',
                'REGISTRAR ': 'REGISTRAR ',
                'CHRO': 'CHRO',
                'CFO': 'CFO',
                'DG': 'DG',
                'adjunct_professor': 'ADJUNCT PROFESSOR',
                'stf': 'STAFF'
                }
designation_names = {}
for i in designations.values():
    designation_names[i] = i

designation_abbrs = {}
for i in designations.keys():
    designation_abbrs[i] = i

roles = {'ro': 'Reviewing Officer',
         'fac': 'Faculty',
         'dir': 'Director',
         'hr': 'Human Resources',
         'stf': 'Staff'
         }
departments = {'SPT': 'SOT',
               'SPM': 'SPM',
               'SLS': 'SLS',
               'Chemical Engineering': 'Chemical Engineering',
               'Civil Department': 'Civil Department',
               'COMPUTER ENGINEERING': 'COMPUTER ENGINEERING',
               'SOT': 'COMPUTER ENGINEERING',
               'ICT': 'ICT',
               'ELECTRICAL': 'ELECTRICAL',
               'MECHANICAL': 'MECHANICAL',
               'Industrial Engineering': 'Industrial Engineering',
               'Nuclear Engineering': 'Nuclear Engineering',
               'SOLAR ENERGY': 'SOLAR ENERGY',
               'science': 'Department of Science',
               'maths': 'MATHEMATICS',
               'LIBRARY SPM': 'LIBRARY SPM',
               'SOT ADMIN': 'SOT ADMIN',
               'LIBRARY SLS': 'LIBRARY SLS',
               'Facility Management and Administration': 'Facility Management and Administration',
               'FINANCE & ACCOUNTS': 'FINANCE & ACCOUNTS',
               'ADMINISTRATION': 'ADMINISTRATION',
               'Student Affairs': 'ADMINISTRATION',
               'H.R.': 'H.R.',
               'SPM ADMIN': 'SPM ADMIN',
               'SPT ADMIN': 'SPT ADMIN',
               'PLACEMENT & TRAINING': 'PLACEMENT & TRAINING',
               'SLS ADMIN': 'SLS ADMIN',
               'Computer Lab SOT': 'Computer Lab SOT',
               'OFFICE OF RESEARCH AND SPONSORED PROGRAM': 'OFFICE OF RESEARCH AND SPONSORED PROGRAM',
               'Admin': 'Admin',
               'EXAMINATION SECTION': 'EXAMINATION SECTION',
               'OFFICE OF INTERNATIONAL RELATIONS': 'OFFICE OF INTERNATIONAL RELATIONS',
               'PLANNING & DEVELOPMENT': 'PLANNING & DEVELOPMENT',
               'SAIL': 'SAIL',
               'CONSTRUCTION': 'CONSTRUCTION',
               'COORDINATION AND LEGAL': 'COORDINATION AND LEGAL',
               'PDPU IT': 'PDPU IT',
               'SRDC': 'SRDC',
               'CENTRAL ADMISSION OFFICE': 'CENTRAL ADMISSION OFFICE',
               'Languages, Literature & Aesthetics': 'Languages, Literature & Aesthetics',
               'REGISTRAR  OFFICE': 'REGISTRAR  OFFICE',
               'HUMAN RESOURCE': 'HUMAN RESOURCE',
               'DG': 'DG',
               'PETROLEUM TECHNOLOGY': 'PETROLEUM TECHNOLOGY',
               'F&A': 'F&A'
               }

department_name = {}
for i in departments.values():
    department_name[i] = i

department_abbrs = {}
for i in departments.keys():
    department_abbrs[i] = i


class User(AbstractUser):
    mid = models.CharField(max_length=10, null=True, default=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=50, choices=designation_names.items())
    type = models.CharField(max_length=50, choices=[
        ('Faculty', 'Faculty'),
        ('Staff', 'Staff'),
    ])
    full_name = models.CharField(max_length=1024, default="Unset")
    roles = models.CharField(max_length=100, choices=roles.items(), default=None, null=True)
    department = models.CharField(max_length=100, null=True, blank=True)#, choices=department_name.items(), auto_created=True)
    school = models.CharField(max_length=100, choices=(
        ('School of Technology', 'School of Technology'),
        ('School of Petroleum Management', 'School of Petroleum Management'),
        ('School of Petroleum Technology', 'School of Petroleum Technology'),
        ('School of Liberal Studies', 'School of Liberal Studies'),
        ('PDPU', 'PDPU'),
        ('PDEU', 'PDEU')
    ))

    designation_abbreviation = models.CharField(max_length=50, choices=designation_abbrs.items(), auto_created=True, null=True)
    department_abbreviation = models.CharField(max_length=100, null=True)
    school_abbreviation = models.CharField(max_length=100, choices=(
        ('SOT', 'SOT'),
        ('SPM', 'SPM'),
        ('SPT', 'SPT'),
        ('SLS', 'SLS'),
        ('PDPU', 'PDPU'),
        ('PDEU', 'PDEU')
    ))
    date_joined = models.DateTimeField(auto_now_add=True)

    ro1_id = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='ro1')
    ro2_id = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='ro2')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    is_ro1 = models.BooleanField(default=False)
    is_ro2 = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'designation', 'department', 'school']

    def __str__(self):
        return self.email


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, designation, type, full_name, roles, department, school,
                    designation_abbreviation, department_abbreviation, school_abbreviation, is_staff, is_admin, is_hr,
                    is_ro1, is_ro2, mid, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not designation:
            raise ValueError('Users must have an designation')
        if not department:
            raise ValueError('Users must have an department')
        if not school:
            raise ValueError('Users must have an school')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            designation=designation,
            department=department,
            school=school,
        )
        user.type = type
        user.full_name = full_name
        user.roles = roles
        user.designation_abbreviation = designation_abbreviation
        user.department_abbreviation = department_abbreviation
        user.school_abbreviation = school_abbreviation
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.is_hr = is_hr
        user.is_ro1 = is_ro1
        user.is_ro2 = is_ro2
        user.mid = mid
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, designation, department, school, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            designation=designation,
            department=department,
            school=school,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_hr(self, email, username, designation, department, school, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            designation=designation,
            department=department,
            school=school,
        )
        user.is_hr = True
        user.save(using=self._db)
        return user

    def create_ro1(self, email, username, designation, department, school, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            designation=designation,
            department=department,
            school=school,
        )
        user.is_ro1 = True
        user.save(using=self._db)
        return user

    def create_ro2(self, email, username, designation, department, school, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            designation=designation,
            department=department,
            school=school,
        )
        user.is_ro2 = True
        user.save(using_db=self._db)


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    token = models.UUIDField(auto_created=True, default=uuid4, editable=False)
    reset_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}, {self.created_at}"

    class Meta:
        verbose_name_plural = "Password Reset Requests"
        
        


class DualRole(models.Model):
    main_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='main_user', verbose_name='Main User (Staff Profile)', unique=True)
    faculty_profile = models.ForeignKey(User, on_delete=models.PROTECT, related_name='faculty_profile', verbose_name='Alternate Profile (Faculty Profile)', unique=True)

    def __str__(self):
        return f"Staff: {self.main_user.username}, Faculty:{self.faculty_profile.username}"

    def cleanup(self):
        self.main_user.password = self.faculty_profile.password
        self.faculty_profile.save()

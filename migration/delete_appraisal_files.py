from Faculty.FacultyFOET.models import *
from Faculty.FacultyMaths.models import *
from Faculty.FacultySLS.models import *
from Faculty.FacultyScience.models import *
from Faculty.FacultySoEM.models import *

faculties = [
    'anirbid.sircar',
    'busupalli.balanagulu',
    'surendra.sasikumar',
    'brajesh.jha',
    'manish.sinha',
    'rajib.bandyopadhyay',
    'tejas.thaker',
    'Prakash.Chandra',
    'Shreekant.Varshney',
    'manoj.kumar',
    'samir.patel',
    'niragi.dave',
    'tajinder.singh',
    'Amitava.Choudhury',
    'Mayank.G',
    'sk.dash',
    'nirav.patel',
    'n.madhavan',
    'bharti.saini',
    'namrata.bist',
    'prahlad.baruah',
    'rohit.s',
    'dhaval.pujara',
    'abhishek.gor',
    'Ravi.Tejasvi',
    'nandini.modi',
    'Himanshu.chokshi',
    'Subhankar.Roy',
    'Vivek.Pandit',
    'Mahesh.Jallu',
    'nitin.chaudhari',
    'debasis.sarkar',
    'Pradeep.PS',
    'vinay.vakharia',
    'mohendra.roy',
    'brijesh.tripathi',
    'santosh.bharti',
    'kalisadhan.mukherjee',
    'Anup.Sanchela',
    'Shabiimam.ma',
    'Md.Aurangzeb',
    'pavan.gurrala',
    'Shirsendu.Mitra',
    'sheetal.rawat',
    'sivakumar.p',
    'ankur.solanki',
    'Kaushal.Shah',
]


def delete_appraisal_files():
    models = [
        FOETAssistantProfOnContractAppraisalFile,
        FOETAssistantProfAppraisalFile,
        FOETAssociateProfAppraisalFile,
        FOETProfAppraisalFile,
        MathAssistantProfOnContractAppraisalFile,
        MathAssistantProfAppraisalFile,
        MathAssociateProfAppraisalFile,
        MathProfAppraisalFile,
        ScienceAssistantProfOnContractAppraisalFile,
        ScienceAssistantProfAppraisalFile,
        ScienceAssociateProfAppraisalFile,
        ScienceProfAppraisalFile,
        FOLSAssistantProfOnContractAppraisalFile,
        FOLSAssistantProfAppraisalFile,
        FOLSAssociateProfAppraisalFile,
        FOLSProfAppraisalFile,
        FOEMAssistantProfOnContractAppraisalFile,
        FOEMAssistantProfAppraisalFile,
        FOEMAssociateProfAppraisalFile,
        FOEMProfAppraisalFile,
    ]
    files = []
    for model in models:
        for faculty in faculties:
            try:
                file = model.objects.get(user__username=faculty)
                files.append(file)
            except model.DoesNotExist:
                pass
    for file in files:
        file.delete()

delete_appraisal_files()

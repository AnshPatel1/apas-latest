from django.db import transaction

import BulkUpload.BulkUploadFoEM.models as BulkUploadFoEM
import BulkUpload.BulkUploadFoET.models as BulkUploadFoET
import BulkUpload.BulkUploadFoLS.models as BulkUploadFoLS
import BulkUpload.BulkUploadMaths.models as BulkUploadMaths
import BulkUpload.BulkUploadScience.models as BulkUploadScience

school_mode_map = {
    'FoET': BulkUploadFoET,
    'FoLS': BulkUploadFoLS,
    'FoEM': BulkUploadFoEM,
    'Maths': BulkUploadMaths,
    'Science': BulkUploadScience
}


def delete_duplicate_books():
    foet_ids = [755]
    books = BulkUploadFoET.ViewBook.objects.filter(id__in=foet_ids)
    faculty_usernames = []
    for book in books:
        faculty_usernames.append(book.faculty.username)
        book.delete()
    return faculty_usernames


def delete_papers():
    ids = {
        'FoET': [4800, 4282, 4776, 4281, 4597, 4844, 4652, 4653, 4256, 4342, 4474, 4102, 4813, 4817, 4731, 4315, 4778,
                 4058, 4291, 4654, 4387, 4057, 4645, 4727, 4524, 4103, 4821, 4766, 4553, 4789, 4341, 4779, 4780, 4448,
                 4680, 4275, 4804, 4104, 4814, 4476, 4374, 4375, 4843],
        'Maths': [238, 236, 229, 271, 232, ],
        'Science': [860, 714, 857, 865, 878, 775, 853, 743, 851, 780, 844, 770, 702, 737, 785, 761, 787, 753, 883, 845,
                    789]
    }
    faculty_usernames = []
    for school, ids in ids.items():
        papers = school_mode_map[school].ViewScopusWos.objects.filter(id__in=ids)
        for paper in papers:
            faculty_usernames.append(paper.faculty.username)
            paper.delete()
    return faculty_usernames


def delete_patents():
    ids = {
        'Science': [74, 75, 73],
        'FoET': [686, 779, 702, 767, 664, 665, 773, 855]
    }
    faculty_usernames = []
    for school, ids in ids.items():
        patents = school_mode_map[school].ViewPatent.objects.filter(id__in=ids)
        for patent in patents:
            faculty_usernames.append(patent.faculty.username)
            patent.delete()
    return faculty_usernames


def main():
    with transaction.atomic():
        faculty_usernames = delete_duplicate_books() + delete_papers() + delete_patents()
        faculty_usernames = list(set(faculty_usernames))
        print('\n'.join(faculty_usernames))

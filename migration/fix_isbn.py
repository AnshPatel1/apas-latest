from HR.models import BookRecords
import BulkUpload.BulkUploadFoEM.models as BulkUploadFoEM
import BulkUpload.BulkUploadFoET.models as BulkUploadFoET
import BulkUpload.BulkUploadFoLS.models as BulkUploadFoLS
import BulkUpload.BulkUploadMaths.models as BulkUploadMaths
import BulkUpload.BulkUploadScience.models as BulkUploadScience
import Faculty.FacultySoEM.models as ModelsFoEM
import Faculty.FacultyFOET.models as ModelsFoET
import Faculty.FacultySLS.models as ModelsFoLS
import Faculty.FacultyMaths.models as ModelsMaths
import Faculty.FacultyScience.models as ModelsScience

models = [
    BulkUploadFoEM.ViewBook,
    BulkUploadFoET.ViewBook,
    BulkUploadFoLS.ViewBook,
    BulkUploadMaths.ViewBook,
    BulkUploadScience.ViewBook,
    ModelsFoEM.Publication,
    ModelsFoET.Publication,
    ModelsFoLS.Publication,
    ModelsMaths.Publication,
    ModelsScience.Publication,
]

def fix_isbn():
    book_isbn_map = {}
    duplicates = {}
    for book in BookRecords.objects.filter(is_finalized=True):
        uniq_key = f"{book.title}apas_deploy_split{book.month}apas_deploy_split{book.yr}"
        if uniq_key not in book_isbn_map:
            book_isbn_map[uniq_key] = book.isbn
        else:
            if book_isbn_map[uniq_key] != book.isbn:
                if uniq_key not in duplicates:
                    duplicates[uniq_key] = []
                duplicates[uniq_key].append(book.isbn)
                duplicates[uniq_key].append(book_isbn_map[uniq_key])
    for title, dups in duplicates.items():
        print(f"Title: {title}, ISBNs: {', '.join(list(set(dups)))}")
    count = {}
    for uniq_key, isbn in book_isbn_map.items():
        title = uniq_key.split("apas_deploy_split")[0]
        month = int(uniq_key.split("apas_deploy_split")[1])
        year = int(uniq_key.split("apas_deploy_split")[2])
        for model in models:
            books = model.objects.filter(title=title, month=month, year=year)
            books.update(isbn=isbn)
            if str(model) not in count:
                count[str(model)] = 0
            count[str(model)] += books.count()
    print(count)


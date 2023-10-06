from Staff.models import StaffAppraisalFile, StaffConfiguration

for file in StaffAppraisalFile.objects.filter(file_level="RO2").union(
        StaffAppraisalFile.objects.filter(file_level="HR")):
    file.total_marks.ro1 = file.total_marks.ro1 + 0.01
    file.total_marks.ro2 = file.total_marks.ro2 + 0.01
    file.total_marks.ro1 = round(file.total_marks.ro1, 0)
    file.total_marks.ro2 = round(file.total_marks.ro2, 0)
    file.total_marks.save()
    if file.total_marks.ro1 >= 85:
        file.grade_received_ro1 = "Outstanding"
    elif file.total_marks.ro1 >= 65:
        file.grade_received_ro1 = "Good"
    elif file.total_marks.ro1 >= 39:
        file.grade_received_ro1 = "Average"
    elif file.total_marks.ro1 <= 38:
        file.grade_received_ro1 = "Below Average"
    if file.total_marks.ro2 >= 85:
        file.grade_received_ro2 = "Outstanding"
    elif file.total_marks.ro2 >= 65:
        file.grade_received_ro2 = "Good"
    elif file.total_marks.ro2 >= 39:
        file.grade_received_ro2 = "Average"
    elif file.total_marks.ro2 <= 38:
        file.grade_received_ro2 = "Below Average"
    file.save()
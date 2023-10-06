from django.db import models


class FacultyValidator(models.Model):
    teaching_validated = models.BooleanField(default=False)
    research_validated = models.BooleanField(default=False)
    project_validated = models.BooleanField(default=False)
    phd_validated = models.BooleanField(default=False)
    dissertation_validated = models.BooleanField(default=False)
    award_validated = models.BooleanField(default=False)
    consultancy_validated = models.BooleanField(default=False)
    academia_collab_validated = models.BooleanField(default=False)
    international_admission_validated = models.BooleanField(default=False)
    arranging_conferences_validated = models.BooleanField(default=False)
    mentorship_validated = models.BooleanField(default=False)
    attending_conferences_validated = models.BooleanField(default=False)
    community_development_validated = models.BooleanField(default=False)
    extra_curricular_validated = models.BooleanField(default=False)
    additional_validated = models.BooleanField(default=False)
    senior_feedback_validated = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}: Validator Object'

    def is_valid(self, contracted):
        if contracted:
            self.phd_validated = True
        if not contracted:
            self.consultancy_validated = True
        self.save()
        return self.teaching_validated and \
            self.phd_validated and \
            self.dissertation_validated and \
            self.consultancy_validated and \
            self.arranging_conferences_validated \
            and self.mentorship_validated and \
            self.attending_conferences_validated and \
            self.community_development_validated and \
            self.additional_validated

    def is_valid_for_ro(self, contracted):
        # check if all the fields are validated
        if contracted:
            self.phd_validated = True
            self.save()
        if self.teaching_validated and \
                self.research_validated and \
                self.project_validated and \
                self.phd_validated and \
                self.dissertation_validated and \
                self.award_validated and \
                self.consultancy_validated and \
                self.academia_collab_validated and \
                self.international_admission_validated and \
                self.arranging_conferences_validated and \
                self.mentorship_validated and \
                self.attending_conferences_validated and \
                self.community_development_validated and \
                self.extra_curricular_validated and \
                self.additional_validated and \
                self.senior_feedback_validated:
            return True
        else:
            return False

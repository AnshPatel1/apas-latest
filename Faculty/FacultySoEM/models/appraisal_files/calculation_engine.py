# noinspection DuplicatedCode
from . import FOEMAssistantProfOnContractAppraisalFile, FOEMAssistantProfAppraisalFile, FOEMAssociateProfAppraisalFile, \
    FOEMProfAppraisalFile
from .. import MarkField


class CalculationEngine:
    """This class represents a calculation engine, which is a set of rules
    that can be used to calculate the value of an appraisal.
    """

    def __init__(self,
                 file: FOEMAssistantProfOnContractAppraisalFile | FOEMAssistantProfAppraisalFile | FOEMAssociateProfAppraisalFile | FOEMProfAppraisalFile):
        # self.is_on_contract = is_on_contract
        self.file = file

    def calculateGrandTotal(self):
        total = 0
        total += self.calculatePartA()
        total += self.calculatePartB()
        total += self.calculateAdditionalTotal()
        return round(total + 0.01, 0)

    def calculatePartA(self):
        total = 0
        total += self.calculateTeachingMaster()
        total += self.calculateSection2()
        total += self.calculateSection3()
        total += self.calculateSection4()

        return total

    def calculateTeachingMaster(self):
        total = 0
        total += self.calculateTeachingLoad()
        total += self.calculateStudentFeedback()
        total += self.calculateBooksAndPublications()
        total += self.calculateAcademicPractices()
        total += self.calculateExaminationDuty()
        return total

    def calculateTeachingLoad(self):
        tl_avg = (self.file.teaching_load.semester_odd + self.file.teaching_load.semester_even) / 2
        if tl_avg >= self.file.configuration.teaching_load_upper_limit:
            return round(
                self.file.configuration.teaching_load_upper_limit * self.file.configuration.teaching_load_t_coefficient,
                0)
        elif tl_avg <= self.file.configuration.teaching_load_lower_limit:
            return round(
                self.file.configuration.teaching_load_lower_limit * self.file.configuration.teaching_load_t_coefficient,
                0)
        else:
            return round(tl_avg * self.file.configuration.teaching_load_t_coefficient, 0)

    def calculateStudentFeedback(self):
        st_load = self.file.student_feedback
        if st_load <= self.file.configuration.students_feedback_lower_limit:
            return round(
                self.file.configuration.students_feedback_lower_limit * self.file.configuration.students_feedback_s_coefficient,
                0)
        else:
            return round(st_load * self.file.configuration.students_feedback_s_coefficient, 0)

    def calculateExaminationDuty(self):
        total = 0
        total += self.file.exam_duty.timely_invigilation
        total += self.file.exam_duty.paper_setting
        total += self.file.exam_duty.evaluation
        total += self.file.exam_duty.result_submission
        return total

    def calculateBooksAndPublications(self):
        # research based on books and publications
        total = 0
        _books = []  # new
        _chapters = []  # new
        for book in self.file.research_books.all():
            if book.marks.ro1_agreed:
                if book.type == 'book':
                    total += self.file.configuration.section_1e_i_per_book_per_author
                    book.marks.ro1 = self.file.configuration.section_1e_i_per_book_per_author
                    _books.append(self.file.configuration.section_1e_i_per_book_per_author)
                else:
                    total += self.file.configuration.section_1e_i_per_chapter
                    book.marks.ro1 = self.file.configuration.section_1e_i_per_chapter
                    _chapters.append(self.file.configuration.section_1e_i_per_chapter)
            else:
                book.marks.ro1 = 0
            book.marks.save()

        for book in self.file.literary_books.all():
            if book.marks.ro1_agreed:
                if book.type == 'book':
                    total += self.file.configuration.section_1e_ii_per_book_per_author
                    book.marks.ro1 = self.file.configuration.section_1e_ii_per_book_per_author
                    _books.append(self.file.configuration.section_1e_ii_per_book_per_author)
                else:
                    total += self.file.configuration.section_1e_ii_per_chapter
                    book.marks.ro1 = self.file.configuration.section_1e_ii_per_chapter
                    _chapters.append(self.file.configuration.section_1e_ii_per_chapter)
            else:
                book.marks.ro1 = 0
            book.marks.save()
        for book in self.file.textbooks.all():
            if book.marks.ro1_agreed:
                if book.type == 'book':
                    if book.publication_level == 'national':
                        total += self.file.configuration.section_1e_iii_per_national_book_per_author
                        book.marks.ro1 = self.file.configuration.section_1e_iii_per_national_book_per_author
                        _books.append(self.file.configuration.section_1e_iii_per_national_book_per_author)

                    elif book.publication_level == 'international':
                        total += self.file.configuration.section_1e_iii_per_international_book_per_author
                        book.marks.ro1 = self.file.configuration.section_1e_iii_per_international_book_per_author
                        _books.append(self.file.configuration.section_1e_iii_per_international_book_per_author)
                else:
                    total += self.file.configuration.section_1e_iii_per_chapter
                    book.marks.ro1 = self.file.configuration.section_1e_iii_per_chapter
                    _chapters.append(self.file.configuration.section_1e_iii_per_chapter)
            else:
                book.marks.ro1 = 0
            book.marks.save()
        _total = 0  # new
        _books.sort(reverse=True)  # new
        _chapters.sort(reverse=True)  # new
        if len(_books) > 0:  # new
            _total += _books[0]  # new
        if len(_chapters) > 0:  # new
            _total += _chapters[0]  # new
        if len(_chapters) > 1:  # new
            _total += _chapters[1]  # new
        return _total  # new

    def calculateAcademicPractices(self):
        return self.file.modern_teaching_methods.marks.ro1 + self.file.upkeep_of_course_files_marks.ro1 + self.file.inclusion_of_alumni_marks.ro1

    def calculateSection2(self):
        total = 0
        total += self.calculateResearchMaster()
        total += self.calculateProjects()
        if not self.file.user.designation_abbreviation == 'assistant_prof_on_contract':
            total += self.calculatePhDGuidance()
        total += self.calculateDissertationAll()
        total += self.calculateAwards()
        total += self.calculateSectionE()
        total += self.calculateAcademiaCollaboration()
        return total

    def calculateResearchMaster(self):
        total = 0
        total += self.calculatePapers()
        total += self.calculateConferences()
        total += self.calculateEPublications()
        return total

    def calculatePapers(self):
        total = 0
        main_author_cut = 0.7
        co_author_cut = 0.3
        for paper in self.file.publications_in_scopus_wos.all():
            if paper.marks.ro1_agreed:
                if paper.is_main_author:
                    if paper.category == 'scopus':
                        if paper.quality == 'q1':
                            total += self.file.configuration.section_2a_a_i_per_scopus_q1 * main_author_cut
                            paper.marks.ro1 = self.file.configuration.section_2a_a_i_per_scopus_q1 * main_author_cut
                        elif paper.quality == 'q2':
                            total += self.file.configuration.section_2a_a_i_per_scopus_q2 * main_author_cut
                            paper.marks.ro1 = self.file.configuration.section_2a_a_i_per_scopus_q2 * main_author_cut
                        elif paper.quality == 'q3':
                            total += self.file.configuration.section_2a_a_i_per_scopus_q3 * main_author_cut
                            paper.marks.ro1 = self.file.configuration.section_2a_a_i_per_scopus_q3 * main_author_cut
                        elif paper.quality == 'q4':
                            total += self.file.configuration.section_2a_a_i_per_scopus_q4 * main_author_cut
                            paper.marks.ro1 = self.file.configuration.section_2a_a_i_per_scopus_q4 * main_author_cut
                    elif paper.category == 'wos':
                        total += self.file.configuration.section_2a_a_i_per_wos * main_author_cut
                        paper.marks.ro1 = self.file.configuration.section_2a_a_i_per_wos * main_author_cut
                    elif paper.category == 'ugc' or paper.category == 'sci' or paper.category == 'abdc':
                        total += self.file.configuration.section_2a_a_ii_per_publication * main_author_cut
                        paper.marks.ro1 = self.file.configuration.section_2a_a_ii_per_publication * main_author_cut
                else:
                    if paper.category == 'scopus':
                        if paper.quality == 'q1':
                            total += (
                                        self.file.configuration.section_2a_a_i_per_scopus_q1 * co_author_cut)  # / paper.co_author_count
                            paper.marks.ro1 = (
                                        self.file.configuration.section_2a_a_i_per_scopus_q1 * co_author_cut)  # / paper.co_author_count
                        elif paper.quality == 'q2':
                            total += (
                                        self.file.configuration.section_2a_a_i_per_scopus_q2 * co_author_cut)  # / paper.co_author_count
                            paper.marks.ro1 = (
                                        self.file.configuration.section_2a_a_i_per_scopus_q2 * co_author_cut)  # / paper.co_author_count
                        elif paper.quality == 'q3':
                            total += (
                                        self.file.configuration.section_2a_a_i_per_scopus_q3 * co_author_cut)  # / paper.co_author_count
                            paper.marks.ro1 = (
                                        self.file.configuration.section_2a_a_i_per_scopus_q3 * co_author_cut)  # / paper.co_author_count
                        elif paper.quality == 'q4':
                            total += (
                                        self.file.configuration.section_2a_a_i_per_scopus_q4 * co_author_cut)  # / paper.co_author_count
                            paper.marks.ro1 = (
                                        self.file.configuration.section_2a_a_i_per_scopus_q4 * co_author_cut)  # / paper.co_author_count
                    elif paper.category == 'wos':
                        total += (
                                    self.file.configuration.section_2a_a_i_per_wos * co_author_cut)  # / paper.co_author_count
                        paper.marks.ro1 = (
                                    self.file.configuration.section_2a_a_i_per_wos * co_author_cut)  # / paper.co_author_count
                    elif paper.category == 'ugc' or paper.category == 'sci' or paper.category == 'abdc':
                        total += self.file.configuration.section_2a_a_ii_per_publication * co_author_cut
                        paper.marks.ro1 = self.file.configuration.section_2a_a_ii_per_publication * co_author_cut
            else:
                paper.marks.ro1 = 0
            paper.marks.save()
        return round(total, 2)

    def calculateConferences(self):
        total = 0
        main_author_cut = 0.7
        co_author_cut = 0.3
        for paper in self.file.conference_proceedings_scopus_wos.all():
            if paper.marks.ro1_agreed:
                if paper.is_main_author:
                    total += self.file.configuration.section_2a_a_ii_per_conference * main_author_cut
                    paper.marks.ro1 = self.file.configuration.section_2a_a_ii_per_conference * main_author_cut
                else:
                    total += self.file.configuration.section_2a_a_ii_per_conference * co_author_cut
                    paper.marks.ro1 = self.file.configuration.section_2a_a_ii_per_conference * co_author_cut
                # if paper.is_main_author:
                #     if paper.category == 'scopus':
                #         if paper.quality == 'q1':
                #             total += self.file.configuration.section_2a_a_ii_per_scopus_q1 * main_author_cut
                #             paper.marks.ro1 = self.file.configuration.section_2a_a_ii_per_scopus_q1 * main_author_cut
                #         elif paper.quality == 'q2':
                #             total += self.file.configuration.section_2a_a_ii_per_scopus_q2 * main_author_cut
                #             paper.marks.ro1 = self.file.configuration.section_2a_a_ii_per_scopus_q2 * main_author_cut
                #         elif paper.quality == 'q3':
                #             total += self.file.configuration.section_2a_a_ii_per_scopus_q3 * main_author_cut
                #             paper.marks.ro1 = self.file.configuration.section_2a_a_ii_per_scopus_q3 * main_author_cut
                #         elif paper.quality == 'q4':
                #             total += self.file.configuration.section_2a_a_ii_per_scopus_q4 * main_author_cut
                #             paper.marks.ro1 = self.file.configuration.section_2a_a_ii_per_scopus_q4 * main_author_cut
                #     elif paper.category == 'wos':
                #         total += self.file.configuration.section_2a_a_i_per_wos * main_author_cut
                #         paper.marks.ro1 = self.file.configuration.section_2a_a_i_per_wos * main_author_cut
                # else:
                #     if paper.category == 'scopus':
                #         if paper.quality == 'q1':
                #             total += (self.file.configuration.section_2a_a_ii_per_scopus_q1 * co_author_cut)  # / paper.co_author_count
                #             paper.marks.ro1 = (self.file.configuration.section_2a_a_ii_per_scopus_q1 * co_author_cut)  # / paper.co_author_count
                #         elif paper.quality == 'q2':
                #             total += (self.file.configuration.section_2a_a_ii_per_scopus_q2 * co_author_cut)  # / paper.co_author_count
                #             paper.marks.ro1 = (self.file.configuration.section_2a_a_ii_per_scopus_q2 * co_author_cut)  # / paper.co_author_count
                #         elif paper.quality == 'q3':
                #             total += (self.file.configuration.section_2a_a_ii_per_scopus_q3 * co_author_cut)  # / paper.co_author_count
                #             paper.marks.ro1 = (self.file.configuration.section_2a_a_ii_per_scopus_q3 * co_author_cut)  # / paper.co_author_count
                #         elif paper.quality == 'q4':
                #             total += (self.file.configuration.section_2a_a_ii_per_scopus_q4 * co_author_cut)  # / paper.co_author_count
                #             paper.marks.ro1 = (self.file.configuration.section_2a_a_ii_per_scopus_q4 * co_author_cut)  # / paper.co_author_count
                #     elif paper.category == 'wos':
                #         total += (self.file.configuration.section_2a_a_ii_per_wos * co_author_cut)  # / paper.co_author_count
                #         paper.marks.ro1 = (self.file.configuration.section_2a_a_ii_per_wos * co_author_cut)  # / paper.co_author_count
            else:
                paper.marks.ro1 = 0
            paper.marks.save()
        return round(total, 2)

    def calculateEPublications(self):
        count = 0
        total = 0
        for pub in self.file.e_publications_articles.all():
            if count >= 2:
                break
            if pub.marks.ro1_agreed:
                count += 1
                total += self.file.configuration.section_2a_b_per_e_publication
                pub.marks.ro1 = self.file.configuration.section_2a_b_per_e_publication
            else:
                pub.marks.ro1 = 0
            pub.marks.save()
        return round(total, 2)

    def calculateProjects(self):
        total = 0
        osrp_count = 0
        for project in self.file.projects.all():
            if project.marks.ro1_agreed:
                if project.project_category == 'INS':
                    total += project.marks.ro1
                elif project.project_category == 'OSRP' and self.file.user.designation_abbreviation == 'assistant_prof_on_contract':
                    if osrp_count > 0:
                        continue
                    osrp_count += 1
                    total += self.file.configuration.section_2a_c_category_osrp_student_research_project
                    project.marks.ro1 = self.file.configuration.section_2a_c_category_osrp_student_research_project
                elif project.project_participation == 'pi':
                    if project.project_category == 'MAJOR':
                        total += self.file.configuration.section_2a_c_category_major_per_pi
                        project.marks.ro1 = self.file.configuration.section_2a_c_category_major_per_pi
                    elif project.project_category == 'MEDIUM':
                        total += self.file.configuration.section_2a_c_category_medium_per_pi
                        project.marks.ro1 = self.file.configuration.section_2a_c_category_medium_per_pi
                    elif project.project_category == 'MINOR':
                        total += self.file.configuration.section_2a_c_category_minor_per_pi
                        project.marks.ro1 = self.file.configuration.section_2a_c_category_minor_per_pi
                elif project.project_participation == 'copi':
                    if project.project_category == 'MAJOR':
                        total += self.file.configuration.section_2a_c_category_major_per_co_pi
                        project.marks.ro1 = self.file.configuration.section_2a_c_category_major_per_co_pi
                    elif project.project_category == 'MEDIUM':
                        total += self.file.configuration.section_2a_c_category_medium_per_co_pi
                        project.marks.ro1 = self.file.configuration.section_2a_c_category_medium_per_co_pi
                    elif project.project_category == 'MINOR':
                        total += self.file.configuration.section_2a_c_category_minor_per_co_pi
                        project.marks.ro1 = self.file.configuration.section_2a_c_category_minor_per_co_pi

            project.marks.save()
        return round(total, 2)

    def calculatePhDGuidance(self):
        total = 0
        if self.file.user.designation_abbreviation != 'assistant_prof_on_contract':
            for guidance in self.file.phd_guidance.filter(category='internal'):
                print(guidance.status)
                if guidance.marks.ro1_agreed:
                    if guidance.status == 'awarded':
                        total += self.file.configuration.section_2b_phd_guidance_awarded
                        guidance.marks.ro1 = self.file.configuration.section_2b_phd_guidance_awarded
                    elif guidance.status == 'synopsis':
                        total += self.file.configuration.section_2b_phd_guidance_synopsis_submitted
                        guidance.marks.ro1 = self.file.configuration.section_2b_phd_guidance_synopsis_submitted
                    elif guidance.status == 'ongoing':
                        total += self.file.configuration.section_2b_phd_guidance_under_progress
                        guidance.marks.ro1 = self.file.configuration.section_2b_phd_guidance_under_progress
                    elif guidance.status == 'other':
                        total += 0
                        guidance.marks.ro1 = 0
                guidance.marks.save()
        if self.file.external_phd_guidance_available:
            count = 0
            for guidance in self.file.phd_guidance.filter(category='external'):
                if guidance.marks.ro1_agreed and count <= 2:
                    count += 1
                    total += self.file.configuration.section_2b_phd_guidance_external
                    guidance.marks.ro1 = self.file.configuration.section_2b_phd_guidance_external
                guidance.marks.save()

        return round(total, 2)

    def calculateDissertationAll(self):
        return self.calculateMastersThesis()

    # def calculateBachelorsDissertation(self):
    #     total = 0
    #     count = 0
    #     for dissertation in self.file.bachelors_dissertation.all():
    #         if dissertation.marks.ro1_agreed and dissertation.is_awarded and count <= 10:
    #             count += 1
    #             total += self.file.configuration.section_2c_i_marks_per_dissertation_awarded
    #             dissertation.marks.ro1 = self.file.configuration.section_2c_i_marks_per_dissertation_awarded
    #         dissertation.marks.save()
    #     return round(total, 2)

    def calculateMastersThesis(self):
        total = 0
        count = 0
        for thesis in self.file.masters_thesis.all():
            if thesis.marks.ro1_agreed and count <= self.file.configuration.section_2c_ii_max_thesis:
                count += 1
                if thesis.status == 'submitted':
                    total += self.file.configuration.section_2c_ii_marks_per_thesis_submitted
                    thesis.marks.ro1 = self.file.configuration.section_2c_ii_marks_per_thesis_submitted
                elif thesis.status == 'submitted_with_ipr':
                    total += self.file.configuration.section_2c_ii_marks_per_thesis_submitted_with_ipr
                    thesis.marks.ro1 = self.file.configuration.section_2c_ii_marks_per_thesis_submitted_with_ipr
            else:
                thesis.marks.ro1 = 0
            thesis.marks.save()
        return round(total, 2)

    def calculateAwards(self):
        total = 0
        for award in self.file.recognition_awards.all():
            if award.marks.ro1_agreed:
                if award.award_type == 'international':
                    total += self.file.configuration.section_2d_international_level
                    award.marks.ro1 = self.file.configuration.section_2d_international_level
                elif award.award_type == 'national':
                    total += self.file.configuration.section_2d_national_level
                    award.marks.ro1 = self.file.configuration.section_2d_national_level
                elif award.award_type == 'state':
                    total += self.file.configuration.section_2d_state_level
                    award.marks.ro1 = self.file.configuration.section_2d_state_level
                elif award.award_type == 'university' or award.award_type == 'regional':
                    total += self.file.configuration.section_2d_regional_university_level
                    award.marks.ro1 = self.file.configuration.section_2d_regional_university_level
            else:
                award.marks.ro1 = 0
            award.marks.save()
        if total > self.file.configuration.section_2d_recognition_awards_received_max_marks:
            total = self.file.configuration.section_2d_recognition_awards_received_max_marks
        return round(total, 2)

    def calculateSectionE(self):
        if self.file.user.designation_abbreviation == 'assistant_prof_on_contract' and len(
                list(self.file.providing_consultancy.all())) == 0:
            return self.calculateIndustryCollaboration()
        else:
            return self.calculateConsultancy()

    def calculateConsultancy(self):
        total = 0
        for consultancy in self.file.providing_consultancy.all():
            if consultancy.marks.ro1_agreed:
                total += self.file.configuration.section_2e_providing_consultancy
                consultancy.marks.ro1 = self.file.configuration.section_2e_providing_consultancy
            else:
                consultancy.marks.ro1 = 0
            consultancy.marks.save()
        return round(total, 2)

    def calculateIndustryCollaboration(self):
        total = 0
        for industry_collaboration in self.file.industry_collaboration.all():
            if industry_collaboration.marks.ro1_agreed:
                total += self.file.configuration.section_2e_industry_collaboration_project
                industry_collaboration.marks.ro1 = self.file.configuration.section_2e_industry_collaboration_project
            else:
                industry_collaboration.marks.ro1 = 0
            industry_collaboration.marks.save()
        return round(total, 2)

    def calculateAcademiaCollaboration(self):
        if self.file.academia_collaboration_total is None:
            self.file.academia_collaboration_total = MarkField()
        self.file.academia_collaboration_total.ro1 = self.file.academia_collaboration.mou_marks.ro1 + self.file.academia_collaboration.contribution_marks.ro1
        self.file.academia_collaboration_total.save()
        self.file.save()
        return round(self.file.academia_collaboration_total.ro1, 2)

    def calculateSection3(self):
        return self.calculateArrangingConferences() + self.calculateMentoring()

    def calculateArrangingConferences(self):
        total = 0
        if self.file.arranging_conferences_total is None:
            self.file.arranging_conferences_total = MarkField()
        if self.file.arranging_conferences_available:
            total += self.file.arranging_conferences_total.ro1
        else:
            self.file.arranging_conferences_total.ro1 = 0
            total = 0
        self.file.arranging_conferences_total.save()
        self.file.save()
        return round(total, 2)

    def calculateMentoring(self):
        total = 0
        if self.file.being_mentor_total is None:
            self.file.being_mentor_total = MarkField()
        if self.file.being_mentor_available:
            total += self.file.being_mentor_total.ro1
        else:
            self.file.being_mentor_total.ro1 = 0
            total = 0
        self.file.being_mentor_total.save()
        self.file.save()
        return round(total, 2)

    def calculateSection4(self):
        return self.calculateAttendingConferences() + self.calculateCommunityDevelopment() + self.calculateExtraCurricular()

    def calculateAttendingConferences(self):
        total = 0
        for conference in self.file.attending_conferences.all():
            if conference.marks.ro1_agreed:
                total += self.file.configuration.section_4a_arranging_conferences_marks_per_conference
                conference.marks.ro1 = self.file.configuration.section_4a_arranging_conferences_marks_per_conference
            else:
                conference.marks.ro1 = 0

            conference.marks.save()
        return min(total, self.file.configuration.section_4a_arranging_conferences_max_marks)

    def calculateCommunityDevelopment(self):
        if self.file.community_development_total:
            return self.file.community_development_total.ro1
        else:
            return 0

    def calculateExtraCurricular(self):
        total = 0
        # if self.file.involvement_extra_curricular_marks is None:
        #     self.file.involvement_extra_curricular_marks = MarkField()
        # total += self.file.placement_duty_marks.ro1
        # total += self.file.admission_duty_marks.ro1
        total += self.file.involvement_extra_curricular_marks.ro1
        # self.file.involvement_extra_curricular_marks.ro1 = total
        # self.file.involvement_extra_curricular_marks.save()
        # self.file.save()
        return round(total, 2)

    def calculateAdditionalMarks(self):
        total = 0
        total += self.file.placement_duty_marks.ro1
        total += self.file.admission_duty_marks.ro1
        total += self.file.pgp_chair_marks.ro1
        total += self.file.e_mba_chair_marks.ro1
        if self.file.user.is_hod:
            total += 10
        return round(total, 2)

    def calculateMOOC(self):
        total = 0
        if self.file.is_mooc_available:
            if self.file.mooc_course.marks.ro1_agreed:
                total += self.file.configuration.self_development_mooc_course_marks
        return round(total, 2)

    def calculateAdditionalTotal(self):
        total = 0
        total += self.calculateAdditionalMarks()
        total += self.calculateMOOC()
        return round(total, 2)

    def calculatePartB(self):
        total = 0
        total += self.file.senior_feedback_marks.ro1
        total += self.file.self_development_total.ro1
        total += self.file.additional_responsibilities_marks.ro1
        print('Total: ', total)
        return round(total, 2)

    @staticmethod
    def getGradeName(self, grade):
        if grade == 'O':
            return 'Outstanding'
        elif grade == 'G':
            return 'Good'
        elif grade == 'A':
            return 'Average'
        elif grade == 'U':
            return 'Unsatisfactory'
        else:
            return 'N/A'


class CalculationEngineR2:
    """This class represents a calculation engine, which is a set of rules
    that can be used to calculate the value of an appraisal.
    """

    def __init__(self,
                 file: FOEMAssistantProfOnContractAppraisalFile | FOEMAssistantProfAppraisalFile | FOEMAssociateProfAppraisalFile | FOEMProfAppraisalFile):
        # self.is_on_contract = is_on_contract
        self.file = file

    def calculateGrandTotal(self):
        total = 0
        total += self.calculatePartA()
        total += self.calculatePartB()
        total += self.calculateAdditionalTotal()
        return round(total + 0.01, 0)

    def calculatePartA(self):
        total = 0
        total += self.calculateTeachingMaster()
        total += self.calculateSection2()
        total += self.calculateSection3()
        total += self.calculateSection4()

        return total

    def calculateTeachingMaster(self):
        total = 0
        total += self.calculateTeachingLoad()
        total += self.calculateStudentFeedback()
        total += self.calculateBooksAndPublications()
        total += self.calculateAcademicPractices()
        total += self.calculateExaminationDuty()
        return total

    def calculateTeachingLoad(self):
        tl_avg = (self.file.teaching_load.semester_odd + self.file.teaching_load.semester_even) / 2
        if tl_avg >= self.file.configuration.teaching_load_upper_limit:
            return round(
                self.file.configuration.teaching_load_upper_limit * self.file.configuration.teaching_load_t_coefficient,
                0)
        elif tl_avg <= self.file.configuration.teaching_load_lower_limit:
            return round(
                self.file.configuration.teaching_load_lower_limit * self.file.configuration.teaching_load_t_coefficient,
                0)
        else:
            return round(tl_avg * self.file.configuration.teaching_load_t_coefficient, 0)

    def calculateStudentFeedback(self):
        st_load = self.file.student_feedback
        if st_load <= self.file.configuration.students_feedback_lower_limit:
            return round(
                self.file.configuration.students_feedback_lower_limit * self.file.configuration.students_feedback_s_coefficient,
                0)
        else:
            return round(st_load * self.file.configuration.students_feedback_s_coefficient, 0)

    def calculateExaminationDuty(self):
        total = 0
        total += self.file.exam_duty.timely_invigilation
        total += self.file.exam_duty.paper_setting
        total += self.file.exam_duty.evaluation
        total += self.file.exam_duty.result_submission
        return total

    def calculateBooksAndPublications(self):
        # research based on books and publications
        total = 0
        _books = []  # new
        _chapters = []  # new
        for book in self.file.research_books.all():
            if book.marks.ro2_agreed:
                if book.type == 'book':
                    total += self.file.configuration.section_1e_i_per_book_per_author
                    book.marks.ro2 = self.file.configuration.section_1e_i_per_book_per_author
                    _books.append(self.file.configuration.section_1e_i_per_book_per_author)
                else:
                    total += self.file.configuration.section_1e_i_per_chapter
                    book.marks.ro2 = self.file.configuration.section_1e_i_per_chapter
                    _chapters.append(self.file.configuration.section_1e_i_per_chapter)
            else:
                book.marks.ro2 = 0
            book.marks.save()

        for book in self.file.literary_books.all():
            if book.marks.ro2_agreed:
                if book.type == 'book':
                    total += self.file.configuration.section_1e_ii_per_book_per_author
                    book.marks.ro2 = self.file.configuration.section_1e_ii_per_book_per_author
                    _books.append(self.file.configuration.section_1e_ii_per_book_per_author)
                else:
                    total += self.file.configuration.section_1e_ii_per_chapter
                    book.marks.ro2 = self.file.configuration.section_1e_ii_per_chapter
                    _chapters.append(self.file.configuration.section_1e_ii_per_chapter)
            else:
                book.marks.ro2 = 0
            book.marks.save()
        for book in self.file.textbooks.all():
            if book.marks.ro2_agreed:
                if book.type == 'book':
                    if book.publication_level == 'national':
                        total += self.file.configuration.section_1e_iii_per_national_book_per_author
                        book.marks.ro2 = self.file.configuration.section_1e_iii_per_national_book_per_author
                        _books.append(self.file.configuration.section_1e_iii_per_national_book_per_author)

                    elif book.publication_level == 'international':
                        total += self.file.configuration.section_1e_iii_per_international_book_per_author
                        book.marks.ro2 = self.file.configuration.section_1e_iii_per_international_book_per_author
                        _books.append(self.file.configuration.section_1e_iii_per_international_book_per_author)
                else:
                    total += self.file.configuration.section_1e_iii_per_chapter
                    book.marks.ro2 = self.file.configuration.section_1e_iii_per_chapter
                    _chapters.append(self.file.configuration.section_1e_iii_per_chapter)
            else:
                book.marks.ro2 = 0
            book.marks.save()
        _total = 0  # new
        _books.sort(reverse=True)  # new
        _chapters.sort(reverse=True)  # new
        if len(_books) > 0:  # new
            _total += _books[0]  # new
        if len(_chapters) > 0:  # new
            _total += _chapters[0]  # new
        if len(_chapters) > 1:  # new
            _total += _chapters[1]  # new
        return _total  # new

    def calculateAcademicPractices(self):
        return self.file.modern_teaching_methods.marks.ro2 + self.file.upkeep_of_course_files_marks.ro2 + self.file.inclusion_of_alumni_marks.ro2


    def calculateSection2(self):
        total = 0
        total += self.calculateResearchMaster()
        total += self.calculateProjects()
        if not self.file.user.designation_abbreviation == 'assistant_prof_on_contract':
            total += self.calculatePhDGuidance()
        total += self.calculateDissertationAll()
        total += self.calculateAwards()
        total += self.calculateSectionE()
        total += self.calculateAcademiaCollaboration()
        return total

    def calculateResearchMaster(self):
        total = 0
        total += self.calculatePapers()
        total += self.calculateConferences()
        total += self.calculateEPublications()
        return total

    def calculatePapers(self):
        total = 0
        main_author_cut = 0.7
        co_author_cut = 0.3
        for paper in self.file.publications_in_scopus_wos.all():
            if paper.marks.ro2_agreed:
                if paper.is_main_author:
                    if paper.category == 'scopus':
                        if paper.quality == 'q1':
                            total += self.file.configuration.section_2a_a_i_per_scopus_q1 * main_author_cut
                            paper.marks.ro2 = self.file.configuration.section_2a_a_i_per_scopus_q1 * main_author_cut
                        elif paper.quality == 'q2':
                            total += self.file.configuration.section_2a_a_i_per_scopus_q2 * main_author_cut
                            paper.marks.ro2 = self.file.configuration.section_2a_a_i_per_scopus_q2 * main_author_cut
                        elif paper.quality == 'q3':
                            total += self.file.configuration.section_2a_a_i_per_scopus_q3 * main_author_cut
                            paper.marks.ro2 = self.file.configuration.section_2a_a_i_per_scopus_q3 * main_author_cut
                        elif paper.quality == 'q4':
                            total += self.file.configuration.section_2a_a_i_per_scopus_q4 * main_author_cut
                            paper.marks.ro2 = self.file.configuration.section_2a_a_i_per_scopus_q4 * main_author_cut
                    elif paper.category == 'wos':
                        total += self.file.configuration.section_2a_a_i_per_wos * main_author_cut
                        paper.marks.ro2 = self.file.configuration.section_2a_a_i_per_wos * main_author_cut
                    elif paper.category == 'ugc' or paper.category == 'sci' or paper.category == 'abdc':
                        total += self.file.configuration.section_2a_a_ii_per_publication * main_author_cut
                        paper.marks.ro2 = self.file.configuration.section_2a_a_ii_per_publication * main_author_cut
                else:
                    if paper.category == 'scopus':
                        if paper.quality == 'q1':
                            total += (
                                    self.file.configuration.section_2a_a_i_per_scopus_q1 * co_author_cut)  # / paper.co_author_count
                            paper.marks.ro2 = (
                                    self.file.configuration.section_2a_a_i_per_scopus_q1 * co_author_cut)  # / paper.co_author_count
                        elif paper.quality == 'q2':
                            total += (
                                    self.file.configuration.section_2a_a_i_per_scopus_q2 * co_author_cut)  # / paper.co_author_count
                            paper.marks.ro2 = (
                                    self.file.configuration.section_2a_a_i_per_scopus_q2 * co_author_cut)  # / paper.co_author_count
                        elif paper.quality == 'q3':
                            total += (
                                    self.file.configuration.section_2a_a_i_per_scopus_q3 * co_author_cut)  # / paper.co_author_count
                            paper.marks.ro2 = (
                                    self.file.configuration.section_2a_a_i_per_scopus_q3 * co_author_cut)  # / paper.co_author_count
                        elif paper.quality == 'q4':
                            total += (
                                    self.file.configuration.section_2a_a_i_per_scopus_q4 * co_author_cut)  # / paper.co_author_count
                            paper.marks.ro2 = (
                                    self.file.configuration.section_2a_a_i_per_scopus_q4 * co_author_cut)  # / paper.co_author_count
                    elif paper.category == 'wos':
                        total += (
                                self.file.configuration.section_2a_a_i_per_wos * co_author_cut)  # / paper.co_author_count
                        paper.marks.ro2 = (
                                self.file.configuration.section_2a_a_i_per_wos * co_author_cut)  # / paper.co_author_count
                    elif paper.category == 'ugc' or paper.category == 'sci' or paper.category == 'abdc':
                        total += self.file.configuration.section_2a_a_ii_per_publication * co_author_cut
                        paper.marks.ro2 = self.file.configuration.section_2a_a_ii_per_publication * co_author_cut
            else:
                paper.marks.ro2 = 0
            paper.marks.save()
        return round(total, 2)

    # def calculatePapersSciUGC(self):
    #     total = 0
    #     main_author_cut = 0.7
    #     co_author_cut = 0.3
    #
    #     for paper in self.file.publications_in_sci_ugc.all():
    #         if paper.marks.ro2_agreed:
    #             if paper.is_main_author:
    #                 total += self.file.configuration.section_2a_a_ii_per_publication * main_author_cut
    #                 paper.marks.ro2 = self.file.configuration.section_2a_a_ii_per_publication * main_author_cut
    #             else:
    #                 total += self.file.configuration.section_2a_a_ii_per_publication * co_author_cut
    #                 paper.marks.ro2 = self.file.configuration.section_2a_a_ii_per_publication * co_author_cut
    #         else:
    #             paper.marks.ro2 = 0
    #         paper.marks.save()
    #     return round(total, 2)

    def calculateConferences(self):
        total = 0
        main_author_cut = 0.7
        co_author_cut = 0.3
        for paper in self.file.conference_proceedings_scopus_wos.all():
            if paper.marks.ro2_agreed:
                if paper.is_main_author:
                    total += self.file.configuration.section_2a_a_ii_per_conference * main_author_cut
                    paper.marks.ro2 = self.file.configuration.section_2a_a_ii_per_conference * main_author_cut
                else:
                    total += self.file.configuration.section_2a_a_ii_per_conference * co_author_cut
                    paper.marks.ro2 = self.file.configuration.section_2a_a_ii_per_conference * co_author_cut
                # if paper.is_main_author:
                #     if paper.category == 'scopus':
                #         if paper.quality == 'q1':
                #             total += self.file.configuration.section_2a_a_ii_per_scopus_q1 * main_author_cut
                #             paper.marks.ro2 = self.file.configuration.section_2a_a_ii_per_scopus_q1 * main_author_cut
                #         elif paper.quality == 'q2':
                #             total += self.file.configuration.section_2a_a_ii_per_scopus_q2 * main_author_cut
                #             paper.marks.ro2 = self.file.configuration.section_2a_a_ii_per_scopus_q2 * main_author_cut
                #         elif paper.quality == 'q3':
                #             total += self.file.configuration.section_2a_a_ii_per_scopus_q3 * main_author_cut
                #             paper.marks.ro2 = self.file.configuration.section_2a_a_ii_per_scopus_q3 * main_author_cut
                #         elif paper.quality == 'q4':
                #             total += self.file.configuration.section_2a_a_ii_per_scopus_q4 * main_author_cut
                #             paper.marks.ro2 = self.file.configuration.section_2a_a_ii_per_scopus_q4 * main_author_cut
                #     elif paper.category == 'wos':
                #         total += self.file.configuration.section_2a_a_i_per_wos * main_author_cut
                #         paper.marks.ro2 = self.file.configuration.section_2a_a_i_per_wos * main_author_cut
                # else:
                #     if paper.category == 'scopus':
                #         if paper.quality == 'q1':
                #             total += (self.file.configuration.section_2a_a_ii_per_scopus_q1 * co_author_cut)  # / paper.co_author_count
                #             paper.marks.ro2 = (self.file.configuration.section_2a_a_ii_per_scopus_q1 * co_author_cut)  # / paper.co_author_count
                #         elif paper.quality == 'q2':
                #             total += (self.file.configuration.section_2a_a_ii_per_scopus_q2 * co_author_cut)  # / paper.co_author_count
                #             paper.marks.ro2 = (self.file.configuration.section_2a_a_ii_per_scopus_q2 * co_author_cut)  # / paper.co_author_count
                #         elif paper.quality == 'q3':
                #             total += (self.file.configuration.section_2a_a_ii_per_scopus_q3 * co_author_cut)  # / paper.co_author_count
                #             paper.marks.ro2 = (self.file.configuration.section_2a_a_ii_per_scopus_q3 * co_author_cut)  # / paper.co_author_count
                #         elif paper.quality == 'q4':
                #             total += (self.file.configuration.section_2a_a_ii_per_scopus_q4 * co_author_cut)  # / paper.co_author_count
                #             paper.marks.ro2 = (self.file.configuration.section_2a_a_ii_per_scopus_q4 * co_author_cut)  # / paper.co_author_count
                #     elif paper.category == 'wos':
                #         total += (self.file.configuration.section_2a_a_ii_per_wos * co_author_cut)  # / paper.co_author_count
                #         paper.marks.ro2 = (self.file.configuration.section_2a_a_ii_per_wos * co_author_cut)  # / paper.co_author_count
            else:
                paper.marks.ro2 = 0
            paper.marks.save()
        return round(total, 2)

    def calculateEPublications(self):
        count = 0
        total = 0
        for pub in self.file.e_publications_articles.all():
            if count >= 2:
                break
            if pub.marks.ro2_agreed:
                count += 1
                total += self.file.configuration.section_2a_b_per_e_publication
                pub.marks.ro2 = self.file.configuration.section_2a_b_per_e_publication
            else:
                pub.marks.ro2 = 0
            pub.marks.save()
        return round(total, 2)

    def calculateProjects(self):
        total = 0
        osrp_count = 0
        for project in self.file.projects.all():
            if project.marks.ro2_agreed:
                if project.project_category == 'INS':
                    project.marks.ro2 = project.marks.ro1
                    project.save()
                    total += project.marks.ro2
                elif project.project_category == 'OSRP' and self.file.user.designation_abbreviation == 'assistant_prof_on_contract':
                    if osrp_count > 0:
                        continue
                    osrp_count += 1
                    total += self.file.configuration.section_2a_c_category_osrp_student_research_project
                    project.marks.ro2 = self.file.configuration.section_2a_c_category_osrp_student_research_project
                elif project.project_participation == 'pi':
                    if project.project_category == 'MAJOR':
                        total += self.file.configuration.section_2a_c_category_major_per_pi
                        project.marks.ro2 = self.file.configuration.section_2a_c_category_major_per_pi
                    elif project.project_category == 'MEDIUM':
                        total += self.file.configuration.section_2a_c_category_medium_per_pi
                        project.marks.ro2 = self.file.configuration.section_2a_c_category_medium_per_pi
                    elif project.project_category == 'MINOR':
                        total += self.file.configuration.section_2a_c_category_minor_per_pi
                        project.marks.ro2 = self.file.configuration.section_2a_c_category_minor_per_pi
                elif project.project_participation == 'copi':
                    if project.project_category == 'MAJOR':
                        total += self.file.configuration.section_2a_c_category_major_per_co_pi
                        project.marks.ro2 = self.file.configuration.section_2a_c_category_major_per_co_pi
                    elif project.project_category == 'MEDIUM':
                        total += self.file.configuration.section_2a_c_category_medium_per_co_pi
                        project.marks.ro2 = self.file.configuration.section_2a_c_category_medium_per_co_pi
                    elif project.project_category == 'MINOR':
                        total += self.file.configuration.section_2a_c_category_minor_per_co_pi
                        project.marks.ro2 = self.file.configuration.section_2a_c_category_minor_per_co_pi

            project.marks.save()
        return round(total, 2)

    def calculatePhDGuidance(self):
        total = 0
        if self.file.user.designation_abbreviation != 'assistant_prof_on_contract':
            for guidance in self.file.phd_guidance.filter(category='internal'):
                print(guidance.status)
                if guidance.marks.ro2_agreed:
                    if guidance.status == 'awarded':
                        total += self.file.configuration.section_2b_phd_guidance_awarded
                        guidance.marks.ro2 = self.file.configuration.section_2b_phd_guidance_awarded
                    elif guidance.status == 'synopsis':
                        total += self.file.configuration.section_2b_phd_guidance_synopsis_submitted
                        guidance.marks.ro2 = self.file.configuration.section_2b_phd_guidance_synopsis_submitted
                    elif guidance.status == 'ongoing':
                        total += self.file.configuration.section_2b_phd_guidance_under_progress
                        guidance.marks.ro2 = self.file.configuration.section_2b_phd_guidance_under_progress
                    elif guidance.status == 'other':
                        total += 0
                        guidance.marks.ro2 = 0
                guidance.marks.save()
        if self.file.external_phd_guidance_available:
            count = 0
            for guidance in self.file.phd_guidance.filter(category='external'):
                if guidance.marks.ro2_agreed and count <= 2:
                    count += 1
                    total += self.file.configuration.section_2b_phd_guidance_external
                    guidance.marks.ro2 = self.file.configuration.section_2b_phd_guidance_external
                guidance.marks.save()

        return round(total, 2)

    def calculateDissertationAll(self):
        return self.calculateMastersThesis()

    # def calculateBachelorsDissertation(self):
    #     total = 0
    #     count = 0
    #     for dissertation in self.file.bachelors_dissertation.all():
    #         if dissertation.marks.ro2_agreed and dissertation.is_awarded and count <= 10:
    #             count += 1
    #             total += self.file.configuration.section_2c_i_marks_per_dissertation_awarded
    #             dissertation.marks.ro2 = self.file.configuration.section_2c_i_marks_per_dissertation_awarded
    #         dissertation.marks.save()
    #     return round(total, 2)

    def calculateMastersThesis(self):
        total = 0
        count = 0
        for thesis in self.file.masters_thesis.all():
            if thesis.marks.ro2_agreed and count <= self.file.configuration.section_2c_ii_max_thesis:
                count += 1
                if thesis.status == 'submitted':
                    total += self.file.configuration.section_2c_ii_marks_per_thesis_submitted
                    thesis.marks.ro2 = self.file.configuration.section_2c_ii_marks_per_thesis_submitted
                elif thesis.status == 'submitted_with_ipr':
                    total += self.file.configuration.section_2c_ii_marks_per_thesis_submitted_with_ipr
                    thesis.marks.ro2 = self.file.configuration.section_2c_ii_marks_per_thesis_submitted_with_ipr
            else:
                thesis.marks.ro2 = 0
            thesis.marks.save()
        return round(total, 2)

    def calculateAwards(self):
        total = 0
        for award in self.file.recognition_awards.all():
            if award.marks.ro2_agreed:
                if award.award_type == 'international':
                    total += self.file.configuration.section_2d_international_level
                    award.marks.ro2 = self.file.configuration.section_2d_international_level
                elif award.award_type == 'national':
                    total += self.file.configuration.section_2d_national_level
                    award.marks.ro2 = self.file.configuration.section_2d_national_level
                elif award.award_type == 'state':
                    total += self.file.configuration.section_2d_state_level
                    award.marks.ro2 = self.file.configuration.section_2d_state_level
                elif award.award_type == 'university' or award.award_type == 'regional':
                    total += self.file.configuration.section_2d_regional_university_level
                    award.marks.ro2 = self.file.configuration.section_2d_regional_university_level
            else:
                award.marks.ro2 = 0
            award.marks.save()
        if total > self.file.configuration.section_2d_recognition_awards_received_max_marks:
            total = self.file.configuration.section_2d_recognition_awards_received_max_marks
        return round(total, 2)

    def calculateSectionE(self):
        if self.file.user.designation_abbreviation == 'assistant_prof_on_contract' and len(
                list(self.file.providing_consultancy.all())) == 0:
            return self.calculateIndustryCollaboration()
        else:
            return self.calculateConsultancy()

    def calculateConsultancy(self):
        total = 0
        for consultancy in self.file.providing_consultancy.all():
            if consultancy.marks.ro2_agreed:
                total += self.file.configuration.section_2e_providing_consultancy
                consultancy.marks.ro2 = self.file.configuration.section_2e_providing_consultancy
            else:
                consultancy.marks.ro2 = 0
            consultancy.marks.save()
        return round(total, 2)

    def calculateIndustryCollaboration(self):
        total = 0
        for industry_collaboration in self.file.industry_collaboration.all():
            if industry_collaboration.marks.ro2_agreed:
                total += self.file.configuration.section_2e_industry_collaboration_project
                industry_collaboration.marks.ro2 = self.file.configuration.section_2e_industry_collaboration_project
            else:
                industry_collaboration.marks.ro2 = 0
            industry_collaboration.marks.save()
        return round(total, 2)

    def calculateAcademiaCollaboration(self):
        if self.file.academia_collaboration_total is None:
            self.file.academia_collaboration_total = MarkField()
        self.file.academia_collaboration_total.ro2 = self.file.academia_collaboration.mou_marks.ro2 + self.file.academia_collaboration.contribution_marks.ro2
        self.file.academia_collaboration_total.save()
        self.file.save()
        return round(self.file.academia_collaboration_total.ro2, 2)

    def calculateSection3(self):
        return self.calculateArrangingConferences() + self.calculateMentoring()

    def calculateArrangingConferences(self):
        total = 0
        if self.file.arranging_conferences_total is None:
            self.file.arranging_conferences_total = MarkField()
        if self.file.arranging_conferences_available:
            total += self.file.arranging_conferences_total.ro2
        else:
            self.file.arranging_conferences_total.ro2 = 0
            total = 0
        self.file.arranging_conferences_total.save()
        self.file.save()
        return round(total, 2)

    def calculateMentoring(self):
        total = 0
        if self.file.being_mentor_total is None:
            self.file.being_mentor_total = MarkField()
        if self.file.being_mentor_available:
            total += self.file.being_mentor_total.ro2
        else:
            self.file.being_mentor_total.ro2 = 0
            total = 0
        self.file.being_mentor_total.save()
        self.file.save()
        return round(total, 2)

    def calculateSection4(self):
        return self.calculateAttendingConferences() + self.calculateCommunityDevelopment() + self.calculateExtraCurricular()

    def calculateAttendingConferences(self):
        total = 0
        for conference in self.file.attending_conferences.all():
            if conference.marks.ro2_agreed:
                total += self.file.configuration.section_4a_arranging_conferences_marks_per_conference
                conference.marks.ro2 = self.file.configuration.section_4a_arranging_conferences_marks_per_conference
            else:
                conference.marks.ro2 = 0

            conference.marks.save()
        return min(total, self.file.configuration.section_4a_arranging_conferences_max_marks)

    def calculateCommunityDevelopment(self):
        if self.file.community_development_total:
            return self.file.community_development_total.ro2
        else:
            return 0

    def calculateExtraCurricular(self):
        total = 0
        # if self.file.involvement_extra_curricular_marks is None:
        #     self.file.involvement_extra_curricular_marks = MarkField()
        # total += self.file.placement_duty_marks.ro2
        # total += self.file.admission_duty_marks.ro2
        total += self.file.involvement_extra_curricular_marks.ro2
        # self.file.involvement_extra_curricular_marks.ro2 = total
        # self.file.involvement_extra_curricular_marks.save()
        # self.file.save()
        return round(total, 2)

    def calculateAdditionalMarks(self):
        total = 0
        total += self.file.placement_duty_marks.ro1
        total += self.file.admission_duty_marks.ro1
        total += self.file.pgp_chair_marks.ro1
        total += self.file.e_mba_chair_marks.ro1
        if self.file.user.is_hod:
            total += 10
        return round(total, 2)

    def calculateMOOC(self):
        total = 0
        if self.file.is_mooc_available:
            if self.file.mooc_course.marks.ro2_agreed:
                total += self.file.configuration.self_development_mooc_course_marks
        return round(total, 2)

    def calculateAdditionalTotal(self):
        total = 0
        total += self.calculateAdditionalMarks()
        total += self.calculateMOOC()
        return round(total, 2)

    def calculatePartB(self):
        total = 0
        total += self.file.senior_feedback_marks.ro2
        total += self.file.self_development_total.ro2
        total += self.file.additional_responsibilities_marks.ro2

        return round(total, 2)

    @staticmethod
    def getGradeName(self, grade):
        if grade == 'O':
            return 'Outstanding'
        elif grade == 'G':
            return 'Good'
        elif grade == 'A':
            return 'Average'
        elif grade == 'U':
            return 'Unsatisfactory'
        else:
            return 'N/A'

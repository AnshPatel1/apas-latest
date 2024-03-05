from django.db import models


class FOEMGoalSheetAssociateProf(models.Model):
    """This is the FoEM Goalsheet model. It contains the fields for the FoEM Goalsheet form."""
    # Configurations
    year = models.IntegerField()
    is_active = models.BooleanField(default=False)

    grand_total = models.IntegerField(default=360)

    # ||||||||||||||||||||||   PART A   ||||||||||||||||||||||
    # TOTAL FOR PART A (SECTION 1 TO 4) SHOULD BE 307
    part_a_total = models.IntegerField(default=315)

    # ======================   Section 1: Teaching (TCS iON)   ======================
    # Configurations for Section 1
    section_1_minimum_marks = models.IntegerField(default=75)
    section_1_maximum_marks = models.IntegerField(default=105)

    # Section 1.A: Teaching Load
    # If teaching load is >=14 then 42 marks
    # If teaching load is from 6 to 15 (inclusive) then marks = (no of hours) * 2.6
    # If teaching load is from 1 to 5 (inclusive) then marks = 13

    teaching_load_upper_limit = models.IntegerField(default=14)
    teaching_load_lower_limit = models.IntegerField(default=4)
    teaching_load_t_coefficient = models.FloatField(default=2.6)
    teaching_load_minimum_marks = models.IntegerField(default=13)

    # ------- Section 1.B: Students Feedback (TCS iON) -------

    students_feedback_s_coefficient = models.FloatField(default=3)
    students_feedback_lower_limit = models.IntegerField(default=3)

    # ------- Section 1.C: Academic Practices (RO/ RV) -------
    modern_methods_of_teaching_max_marks = models.IntegerField(default=10)
    upkeep_of_course_files_max_marks = models.IntegerField(default=3)
    inclusion_of_alumni_max_marks = models.IntegerField(default=5)

    # ------- Section 1.D (Exam Cell) -------
    section_1d_max_marks = models.IntegerField(default=30)
    #   Section 1.D(a): Teaching Innovation
    timely_invigilation = models.IntegerField(default=7)
    #   Section 1.D(b): Paper Setting
    paper_setting = models.IntegerField(default=8)
    #   Section 1.D(c): Teaching Innovation
    evaluation = models.IntegerField(default=8)
    #   Section 1.D(d): Teaching Innovation
    result_submission = models.IntegerField(default=7)

    # ------- Section 1.E: Books and Publications (RIMS / Dean Office) -------
    #  Section 1.E(i): Research based books or monographs
    #      20 marks to be given per book
    #      5 marks to be given per chapter in an edited book
    section_1e_i_per_book_per_author = models.IntegerField(default=20)
    section_1e_i_per_chapter = models.IntegerField(default=5)

    #  Section 1.E(ii): Literary published by International /National Publishers with an established peer review system with ISBN/ISSNs
    section_1e_ii_per_book_per_author = models.IntegerField(default=15)
    section_1e_ii_per_chapter = models.IntegerField(default=3)

    #  Section 1.E(iii): Textbooks published by International /National Publishers with an established peer review system with ISBN/ISSNs
    #      20 marks to be given per international book per author
    #      15 marks to be given per national book per author
    #      5 marks to be given per chapter in an edited book

    section_1e_iii_per_international_book_per_author = models.IntegerField(default=20)
    section_1e_iii_per_national_book_per_author = models.IntegerField(default=15)
    section_1e_iii_per_chapter = models.IntegerField(default=5)

    # ======================   Section 2: Research And Publications/Patents   ======================
    # Section 2 Configurations:
    section_2_subtotal = models.IntegerField(default=165)
    # ------- Section 2.A: Research Publications (RIMS / Dean Office) -------
    # Section 2.A Configurations:
    section_2a_subtotal = models.IntegerField(default=45)

    # Section 2.A.a(i): Publication in Scopus journals / Web of Science journals (Minimum 1 required)
    #     25 marks to be given for scopus indexed journals in Q1
    #     20 marks to be given for scopus indexed journals in Q2
    #     15 marks to be given for scopus indexed journals in Q3
    #     10 marks to be given for scopus indexed journals in Q4
    #     20 marks to be given for Web of Science indexed journals

    section_2a_a_i_per_scopus_q1 = models.IntegerField(default=25)
    section_2a_a_i_per_scopus_q2 = models.IntegerField(default=25)
    section_2a_a_i_per_scopus_q3 = models.IntegerField(default=15)
    section_2a_a_i_per_scopus_q4 = models.IntegerField(default=15)
    section_2a_a_i_per_wos = models.IntegerField(default=25)

    # Section 2.A.a(ii): Publication in Science Citation Index (SCI) journals with a citescore by reputed publishers like Springer,
    # Wiley, Elsevier, Taylor and Francis etc. and UGC Care List of Journals
    section_2a_a_ii_per_publication = models.IntegerField(default=15)

    # Section 2.A.a(iii): Conference Proceedings as full papers (Abstracts not to be included)
    #     5 marks to be given for each conference

    section_2a_a_ii_per_conference = models.IntegerField(default=5)

    # -------------- Section 2.A.b: E- publications/ articles --------------
    #     5 marks to be given for per e-publications/articles
    #     maximum of 2 publications/articles per year (10 mark cap)

    section_2a_b_per_e_publication = models.IntegerField(default=5)
    section_2a_b_max_marks = models.IntegerField(default=10)

    # -------------- Section 2.A.c: Projects --------------
    #     8 Categories of Projects A to H & Institutional Projects

    #       Category Major:  (fund of Rs. 10 lakhs and above)
    #           20 marks to be given if appraisee is the PI
    #           5 marks to be given if appraisee is the Co-PI
    section_2a_c_category_major_per_pi = models.IntegerField(default=20)
    section_2a_c_category_major_per_co_pi = models.IntegerField(default=15)

    #       Category Medium:  (above 5 lakhs)
    #           15 marks to be given if appraisee is the PI
    #           3 marks to be given if appraisee is the Co-PI
    section_2a_c_category_medium_per_pi = models.IntegerField(default=15)
    section_2a_c_category_medium_per_co_pi = models.IntegerField(default=10)

    #       Category Minor:  (above 50 lakhs)
    #           10 marks to be given if appraisee is the PI
    #           2 marks to be given if appraisee is the Co-PI
    section_2a_c_category_minor_per_pi = models.IntegerField(default=7)
    section_2a_c_category_minor_per_co_pi = models.IntegerField(default=4)

    #       Category Institutional Projects:  20 marks to be given
    section_2a_c_category_institutional_projects = models.IntegerField(default=20)

    # Only for Assistant Professors(On Contract)
    # 7 marks flat for any project of OSRP Student Research Project maximum of 1 per year (7 mark cap)
    section_2a_c_category_osrp_student_research_project = models.IntegerField(default=7)

    # -------------- Section 2.B: PhD Guidance as per current year --------------
    # 0 marks to be awarded for PhD guidance awarded
    # 0 marks to be awarded for PhD guidance Synopsis Submitted
    # 0 marks to be awarded for PhD guidance Under Progress
    section_2b_phd_guidance_awarded = models.IntegerField(default=20)
    section_2b_phd_guidance_synopsis_submitted = models.IntegerField(default=10)
    section_2b_phd_guidance_under_progress = models.IntegerField(default=5)

    section_2b_phd_guidance_external = models.IntegerField(default=5)
    section_2b_phd_guidance_external_max = models.IntegerField(default=2)

    # -------------- Section 2.C: Dissertation/Thesis --------------
    # -> Not Applicable for This Institute
    # # Section 2.C.i: Bachelors Dissertation/Project
    # #     2 marks to be given per Bachelors Dissertation/Project
    # #     maximum of 10 Bachelors Dissertation/Project per year (20 mark cap)
    # section_2c_i_marks_per_dissertation_awarded = models.IntegerField(default=2)
    # section_2c_i_max_dissertation = models.IntegerField(default=15)

    # Section 2.C.ii: Masters' Thesis (Capped at 2 thesis per year)
    #     6 marks to be given if thesis is Submitted
    #     8 marks to be given if thesis is Submitted and Patent granted/published
    #     10 marks to be given if thesis is Submitted, Papers published, and Patent granted/published
    section_2c_ii_marks_per_thesis_submitted = models.IntegerField(default=6)
    section_2c_ii_marks_per_thesis_submitted_with_ipr = models.IntegerField(default=12)
    section_2c_ii_max_thesis = models.IntegerField(default=10)

    # # -------------- Section 2.D: Patents/Inventions leading to patents - (Having OR Option) --------------
    # #     50 marks to be given for patent granted & licensed
    # #     25 marks to be given for patent granted
    # #     15 marks to be given for patent published
    # #     5 marks to be given for patent filed
    # section_2d_patent_granted_and_licensed = models.IntegerField(default=50)
    # section_2d_patent_granted = models.IntegerField(default=25)
    # section_2d_patent_published = models.IntegerField(default=15)
    # section_2d_patent_filed = models.IntegerField(default=5)
    #
    # # -------------- OR (Only for Assistant Professors(On Contract)) --------------
    # #     Faculty advisor to Student(s) representing PDEU for various industrial/technical/ societal competitive events.
    # #     maximum of 25 marks to be given by RO/RV
    # section_2d_faculty_advisor_to_student = models.IntegerField(default=25)

    # -------------- Section 2.D: Recognition/Awards received --------------
    #     To be awarded by RO/RV. Capped at 10 marks
    section_2d_recognition_awards_received_max_marks = models.IntegerField(default=10)
    #     10 marks to be given per International Level
    #     7 marks to be given per National Level
    #     5 marks to be given per State Level
    #     2 marks to be given per Regional/University Level
    section_2d_international_level = models.IntegerField(default=10)
    section_2d_national_level = models.IntegerField(default=7)
    section_2d_state_level = models.IntegerField(default=5)
    section_2d_regional_university_level = models.IntegerField(default=2)

    # -------------- Section 2.E: Providing Consultancy/ Organizing MDPs , EDPs as Chief Coordinator/ Program Head services on the behalf of University --------------
    #     10 marks to be given for Amount earned of max Rs. 2 lacs (Engg)(NET)
    #     Contains OR Option only for Assistant Professors(On Contract)
    section_2e_providing_consultancy = models.IntegerField(default=10)

    # -------------- OR (Only for Assistant Professors(On Contract)) --------------
    #     Industry Collaboration (Academia-Industry Connect) Project in
    #     collaboration with Industry Conducting a Workshop/Seminar in collaboration with Industry
    #         10 marks to be given for Amount earned of max Rs. 2 lacs (Engg)
    section_2e_industry_collaboration_project = models.IntegerField(default=0)

    # -------------- Section 2.F: Academia Collaboration (University/ Societies/ Research Organization) --------------
    #     Capped at 25 marks for both activities done
    section_2f_academia_collaboration_max_marks = models.IntegerField(default=20)
    #     5 marks to be given for MoU signed
    #     20 marks to be given for faculty contribution
    section_2f_mou_signed = models.IntegerField(default=5)
    section_2f_faculty_contribution = models.IntegerField(default=15)

    # =============== Section 3: Administrative Activities ===============
    # Marks to be awarded by RO/RV
    # Section 3 Configurations:
    section_3_subtotal = models.IntegerField(default=58)

    # # ------- Section 3.A: Successful conversion of International Admission (SLS)/ Local Placements -------
    # section_3a_international_admission = models.IntegerField(default=21)

    # ------- Section 3.B: Arranging Conferences/ Seminars/Conclaves -------
    #     Max 15 marks to be given by RO/RV
    section_3b_arranging_conferences_max_marks = models.IntegerField(default=20)

    # ------- Section 3.C: Being Mentor to students(providing Career/Academic counselling) -------
    #     Max 25 marks to be given by RO/RV
    section_3c_mentor_to_students_max_marks = models.IntegerField(default=5)

    # =============== Section 4: Extended Activities ===============
    # Marks to be awarded by RO/RV
    # Section 4 Configurations:

    # ------- Section 4.A: Arranging Conferences/ Seminars -------
    # As  session chair/ symposium chair/Keynote/Special Invitee. With permission of the Director, without utilising University Funds
    # 10 marks to be given awarded per conference/seminar
    # Capped at 20 marks per year
    section_4a_arranging_conferences_max_marks = models.IntegerField(default=20)
    section_4a_arranging_conferences_marks_per_conference = models.IntegerField(default=10)

    # ------- Section 4.B: Community Development Initiatives -------
    #     Max 10 marks to be given by RO/RV
    section_4b_community_development_initiatives_max_marks = models.IntegerField(default=10)

    # ------- Section 4.C: Involvement in Extra curricular/ Co- curricular activities -------
    #     Max 10 marks to be given OSAIL
    section_4c_involvement_in_extra_curricular_activities_max_marks = models.IntegerField(default=10)

    # ||||||||||||||||||||||  PART B ||||||||||||||||||||||
    # Total for Part B = 40 marks
    part_b_total = models.IntegerField(default=40)
    # =============== Section 1: Senior Feedback ===============
    # Marks to be awarded by RO/RV
    # Outstanding: 15 marks
    # Good: 12 marks
    # Average: 7 marks
    # Unsatisfactory: 3 marks
    senior_feedback_outstanding_marks = models.IntegerField(default=15)
    senior_feedback_good_marks = models.IntegerField(default=12)
    senior_feedback_average_marks = models.IntegerField(default=7)
    senior_feedback_unsatisfactory_marks = models.IntegerField(default=3)

    # =============== Section 2: Self Development ===============
    # Marks to be awarded by RO/RV
    # Outstanding: 10 marks
    # Good: 7 marks
    # Average: 5 marks
    # Unsatisfactory: 3 marks
    self_development_outstanding_marks = models.IntegerField(default=10)
    self_development_good_marks = models.IntegerField(default=7)
    self_development_average_marks = models.IntegerField(default=5)
    self_development_unsatisfactory_marks = models.IntegerField(default=3)
    # If Undertaken relevant MOOC course approved by AICTE/MHRD, received a certificate, Under CPDA : 15 marks to be awarded
    # Over and above the marks awarded in Section 2
    self_development_mooc_course_marks = models.IntegerField(default=15)

    # =============== Section 3: Ability to take and successfully execute additional responsibilities ===============
    # Marks to be awarded by RO/RV
    # Outstanding: 15 marks
    # Good: 12 marks
    # Average: 7 marks
    # Unsatisfactory: 3 marks
    additional_responsibilities_outstanding_marks = models.IntegerField(default=20)
    additional_responsibilities_good_marks = models.IntegerField(default=14)
    additional_responsibilities_average_marks = models.IntegerField(default=10)
    additional_responsibilities_unsatisfactory_marks = models.IntegerField(default=6)

    def __str__(self):
        if self.is_active:
            return f"FoEM Associate Professor Goalsheet for {self.year} (Active)"
        else:
            return f"FoEM Associate Professor Goalsheet for {self.year}"

    class Meta:
        verbose_name = "Goalsheet Configuration for FoEM Associate Professor"
        verbose_name_plural = "Goalsheet Configurations for FoEM Associate Professor"

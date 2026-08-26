from models import Enrollment, Student, Course

def _validate_normalize_enrollment_args(enrollments, student, course, semester):
    if not isinstance(enrollments, list):
        raise TypeError("enrollments need to be an Enrollment list")
    if not isinstance(student, Student):
        raise TypeError("student needs to be a Student type")
    if not isinstance(course, Course):
        raise TypeError("course needs to be a Course type")
    semester = Enrollment.semester_check(semester)
    for enrollment in enrollments:
        if not isinstance(enrollment,Enrollment):
            raise TypeError("Need an Enrollment list")
    return semester

def enroll_student(enrollments, student, course, semester):
    semester = _validate_normalize_enrollment_args(enrollments,student,course,semester)
    count = 0
    current_enrollment = None
    for enrollment in enrollments:
        if(
            student.sid == enrollment.sid
            and course.course_id == enrollment.course_id
            and semester == enrollment.semester
        ):
            if enrollment.status == "Enrolled":
                raise ValueError("Already enrolled")

            if enrollment.status == "Completed":
                raise ValueError("Course already completed")

            if enrollment.status == "Dropped":
                current_enrollment = enrollment
        if (
            enrollment.course_id == course.course_id
            and enrollment.semester == semester
            and enrollment.status == "Enrolled"
        ):
            count += 1
    if course.capacity <= count:
        raise ValueError("Course is full")
    if current_enrollment is not None:
        current_enrollment.status = "Enrolled"
        return True
    new_enroll = Enrollment(student,course,semester)
    enrollments.append(new_enroll)
    return True
        
def drop_course(enrollments, student, course, semester):
    semester = _validate_normalize_enrollment_args(enrollments,student,course,semester)
    for enrollment in enrollments:
        if(
            enrollment.sid == student.sid
            and enrollment.course_id == course.course_id
            and enrollment.semester == semester
        ):
            if enrollment.status == 'Completed':
                raise ValueError("Cannot drop a completed course")
            elif enrollment.status == 'Dropped':
                return False
            else:
                enrollment.status = 'Dropped'
                return True
    return False

def update_grade(enrollments, student, course, semester, grade):
    semester = _validate_normalize_enrollment_args(enrollments,student,course,semester)
    if grade is None:
        raise ValueError("Grade cannot be none")
    grade = Enrollment.grade_check(grade)
    for enrollment in enrollments:
        if(
            enrollment.sid == student.sid
            and enrollment.course_id == course.course_id
            and enrollment.semester == semester
        ): 
            if enrollment.status == 'Dropped':
                raise ValueError('This course is dropped')
            elif enrollment.status == 'Enrolled':
                enrollment.status = 'Completed'
            enrollment.grade = grade
            return True
    return False

def get_student_enrollments(enrollments, student, semester=None):
    if not isinstance(enrollments, list):
        raise TypeError("enrollments need to be an Enrollment list")
    if not isinstance(student, Student):
        raise TypeError("student needs to be a Student type")
    for enrollment in enrollments:
        if not isinstance(enrollment,Enrollment):
            raise TypeError("Need an Enrollment list")
    if semester is not None:
        semester = Enrollment.semester_check(semester)
    if semester is None:
        student_enrollments = [enrollment for enrollment in enrollments if enrollment.sid == student.sid]
    else:
        student_enrollments = [enrollment for enrollment in enrollments if enrollment.sid == student.sid
                   and semester == enrollment.semester]
    return student_enrollments

def get_course_enrollments(enrollments, course, semester=None):
    if not isinstance(enrollments, list):
        raise TypeError("enrollments need to be an Enrollment list")
    if not isinstance(course, Course):
        raise TypeError("course needs to be a Course type")
    for enrollment in enrollments:
        if not isinstance(enrollment,Enrollment):
            raise TypeError("Need an Enrollment list")
    if semester is not None:
        semester = Enrollment.semester_check(semester)
    if semester is None:
        course_enrollments = [enrollment for enrollment in enrollments if enrollment.course_id == course.course_id]
    else:
        course_enrollments = [enrollment for enrollment in enrollments if enrollment.course_id == course.course_id
                           and enrollment.semester == semester]
    return course_enrollments

def get_course_roster(enrollments, course, semester):
    enrollment_list = get_course_enrollments(enrollments,course,semester)
    student_in_course = [enrollment.student for enrollment in enrollment_list if enrollment.status == 'Enrolled']
    return student_in_course

def get_student_courses(enrollments, student,semester):
    enrollment_list = get_student_enrollments(enrollments,student,semester)
    student_courses = [enrollment.course for enrollment in enrollment_list if enrollment.status == 'Enrolled']
    return student_courses

GRADE_POINTS = {
    "A": 4.0,
    "AB": 3.5,
    "B": 3.0,
    "BC": 2.5,
    "C": 2.0,
    "D": 1.0,
    "F": 0.0
}
def calculate_gpa(enrollments, student, semester=None):
    enrollment_list = get_student_enrollments(enrollments,student,semester)
    total = 0
    all_credits =  0
    for enrollment in enrollment_list:
        if enrollment.grade is None:
            continue
        if enrollment.status == 'Completed':
            total += GRADE_POINTS[enrollment.grade] * enrollment.course.credits
            all_credits += enrollment.course.credits
    if all_credits == 0:
        return None
    return total/all_credits

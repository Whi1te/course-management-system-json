from models import Student, Course, Enrollment
from student_service import find_student
from course_service import find_course
import json
from pathlib import Path

def student_to_dict(student):
    if not isinstance(student,Student):
        raise TypeError("Student object only")
    student_dict = {'name': student.name,
                   'email': student.email,
                   'sid': student.sid,
                   'major': student.major}
    return student_dict

def course_to_dict(course):
    if not isinstance(course,Course):
        raise TypeError('Course object only')
    course_dict = {'course_id': course.course_id,
                   'name': course.name,
                   'credits': course.credits,
                   'instructor': course.instructor,
                   'capacity': course.capacity}
    return course_dict

def enrollment_to_dict(enrollment):
    if not isinstance(enrollment,Enrollment):
        raise TypeError("Enrollment object only")
    enrollment_dict = {'student': enrollment.sid,
                       'course': enrollment.course_id,
                       'semester': enrollment.semester,
                       'status': enrollment.status,
                       'grade': enrollment.grade}
    return enrollment_dict

def dict_to_student(data):
    if not isinstance(data,dict):
        raise TypeError('Need a dictionary')
    fields = ['name','email','sid','major']
    for field in fields:
        if field not in data:
            raise ValueError(f'Field {field} missed')
    return Student(data['name'],data['email'],data['sid'],data['major'])

def dict_to_course(data):
    if not isinstance(data,dict):
        raise TypeError('Need a dictionary')
    fields = ['course_id','name','credits','instructor','capacity']
    for field in fields:
        if field not in data:
            raise ValueError(f'Field {field} missed')
    return Course(data['course_id'],data['name'],data['credits'],data['instructor'],data['capacity'])

def dict_to_enrollment(data,students,courses):
    if not isinstance(data,dict):
        raise TypeError('Need a dictionary')
    fields = ['student','course','semester','status','grade']
    for field in fields:
        if field not in data:
            raise ValueError(f'Field {field} missed')
    student = find_student(students,data['student'])
    if student is None:
        raise ValueError("Student not found")
    course = find_course(courses,data['course'])
    if course is None:
        raise ValueError("Course not found")
    return Enrollment(student,course,data['semester'],data['status'],data['grade'])

def build_data(students, courses, enrollments):
    if not isinstance(students,list) or not isinstance(courses,list) or not isinstance(enrollments,list):
        raise TypeError('List data only')
    student_list = [student_to_dict(student) for student in students]
    course_list = [course_to_dict(course) for course in courses]
    enrollment_list = [enrollment_to_dict(enrollment) for enrollment in enrollments]
    data = {'Students': student_list,
            'Courses': course_list,
            'Enrollments': enrollment_list}
    return data

def save_data(students, courses, enrollments, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = build_data(students,courses,enrollments)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_raw_data(path):
    path = Path(path)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON file")
    return data

def load_data(path):
    raw_data = load_raw_data(path)

    if raw_data is None:
        return [], [], []

    if not isinstance(raw_data, dict):
        raise TypeError("Invalid data format")
    fields = ['Students', 'Courses', 'Enrollments']
    for field in fields:
        if field not in raw_data:
            raise ValueError(f'Field {field} missed')
        if not isinstance(raw_data[field], list):
            raise TypeError(f"{field} must be a list")

    students = [dict_to_student(student) for student in raw_data.get('Students')]
    courses = [dict_to_course(course) for course in raw_data.get('Courses')]
    enrollments = [dict_to_enrollment(enrollment, students,courses) 
                   for enrollment in raw_data.get('Enrollments')]

    return students, courses, enrollments
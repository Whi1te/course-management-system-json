from pathlib import Path
from save_load import save_data, load_data
from models import Student,Course,Enrollment
import student_service as ss
import course_service as cs
import enrollment_service as es

DATA_FILE = Path(__file__).parent / 'data'/ 'course_management.json'

def show_student_menu():
    print('''
1. Add Student
2. Find Student
3. Update Student
4. Delete Student
0. Back
''')

def student_menu(students,enrollments):
    while True:
        show_student_menu()
        choice_s = input('Choose an option').strip()
        match choice_s:
            case '0':
                break
            case '1':
                name = input("Enter the student's name:")
                email = input("Enter the student's email:")
                sid = input("Enter the student's sid:")
                major = input("Enter the student's major:")
                try:
                    student = Student(name,email,sid,major)
                    ss.add_student(students,student)
                except(ValueError,TypeError) as e:
                    print(f"Failed to add student: {e}")
                else:
                    print('Student added')
            case '2':
                sid = input("Enter the student's sid:")
                try:
                    student = ss.find_student(students,sid)
                except(TypeError,ValueError) as e:
                    print(f"Failed to find student: {e}")
                else:
                    if student is None:
                        print("Student not found")
                    else:
                        print(student)
            case '3':
                sid = input("Enter the student's sid:")
                print('Enter new information for student or ' 
                'Enter 0 to keep original information')
                name = input("Enter the update name or 0 to keep:").strip()
                email = input("Enter the update email or 0 to keep:").strip()
                major = input("Enter the update major or 0 to keep:").strip()
                if name == '0': 
                    name = None
                if email == '0': 
                    email = None
                if major == '0': 
                    major = None
                try:
                    success = ss.update_student(students,sid,name,email,major)
                except (TypeError,ValueError)as e:
                    print(f"Failed to update student: {e}")
                else:
                    if success:
                        print("Student updated")
                    else:
                        print("Student not found")
            case '4':
                sid = input("Enter the student's sid:")
                try:
                    sid = Student.sid_chek(sid)
                except(TypeError,ValueError) as e:
                    print(f"Failed to delete student: {e}")
                    continue
                if any(enrollment.sid == sid for enrollment in enrollments):
                    print("Cannot delete student with enrollment records")
                    continue
                try:
                    success = ss.delete_student(students,sid)
                except(TypeError,ValueError)as e:
                    print(f"Failed to delete student: {e}")
                else:
                    if success:
                        print("Student deleted")
                    else:
                        print("Student not found")
            case _:
                print('Invalid command')

def show_course_menu():
    print('''
1. Add Course
2. Find Course
3. Update Course
4. Delete Course
0. Back
''')

def course_menu(courses,enrollments):
    while True:
        show_course_menu()
        choice = input("Choose a command").strip()
        match choice:
            case "1":
                course_id = input("Enter the course id: ")
                name = input("Enter the course name: ")
                credits = input("Enter the course credits: ")
                instructor = input("Enter the instructor's name: ")
                capacity = input("Enter the course capacity: ")
                try:
                    new_course = Course(course_id,name,credits,instructor,capacity)
                    cs.add_course(courses,new_course)
                except(TypeError,ValueError) as e:
                    print(f"Failed to add course: {e}")
                else:
                    print("Course added")
            case '2':
                course_id = input("Enter the course id: ")
                try:
                    course = cs.find_course(courses,course_id)
                except(TypeError,ValueError) as e:
                    print(f'Failed to find course: {e}')
                else:
                    if course is not None:
                        print(course)
                    else:
                        print('Course not found')
            case '3':
                course_id = input("Enter the course id:")
                print('Enter new information for course or ' 
                      'Enter 0 to keep original information')
                name = input("Enter the update course name or 0 to keep:").strip()
                credits = input("Enter the update credits or 0 to keep:").strip()
                instructor = input("Enter the update instructor or 0 to keep:").strip()
                capacity = input("Enter the update capacity or 0 to keep:").strip()
                if name == '0':
                    name = None
                if credits == '0':
                    credits = None
                if instructor == '0':
                    instructor = None
                if capacity == '0':
                    capacity = None
                try:
                    result = cs.update_course(courses,course_id,name,credits,instructor,capacity)
                except(ValueError,TypeError)as e:
                    print(f'Failed to update course: {e}')
                else:
                    if result:
                        print('Course updated')
                    else:
                        print('Course not found')
            case '4':
                course_id = input("Enter the course id:")
                try:
                    course_id = Course.normalize_course_id(course_id)
                except(ValueError,TypeError)as e:
                    print(f'Failed to delete course: {e}')
                    continue
                if any(enrollment.course_id == course_id for enrollment in enrollments):
                    print("Cannot delete course with enrollment records")
                    continue
                try:
                    result = cs.delete_course(courses,course_id)
                except(ValueError,TypeError)as e:
                    print(f'Failed to delete course: {e}')
                else:
                    if result:
                        print('Course deleted')
                    else:
                        print('Course not found')
            case '0':
                break
            case _:
                print("Invalid command")

def show_enrollment_menu():
    print('''
1. Enroll Student
2. Drop Course
3. Update Grade
0. Back
''')

def enrollment_menu(students, courses, enrollments):
    while True:
        show_enrollment_menu()
        choice = input("Choose a command: ").strip()

        def get_enrollment_info(students, courses):
            sid = input("Enter student's sid: ").strip()
            course_id = input("Enter course id: ").strip()
            semester = input("Enter the semester: ").strip()

            try:
                student = ss.find_student(students, sid)
                course = cs.find_course(courses, course_id)
            except (ValueError, TypeError) as e:
                print(f"Invalid input: {e}")
                return None

            if student is None:
                print("Student not found")
                return None

            if course is None:
                print("Course not found")
                return None

            return student, course, semester

        match choice:
            case '0':
                break

            case '1':
                info = get_enrollment_info(students, courses)
                if info is None:
                    continue
                student, course, semester = info
                try:
                    es.enroll_student(enrollments,student,course,semester)
                except(TypeError,ValueError) as e:
                    print(f'Failed to enroll {e}')
                else:
                    print('Enrolled')

            case '2':
                info = get_enrollment_info(students, courses)
                if info is None:
                    continue
                student, course, semester = info
                try:
                    result = es.drop_course(enrollments,student,course,semester)
                except(TypeError,ValueError) as e:
                    print(f'Failed to drop {e}')
                else:
                    if result:
                        print('Course dropped')
                    else:
                        print('Course not found or already dropped')
                
            case '3':
                info = get_enrollment_info(students, courses)
                if info is None:
                    continue
                student, course, semester = info
                grade = input("Enter the grade: ").strip()
                try:
                    result = es.update_grade(enrollments,student,course,semester, grade)
                except(TypeError,ValueError) as e:
                    print(f'Failed to update {e}')
                else:
                    if result:
                        print('updated')
                    else:
                        print('Update failed')
            case _:
                print("Invalid command")


def show_report_menu():
    print('''
1. View Course Roster
2. View Current Courses
3. Calculate Student GPA
0. Back    
''')

def report_menu(students, courses, enrollments):
    while True:
        show_report_menu()
        choice = input("Choose a command: ").strip()
        match choice:
            case '1':
                semester = input("Enter the semester or 0 for all semester: ").strip()
                if semester == '0':
                    semester = None
                course_id = input("Enter the course id: ")
                try:
                    course = cs.find_course(courses,course_id)
                except(TypeError,ValueError) as e:
                    print(f"Failed to find course: {e}")
                else:
                    if course is None:
                        print("Course not found")
                    else:
                        try:
                            course_roster = es.get_course_roster(enrollments,course,semester)
                        except(ValueError,TypeError)as e:
                            print(f"Failed to get course roster: {e}")
                        else:
                            print(course_roster)

            case '2':
                semester = input("Enter the semester or 0 for all semester: ").strip()
                if semester == '0':
                    semester = None
                sid = input("Enter the sid: ")
                try:
                    student = ss.find_student(students,sid)
                except(TypeError,ValueError) as e:
                    print(f"Failed to find student: {e}")
                else:
                    if student is None:
                        print("Student not found")
                    else:
                        try:
                            student_courses = es.get_student_courses(enrollments,student,semester)
                        except(ValueError,TypeError)as e:
                            print(f"Failed to get student courses: {e}")
                        else:
                            print(student_courses)

            case '3':
                semester = input("Enter the semester or 0 for all semester: ").strip()
                if semester == '0':
                    semester = None
                sid = input("Enter the sid: ")
                try:
                    student = ss.find_student(students,sid)
                except(TypeError,ValueError) as e:
                    print(f"Failed to find student: {e}")
                else:
                    if student is None:
                        print("Student not found")
                    else:
                        try:
                            gpa = es.calculate_gpa(enrollments,student,semester)
                        except(ValueError,TypeError)as e:
                            print(f"Failed to get student's gpa: {e}")
                        else:
                            if gpa is None:
                                print('No completed graded courses found')
                            else:
                                print(f"GPA: {gpa:.2f}")   
            case '0':
                break
            case _:
                print("Invalid command")


def show_menu():
    print(
'''
1. Student Management
2. Course Management
3. Enrollment Management
4. View Reports
0. Save and Exit
''')
    
def main():
    students,courses,enrollments = load_data(DATA_FILE)
    print(students)
    print(courses)
    print(enrollments)

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        match choice:
            case '0':
                save_data(students, courses, enrollments, DATA_FILE)
                break
            case '1':
                student_menu(students,enrollments)
            case '2':
                course_menu(courses,enrollments)
            case '3':
                enrollment_menu(students, courses, enrollments)
            case '4':
                report_menu(students, courses, enrollments)
            case _ :
                print('Invalid command')





if __name__ == "__main__":
    main()

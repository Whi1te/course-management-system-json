from models import Student

def add_student(students, student):
    if not isinstance(student,Student):
        raise TypeError('Only accept Student type')
    if not isinstance(students,list):
        raise TypeError('Only accept Student list')
    for i in students:
        if not isinstance(i,Student):
            raise TypeError('Only accept Student list')
        if i.sid == student.sid:
            raise ValueError("Student already exists")
    students.append(student)
    return True

def find_student(students, sid):
    if not isinstance(students,list):
        raise TypeError('Only accept Student list')
    for student in students:
        if not isinstance(student,Student):
            raise TypeError('Only accept Student list')
    sid = Student.sid_chek(sid)
    for student in students:
        if student.sid == sid:
            return student
    return None

def delete_student(students, sid):
    result = find_student(students,sid)
    if result is None:
        return False
    students.remove(result)
    return True

def update_student(students, sid, name=None, email=None, major=None):
    result = find_student(students,sid)
    if result is None:
        return False
    if name is not  None:
        result.name = name
    if email is not  None:
        result.email = email
    if major is not None:
        result.major = major
    return True
    
    
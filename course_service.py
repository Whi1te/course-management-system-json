from models import Course

def add_course(courses, course):
    if not isinstance(courses,list):
        raise TypeError("courses needs to be a list")
    if not isinstance(course,Course):
        raise TypeError("course needs to be a Course type")
    for c in courses:
        if not isinstance(c, Course):
            raise TypeError("Course type only")
        if c.course_id == course.course_id:
            raise ValueError("Duplicate course")
    courses.append(course)
    return True

def find_course(courses, course_id):
    if not isinstance(courses,list):
        raise TypeError("courses needs to be a list")
    for c in courses:
        if not isinstance(c, Course):
            raise TypeError("Course type only")
    course_id = Course.normalize_course_id(course_id)
    for course in courses:
        if course.course_id == course_id:
            return course
    return None


def delete_course(courses, course_id):
    result = find_course(courses,course_id)
    if result is not None:
        courses.remove(result)
        return True
    return False

def update_course(
    courses,
    course_id,
    name=None,
    credits=None,
    instructor=None,
    capacity=None
):
    result = find_course(courses,course_id)
    if result is None:
        return False
    if name is not None:
        result.name = name
    if credits is not None:
        result.credits = credits
    if instructor is not None:
        result.instructor = instructor
    if capacity is not None:
        result.capacity = capacity
    return True

    

        
            
    
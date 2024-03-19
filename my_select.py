from sqlalchemy import func
from conf.models import Student, Grade, Group, Subject, Teacher
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from conf.db import session
from sqlalchemy import desc



# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1(session):

    query = session.query(Student, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Grade, Student.id == Grade.student_id) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.grade).desc()) \
        .limit(5)

    results = query.all()
    return results


#  Знайти студента із найвищим середнім балом з певного предмета.
def select_2(session, subject_id):
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .join(Grade) \
        .filter(Grade.subjects_id == subject_id) \
        .group_by(Student.id, Student.fullname) \
        .order_by(desc('average_grade')) \
        .limit(1) \
        .all()
    return result

# Знайти середній бал у групах з певного предмета.
def select_3(session, subject_id):

    query = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Student, Group.id == Student.group_id) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subjects_id == Subject.id) \
        .filter(Subject.id == subject_id) \
        .group_by(Group.name)

    results = query.all()
    return results

# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4(session):
    query = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))

    result = query.scalar()
    return result

#Знайти які курси читає певний викладач.
def select_5(session, teacher_id):
    query = session.query(Subject.name) \
        .filter(Subject.teacher_id == teacher_id)

    results = query.all()
    return results

# Знайти список студентів у певній групі
def select_6(session, group_id):
    query = session.query(Student.fullname) \
        .filter(Student.group_id == group_id)

    results = query.all()
    return results

# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(session, group_id, subject_id):
    query = session.query(Student.fullname, Grade.grade) \
        .join(Group, Student.group_id == Group.id) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subjects_id == Subject.id) \
        .filter(Group.id == group_id) \
        .filter(Subject.id == subject_id)

    results = query.all()
    return results
#Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(session, teacher_id):
    query = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Student, Grade.student_id == Student.id) \
        .join(Subject, Grade.subjects_id == Subject.id) \
        .filter(Subject.teacher_id == teacher_id)

    result = query.scalar()
    return result
#Знайти список курсів, які відвідує певний студент.
def select_9(session, student_id):
    query = session.query(Subject.name) \
        .join(Grade, Subject.id == Grade.subjects_id) \
        .filter(Grade.student_id == student_id) \
        .distinct()

    results = query.all()
    return results

def select_10(session, student_id, teacher_id):
    query = session.query(Subject.name) \
        .join(Grade, Subject.id == Grade.subjects_id) \
        .join(Student, Grade.student_id == Student.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Student.id == student_id) \
        .filter(Teacher.id == teacher_id) \
        .distinct()

    results = query.all()
    return results

def select_0(session):
    result = session.query(Student.id).all()
    return result

def select_05(session):
    result = session.query(Subject.id).all()
    return result

def main():
    try:
        #result_0 = select_0(session)
        # result_05 = select_05(session)
        #result_1 = select_1(session)
        #result_2 = select_2(session, 18)
        #result_3 = select_3(session, 18)
        #result_4 = select_4(session)
        #result_5 = select_5(session, 9)
        #result_6 = select_6(session, 9)
        # result_7 = select_7(session, 7, 20)
        #result_8 = select_8(session, 13)
        #result_9 = select_9(session, 124)
        result_10 = select_10(session, 124, 13)

        # Виведення результатів
        # print("Результат запиту 1:")
        # for student, avg_grade in result_1:
        #     print(f"Студент: {student.fullname}, Середній бал: {avg_grade}")

        # print(f"Результат запиту 2: {result_2}")
        # print(f"Результат запиту 3: ")
        # for student, avg_grade in result_3:
        #     print(f"Група: {student}, Середній бал: {avg_grade}")
        #print(f"Результат запиту 4: {result_4}")
        #print(f"Результат запиту 5: {result_5}")
        #print(f"Результат запиту 0: {result_0}")
        # print(f"Результат запиту 05: {result_05}")
        #print(f"Результат запиту 6: {result_6}")
        # print(f"Результат запиту 7: {result_7}")
        #print(f"Результат запиту 8: {result_8}")
        #print(f"Результат запиту 9: {result_9}")
        print(f"Результат запиту 10: {result_10}")
    except SQLAlchemyError as e:
        print(f"Помилка при виконанні запиту: {e}")

    finally:
        # Закриття сесії
        if session:
            session.close()


if __name__ == "__main__":
    main()

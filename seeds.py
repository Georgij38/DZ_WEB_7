from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf.models import Teacher, Group, Student, Subject, Grade
import random
from datetime import datetime, timedelta
from conf.db import URI
# Створення мотора бази даних
engine = create_engine(URI)

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Ініціалізація Faker
fake = Faker('uk_UA')

# Створення вчителів
teachers = []
for _ in range(5):
    teacher = Teacher(fullname=fake.name())
    teachers.append(teacher)
session.add_all(teachers)
session.commit()

# Створення груп
groups = []
for i in range(3):
    group = Group(name=f'Group {i+1}')
    groups.append(group)
session.add_all(groups)
session.commit()

# Створення студентів
students = []
for _ in range(50):
    student = Student(fullname=fake.name(), group=random.choice(groups))
    students.append(student)
session.add_all(students)
session.commit()

# Створення предметів і призначення їх вчителям
subjects = []
for _ in range(8):
    subject = Subject(name=fake.word(), teacher=random.choice(teachers))
    subjects.append(subject)
session.add_all(subjects)
session.commit()

# Створення оцінок для студентів по предметах
for student in students:
    for subject in subjects:
        grade = Grade(grade=random.randint(1, 12), date_of=fake.date_between(start_date='-1y', end_date='today'),student=student, subjects_id=subject.id)

        session.add(grade)
session.commit()

# Закриття сесії
session.close()

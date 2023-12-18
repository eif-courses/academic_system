from database import Database

if __name__ == "__main__":
    db = Database("academic_system.db")
    db.create_tables()

    # Test the methods
    admin_user = db.create_admin_user(db)
    print("Admin User ID:", admin_user.id)

    group = db.create_student_group(db, "PI22E")
    print("Student Group ID:", group.id)

    course = db.create_course(db, "Programming")
    print("Course ID:", course.id)

    subject = db.create_subject(db, "Programming Practice")
    print("Subject ID:", subject.id)

    lecturer = db.create_lecturer(db, "Tom", "tom", "root", admin_user.id)
    print("Lecturer ID:", lecturer.id)

    student = db.create_student(db, "Alona Makeieva", "alona", "makeieva", admin_user.id, group.id)
    print("Student ID:", student.id)

    db.enroll_student_in_subject(db, student.id, subject.id)
    print("Student enrolled in Subject.")

    db.enter_grade_for_student(db, student.id, subject.id, 9)
    print("Grade entered for Student.")

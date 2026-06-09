import sys
import os

# Make sure imports work when running from any directory
sys.path.insert(0, os.path.dirname(__file__))

from services.school_system import SchoolSystem


MENU = """
╔══════════════════════════════════════════╗
║   Student Course Registration System    ║
╠══════════════════════════════════════════╣
║  1. Add Student                          ║
║  2. View Students                        ║
║  3. Search Student                       ║
║  4. Add Course                           ║
║  5. View Courses                         ║
║  6. Register Student to Course           ║
║  7. View Students in a Course            ║
║  8. View Courses for a Student           ║
║  9. Save Data                            ║
║ 10. Load Data                            ║
║  0. Exit                                 ║
╚══════════════════════════════════════════╝
"""


def run():
    system = SchoolSystem()

    print("\n  Welcome to the Student Course Registration System")
    print("  Loading saved data...\n")
    system.load_data()

    while True:
        print(MENU)
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            system.add_student()
        elif choice == "2":
            system.view_students()
        elif choice == "3":
            system.search_student()
        elif choice == "4":
            system.add_course()
        elif choice == "5":
            system.view_courses()
        elif choice == "6":
            system.register_student()
        elif choice == "7":
            system.view_students_in_course()
        elif choice == "8":
            system.view_courses_for_student()
        elif choice == "9":
            system.save_data()
        elif choice == "10":
            system.load_data()
        elif choice == "0":
            print("\n  Saving data before exit...")
            system.save_data()
            print("  Goodbye! 👋\n")
            break
        else:
            print("\n  ⚠  Invalid option. Please choose a number from the menu.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    run()

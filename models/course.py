class Course:
    def __init__(self, course_id, course_name, trainer, capacity):
        self.course_id = course_id
        self.course_name = course_name
        self.trainer = trainer
        self.capacity = capacity

    def display(self):
        print(f"  Course ID   : {self.course_id}")
        print(f"  Course Name : {self.course_name}")
        print(f"  Trainer     : {self.trainer}")
        print(f"  Capacity    : {self.capacity} students")

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "trainer": self.trainer,
            "capacity": self.capacity,
        }

    @staticmethod
    def from_dict(data):
        return Course(
            data["course_id"],
            data["course_name"],
            data["trainer"],
            data["capacity"],
        )

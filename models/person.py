class Person:
    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number

    def display(self):
        print(f"  Name  : {self.name}")
        print(f"  Email : {self.email}")
        print(f"  Phone : {self.phone_number}")

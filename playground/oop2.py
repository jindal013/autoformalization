class Employee:
    
    def __init__(self, first, last):
        self.first = first
        self.last = last
    
    @property
    def email(self):
        return f"{self.first}-{self.last}@email.com"

    @property
    def fullname(self):
        return f"{self.first} {self.last}"
    
    @fullname.setter
    def fullname(self, name):
        first, last = name.split(" ")
        self.first = first
        self.last = last
    
    @fullname.deleter
    def fullname(self):
        print('Delete Name!')
        self.first = None
        self.last = None

emp1 = Employee("Chinmay", "Jindal")

emp1.fullname = "Mark Cuban"

print(emp1.first)
print(emp1.last)
print(emp1.email)

# try:
#     result = 10 / int(input("Enter a number: "))
# except (ValueError, ZeroDivisionError) as e:
#     print(f"An error occurred: {repr(e)}")
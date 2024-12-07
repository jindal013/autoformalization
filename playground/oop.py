class Employee:

    num_of_emps = 0
    raise_amt = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + "." + last + "@company.com"

        Employee.num_of_emps += 1
    
    def __repr__(self):
        return "Employee=('{}', '{}', {})".format(self.first, self.last, self.pay)
    
    def __str__(self):
        return f"{self.fullname()} - {self.email}"

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)
    
    def __add__(self, other):
        return self.pay + other.pay

    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amt = amount
    
    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split('-')
        return cls(first, last, pay)

class Developer(Employee):
    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        # Employee.__init__(self, first, last, pay) # which is not the same as Employee(first, last, pay) as that creates a new object versus giving the current instance the desired atributes
        self.prog_lang = prog_lang

class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

dev_1 = Developer('Chinmay', prog_lang="C++", pay=100000, last='Jindal')
emp_2 = Employee('Mark', 'Cuban', 3000000)

# print(repr(Developer))

print(dev_1 + emp_2)
# print(dev_1.prog_lang)

# print(dev_1.email)
# print(dev_2.pay)
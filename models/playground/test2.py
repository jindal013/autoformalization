class A:
    def method(self):
        print("A's method")

class B(A):
    def method(self):
        print("B's method")
        super().method()

class C(A):
    def method(self):
        print("C's method")
        super().method()

class D(B, C): # order here influences the method resolution order (MRO)
    def method(self):
        print("D's method")
        super().method()

# Let's print out the MRO
D().method()
# This will show the order of classes that will be searched when using super()
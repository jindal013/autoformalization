class Value:
    """ stores a single scalar value and its gradient """

    def __init__(self, data, _children=(), _op=''):
        assert isinstance(data, (int, float)), "data can only be int/float"
        self.data = data
        self.grad = 0.0
        self._prev = set(_children) # used for backprop
        self._backward = lambda : None # used for backprop
        self._op = _op # for debugging
    
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward

        return out
    
    def __pow__(self, other):
        assert isinstance(other, (float, int)), "pow supports only int and float"
        out = Value(self.data ** other, (self,), f"**{other}")

        def _backward():
            self.grad += other * (self.data ** (other - 1)) * out.grad
        out._backward = _backward

        return out

    def relu(self):
        o = 0.0 if self.data < 0 else self.data
        out = Value(o, (self,), "relu")

        def _backward():
            self.grad += (o > 0) * out.grad
        out._backward = _backward

        return out
    
    def backward(self):

        topo = []
        visited = set()

        def build(root):
            if root not in visited:
                visited.add(root)
                for n in root._prev:
                    build(n)
                topo.append(root)
        build(self)

        self.grad = 1.0 # have to remember this
        for i in reversed(topo):
            i._backward()
        
    def __neg__(self):
        return self * (-1)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other
    
    def __radd__(self, other):
        return self + other
    
    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        return self * other**-1
    
    def __rtruediv__(self, other):
        return other * self**-1
    
    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"
class Set(set):
    def __init__(self, *args, **kwds):
        super(Set, self).__init__(*args, **kwds)
    
    def __mul__(self, other_set):
        if len(self) * len(other_set) == 0:
            return Set()

        result = Set()
        for elem in self:
            for other_elem in other_set:
                result.add(elem + other_elem)
        
        return result
    
    def __add__(self, other_set):
        return Set(self.union(other_set))
    
    def first(self, k):
        result = Set()
        for elem in self:
            result.add(elem[:k])
        
        return result
    
    def last(self, k):
        result = Set()
        for elem in self:
            result.add(elem[-k:])
        
        return result

def add_method(cls):
    def decorator(method):
        setattr(cls, method.__name__, method)
        return method
    return decorator
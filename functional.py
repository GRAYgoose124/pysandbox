from functools import wraps


def take(it, n):
    """Take n elements from it."""
    if callable(it):
        it = it()

    for _ in range(n):
        yield next(it) 


class Partial:
    def __init__(self, f, *args, **kwargs):
        self.f, self.args, self.kwargs = f, args, kwargs
    
    def __call__(self, *args, **kwargs): 
        new_partial = Partial(self.f, *(*self.args, *args), **{**self.kwargs, **kwargs})

        try:
            return new_partial.f(*new_partial.args, **new_partial.kwargs)
        except TypeError:
            return new_partial

    def __repr__(self):
        return f'{self.f.__name__}({self.args}, {self.kwargs})'


def partial_map(f, it):
    for e in it:
        yield Partial(f, e)


def partial(*pargs, **pkwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return Partial(func, *(*pargs, *args), **{**pkwargs, **kwargs})
        return wrapper()
    return decorator


def partial_test():    
    def mysum(a, b, kw=None):
        return a + b

    @partial(3)
    def psum(a, b, kw=None):
        return a + b

    a = Partial(mysum)
    print('a', a)
    print('a()', a())
    print('a(2)', a(2))
    print('a(2)(2)', a(2)(2))
    print('a(2, 2)', a(2, 2))
    
    e = psum
    print('e', e)
    print('e()', e())
    print('e(1)', e(1))


def partial_map_test():
    x = partial_map(lambda x, y, z: x - y + z, range(10, 1, -1))
    print([pe(i)()(1) for i, pe in enumerate(x)])

partial_test()
partial_map_test()
   
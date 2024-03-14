def func(x, y):
    return x * y

print(func('abc', 3))

print(func(4, 3))

def func_annotations(x: 'for_x', y: 'for_y') -> 'for_return':
    return x * y

print(func_annotations('abc', 3))
print(func_annotations(4, 3))
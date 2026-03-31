def fac(n):
    if n < 2:
        return 1
    return n * fac(n-1)

for i in range(1, 10):
    print(f'{i}! = {fac(i)}')
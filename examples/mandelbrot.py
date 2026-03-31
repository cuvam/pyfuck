def mandelbrot_divergence_test(c, iterations=100):
    curr = complex(real=0, imag=0)
    for i in range(iterations):
        curr = curr*curr + c
        if curr.real*curr.real + curr.imag*curr.imag > 4:
            return i # diverges (when magnitude > 2, guaranteed to diverge)
    return -1

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) / (in_max - in_min) * (out_max - out_min) + out_min

def mandelbrot_divergence_matrix(xLo, xHi, yLo, yHi, rows, cols, its):
    r_rows = []
    for y in range(rows):
        row = []
        for x in range(cols):
            mapped = (map_range(x, 0, cols, xLo, xHi), map_range(y, 0, rows, yLo, yHi))
            cnum = complex(real=mapped[0], imag=mapped[1])
            val = mandelbrot_divergence_test(cnum, iterations=its)
            row.append(val)
        r_rows.append(row)
    return r_rows

def mandelbrot(xLo, xHi, yLo, yHi, rows, cols, its):
    m = mandelbrot_divergence_matrix(xLo, xHi, yLo, yHi, rows, cols, its)
    shades = '.:-=+*#%@'
    for row in m:
        for val in row:
            if val == -1:
                print(' ', end='')
            else:
                print(shades[int(map_range(val, 0, its, 0, len(shades)-1))], end='')
        print()

mandelbrot(0.272, 0.275, 0.005, 0.008, 50, 100, 500)
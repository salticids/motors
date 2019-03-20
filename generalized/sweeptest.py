class A():
    def __init__(self, a, b):
        self.a = a
        self.b = b

class SweepRow():
    def __init__(self, start, stop, step, mutable, param):
        self.start = start
        self.state = self.start
        self.stop = stop
        self.step = step
        self.mutable = mutable
        self.param = param

def mutsweep(rows, index, f):
    row = rows[index]
    row.state = row.start
    row.mutable.__dict__[row.param] = row.start
    while row.state <= row.stop:
        if index < len(rows)-1:
            mutsweep(rows, index+1, f)
        else:
            f()
        row.state += row.step
        row.mutable.__dict__[row.param] += row.step


r = []
B = A(0, 1)
C = A(2, 3)
r.insert(0, SweepRow(1,2,1, B, 'b'))
r.insert(0, SweepRow(1,2,1, B, 'a'))
# r.append(Row(0,1,0.5))
def fu():
    print(B.a, B.b)
mutsweep(r, 0, fu)